from __future__ import annotations

from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import uuid

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..config import settings
from ..domain.errors import conflict, forbidden, invalid, not_found
from ..domain.order import OrderState, can_transition
from ..models import IdempotencyRecord, Order, OrderItem, Product, ProductAvailability, Store
from .audit import record_audit
from .catalog import current_price


def now_utc():
    return datetime.now(timezone.utc)


def hash_guest_session(raw: str) -> str:
    return hashlib.sha256(raw.strip().encode()).hexdigest()


def canonical_request(payload) -> str:
    return json.dumps(
        {
            "storeId": payload.storeId,
            "customerPhone": payload.customerPhone,
            "items": [
                {
                    "productId": item.productId,
                    "quantity": item.quantity,
                    "clientUnitPrice": str(item.clientUnitPrice) if item.clientUnitPrice is not None else None,
                }
                for item in payload.items
            ],
            "note": payload.note,
        },
        sort_keys=True,
        separators=(",", ":"),
    )


def _order_dict(order, items):
    return {
        "id": order.id,
        "publicOrderCode": order.public_order_code,
        "storeId": order.store_id,
        "state": order.state,
        "customerPhone": order.customer_phone,
        "totalAmount": str(order.total_amount),
        "currency": order.currency,
        "version": order.version,
        "submittedAt": order.submitted_at.isoformat(),
        "items": [
            {
                "productId": item.product_id,
                "productName": item.product_name_snapshot,
                "quantity": item.quantity,
                "unitPrice": str(item.unit_price_snapshot),
                "currency": item.currency_snapshot,
                "lineTotal": str(item.line_total_snapshot),
            }
            for item in items
        ],
    }


def serialize_order(db: Session, order: Order):
    items = db.scalars(select(OrderItem).where(OrderItem.order_id == order.id)).all()
    return _order_dict(order, items)


def submit_order(db: Session, *, payload, idempotency_key, guest_session, correlation_id):
    if not settings.allow_guest_orders:
        raise forbidden("Guest order submission is disabled.")
    if not idempotency_key or len(idempotency_key) > 100:
        raise invalid("X-Idempotency-Key is required and must be <= 100 characters.")
    if not guest_session or len(guest_session) > 200:
        raise invalid("X-Guest-Session is required for anonymous order submission.")

    store = db.get(Store, payload.storeId)
    if not store or not store.active:
        raise not_found("Store not found.")

    session_hash = hash_guest_session(guest_session)
    req_hash = hashlib.sha256(canonical_request(payload).encode()).hexdigest()
    existing = db.scalar(
        select(IdempotencyRecord).where(
            IdempotencyRecord.store_id == store.id,
            IdempotencyRecord.customer_session_hash == session_hash,
            IdempotencyRecord.idempotency_key == idempotency_key,
        )
    )
    if existing:
        if existing.request_hash != req_hash:
            raise conflict("CONFLICT", "The idempotency key was already used with a different request.")
        return json.loads(existing.response_json), True

    accepted = []
    currencies = set()
    for item in payload.items:
        product = db.scalar(
            select(Product).where(
                Product.id == item.productId,
                Product.store_id == store.id,
                Product.active.is_(True),
            )
        )
        if not product:
            raise not_found("One or more requested products do not exist in this store.")

        availability = db.get(ProductAvailability, product.id)
        if not availability or availability.state != "AVAILABLE":
            raise conflict(
                "PRODUCT_UNAVAILABLE",
                f"{product.name} is currently unavailable.",
                {"productId": product.id},
            )

        price = current_price(db, product.id)
        if not price:
            raise conflict("PRODUCT_UNAVAILABLE", "Product has no active price.", {"productId": product.id})

        if item.clientUnitPrice is not None and item.clientUnitPrice.quantize(Decimal("0.01")) != price.amount.quantize(Decimal("0.01")):
            raise conflict(
                "PRICE_CHANGED",
                f"The price of {product.name} changed.",
                {
                    "productId": product.id,
                    "clientUnitPrice": str(item.clientUnitPrice),
                    "serverUnitPrice": str(price.amount),
                    "currency": price.currency,
                },
            )

        currencies.add(price.currency)
        accepted.append(
            (
                product,
                price,
                item.quantity,
                (price.amount * item.quantity).quantize(Decimal("0.01")),
            )
        )

    if len(currencies) != 1:
        raise invalid("All items in one order must use the same currency.")

    currency = next(iter(currencies))
    total = sum((row[3] for row in accepted), Decimal("0.00"))
    now = now_utc()
    order = Order(
        id=str(uuid.uuid4()),
        public_order_code="JHZ-" + uuid.uuid4().hex[:8].upper(),
        store_id=store.id,
        customer_session_hash=session_hash,
        customer_phone=payload.customerPhone,
        state=OrderState.SUBMITTED,
        submitted_at=now,
        total_amount=total,
        currency=currency,
        version=1,
        note=payload.note.strip(),
    )
    db.add(order)
    db.flush()

    item_rows = []
    for product, price, qty, line_total in accepted:
        row = OrderItem(
            id=str(uuid.uuid4()),
            order_id=order.id,
            product_id=product.id,
            product_name_snapshot=product.name,
            quantity=qty,
            unit_price_snapshot=price.amount.quantize(Decimal("0.01")),
            currency_snapshot=price.currency,
            line_total_snapshot=line_total,
            item_state="REQUESTED",
        )
        db.add(row)
        item_rows.append(row)

    response = _order_dict(order, item_rows)
    db.add(
        IdempotencyRecord(
            id=str(uuid.uuid4()),
            store_id=store.id,
            customer_session_hash=session_hash,
            idempotency_key=idempotency_key,
            request_hash=req_hash,
            response_json=json.dumps(response, sort_keys=True),
            response_status=201,
            order_id=order.id,
        )
    )
    record_audit(
        db,
        actor_id=session_hash[:36],
        organization_id=store.organization_id,
        store_id=store.id,
        aggregate_id=order.id,
        action="order_submitted",
        after={"state": order.state, "total": str(order.total_amount)},
        correlation_id=correlation_id,
    )
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        existing = db.scalar(
            select(IdempotencyRecord).where(
                IdempotencyRecord.store_id == store.id,
                IdempotencyRecord.customer_session_hash == session_hash,
                IdempotencyRecord.idempotency_key == idempotency_key,
            )
        )
        if existing and existing.request_hash == req_hash:
            return json.loads(existing.response_json), True
        raise
    return response, False


def get_customer_order(db, order_id, guest_session):
    order = db.get(Order, order_id)
    if not order:
        raise not_found("Order not found.")
    if order.customer_session_hash != hash_guest_session(guest_session):
        raise forbidden("You are not authorized to access this order.")
    return serialize_order(db, order)


def cancel_customer_order(db, order_id, guest_session, correlation_id, expected_version):
    order = db.get(Order, order_id)
    if not order:
        raise not_found("Order not found.")
    session_hash = hash_guest_session(guest_session)
    if order.customer_session_hash != session_hash:
        raise forbidden("You are not authorized to modify this order.")
    if not can_transition(order.state, OrderState.CANCELLED):
        raise conflict("INVALID_STATE_TRANSITION", "This order cannot be cancelled.")

    now = now_utc()
    result = db.execute(
        update(Order)
        .where(
            Order.id == order_id,
            Order.customer_session_hash == session_hash,
            Order.version == expected_version,
        )
        .values(
            state=OrderState.CANCELLED,
            cancelled_at=now,
            version=expected_version + 1,
            updated_at=now,
        )
    )
    if result.rowcount != 1:
        db.rollback()
        raise conflict("CONFLICT", "The order was modified before cancellation. Refresh and retry.")

    store = db.get(Store, order.store_id)
    record_audit(
        db,
        actor_id=session_hash[:36],
        organization_id=store.organization_id,
        store_id=store.id,
        aggregate_id=order.id,
        action="order_cancelled",
        before={"state": order.state, "version": expected_version},
        after={"state": OrderState.CANCELLED, "version": expected_version + 1},
        correlation_id=correlation_id,
    )
    db.commit()
    return serialize_order(db, db.get(Order, order_id))


def merchant_list_orders(db, store_id):
    orders = db.scalars(
        select(Order)
        .where(Order.store_id == store_id)
        .order_by(Order.created_at.desc())
        .limit(200)
    ).all()
    result = []
    for order in orders:
        item_count = sum(db.scalars(select(OrderItem.quantity).where(OrderItem.order_id == order.id)).all())
        result.append(
            {
                "id": order.id,
                "publicOrderCode": order.public_order_code,
                "storeId": order.store_id,
                "state": order.state,
                "itemCount": item_count,
                "totalAmount": order.total_amount,
                "currency": order.currency,
                "version": order.version,
                "createdAt": order.created_at,
            }
        )
    return result


def transition_order(db, *, order_id, target_state, expected_version, actor_id, organization_id, store_id, correlation_id):
    order = db.scalar(select(Order).where(Order.id == order_id, Order.store_id == store_id))
    if not order:
        raise not_found("Order not found.")
    if not can_transition(order.state, target_state):
        raise conflict("INVALID_STATE_TRANSITION", f"Cannot move order from {order.state} to {target_state}.")

    before_state = order.state
    now = now_utc()
    values = {"state": target_state, "version": expected_version + 1, "updated_at": now}
    timestamp_fields = {
        "ACCEPTED": "accepted_at",
        "PREPARING": "preparing_at",
        "READY_FOR_PICKUP": "ready_at",
        "COLLECTED": "collected_at",
        "REJECTED": "rejected_at",
        "CANCELLED": "cancelled_at",
    }
    if target_state in timestamp_fields:
        values[timestamp_fields[target_state]] = now

    result = db.execute(
        update(Order)
        .where(
            Order.id == order_id,
            Order.store_id == store_id,
            Order.version == expected_version,
        )
        .values(**values)
    )
    if result.rowcount != 1:
        db.rollback()
        raise conflict("CONFLICT", "The order was modified by another operator. Refresh and retry.")

    record_audit(
        db,
        actor_id=actor_id,
        organization_id=organization_id,
        store_id=store_id,
        aggregate_id=order_id,
        action=f"order_{target_state.lower()}",
        before={"state": before_state, "version": expected_version},
        after={"state": target_state, "version": expected_version + 1},
        correlation_id=correlation_id,
    )
    db.commit()
    return serialize_order(db, db.get(Order, order_id))
