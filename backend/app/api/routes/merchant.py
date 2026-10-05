from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session

from ...db import get_db
from ...domain.errors import not_found
from ...models import Order, Product, Store
from ...schemas import (
    AvailabilityRequest, MerchantMembershipOut, MerchantMeOut, MerchantOrderListItem, OrderOut, PriceCreateRequest,
    ProductCreateRequest, ProductPatchRequest,
)
from ...security.dependencies import StaffContext, expected_version_header, get_current_staff, require_capability
from ...services.catalog import create_product, patch_product, set_availability, set_price
from ...services.orders import merchant_list_orders, serialize_order, transition_order

router = APIRouter(prefix="/v1/merchant", tags=["merchant"])

@router.get("/me", response_model=MerchantMeOut)
def me(context: StaffContext = Depends(get_current_staff), db: Session = Depends(get_db)):
    memberships = []
    for membership in context.memberships:
        store = db.get(Store, membership.store_id)
        if not store:
            continue
        memberships.append(MerchantMembershipOut(
            storeId=store.id, storeName=store.name, city=store.city, district=store.district,
            branchCode=store.branch_code, role=membership.role,
        ))
    return MerchantMeOut(userId=context.user.id, displayName=context.user.display_name, memberships=memberships)

def correlation_id(request: Request) -> str:
    return request.headers.get("X-Correlation-Id", request.state.correlation_id)

@router.get("/orders", response_model=list[MerchantOrderListItem])
def list_orders(
    store_id: str,
    context: StaffContext = Depends(get_current_staff),
    db: Session = Depends(get_db),
):
    require_capability("view_orders", store_id, context)
    return merchant_list_orders(db, store_id)

@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(
    order_id: str,
    context: StaffContext = Depends(get_current_staff),
    db: Session = Depends(get_db),
):
    order = db.get(Order, order_id)
    if not order:
        raise not_found("Order not found.")
    require_capability("view_orders", order.store_id, context)
    return serialize_order(db, order)

def _transition(order_id, target_state, request, expected_version, context, db):
    order = db.get(Order, order_id)
    if not order:
        raise not_found("Order not found.")
    membership = require_capability("transition_orders", order.store_id, context)
    return transition_order(
        db, order_id=order_id, target_state=target_state, expected_version=expected_version,
        actor_id=context.user.id, organization_id=membership.organization_id,
        store_id=order.store_id, correlation_id=correlation_id(request),
    )

@router.post("/orders/{order_id}/accept", response_model=OrderOut)
def accept_order(order_id, request: Request, expected_version: int = Depends(expected_version_header),
                 context: StaffContext = Depends(get_current_staff), db: Session = Depends(get_db)):
    return _transition(order_id, "ACCEPTED", request, expected_version, context, db)

@router.post("/orders/{order_id}/reject", response_model=OrderOut)
def reject_order(order_id, request: Request, expected_version: int = Depends(expected_version_header),
                 context: StaffContext = Depends(get_current_staff), db: Session = Depends(get_db)):
    return _transition(order_id, "REJECTED", request, expected_version, context, db)

@router.post("/orders/{order_id}/start-preparing", response_model=OrderOut)
def preparing_order(order_id, request: Request, expected_version: int = Depends(expected_version_header),
                    context: StaffContext = Depends(get_current_staff), db: Session = Depends(get_db)):
    return _transition(order_id, "PREPARING", request, expected_version, context, db)

@router.post("/orders/{order_id}/ready", response_model=OrderOut)
def ready_order(order_id, request: Request, expected_version: int = Depends(expected_version_header),
                context: StaffContext = Depends(get_current_staff), db: Session = Depends(get_db)):
    return _transition(order_id, "READY_FOR_PICKUP", request, expected_version, context, db)

@router.post("/orders/{order_id}/collect", response_model=OrderOut)
def collect_order(order_id, request: Request, expected_version: int = Depends(expected_version_header),
                  context: StaffContext = Depends(get_current_staff), db: Session = Depends(get_db)):
    return _transition(order_id, "COLLECTED", request, expected_version, context, db)

@router.post("/catalog/products", response_model=dict, status_code=201)
def add_product(payload: ProductCreateRequest, request: Request,
                context: StaffContext = Depends(get_current_staff), db: Session = Depends(get_db)):
    require_capability("manage_catalog", payload.storeId, context)
    product = create_product(
        db, actor_id=context.user.id, organization_id=context.membership_for(payload.storeId).organization_id,
        payload=payload, correlation_id=correlation_id(request),
    )
    db.commit()
    return {"id": product.id, "version": product.version}

@router.patch("/catalog/products/{product_id}", response_model=dict)
def update_product(product_id: str, payload: ProductPatchRequest, request: Request,
                   context: StaffContext = Depends(get_current_staff), db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise not_found("Product not found.")
    require_capability("manage_catalog", product.store_id, context)
    membership = require_capability("manage_catalog", product.store_id, context)
    updated = patch_product(
        db, actor_id=context.user.id, organization_id=membership.organization_id,
        product_id=product.id, payload=payload, correlation_id=correlation_id(request),
    )
    db.commit()
    return {"id": updated.id, "version": updated.version}

@router.post("/catalog/products/{product_id}/price", response_model=dict)
def add_price(product_id: str, payload: PriceCreateRequest, request: Request,
              context: StaffContext = Depends(get_current_staff), db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise not_found("Product not found.")
    require_capability("manage_prices", product.store_id, context)
    membership = require_capability("manage_prices", product.store_id, context)
    row = set_price(
        db, actor_id=context.user.id, organization_id=membership.organization_id,
        product_id=product_id, payload=payload, correlation_id=correlation_id(request),
    )
    db.commit()
    return {"id": row.id, "amount": row.amount, "currency": row.currency}

@router.post("/catalog/products/{product_id}/availability", response_model=dict)
def availability(product_id: str, payload: AvailabilityRequest, request: Request,
                 context: StaffContext = Depends(get_current_staff), db: Session = Depends(get_db)):
    product = db.get(Product, product_id)
    if not product:
        raise not_found("Product not found.")
    require_capability("manage_availability", product.store_id, context)
    membership = require_capability("manage_availability", product.store_id, context)
    row = set_availability(
        db, actor_id=context.user.id, organization_id=membership.organization_id,
        product_id=product_id, state=payload.state, correlation_id=correlation_id(request),
    )
    db.commit()
    return {"productId": row.product_id, "state": row.state, "version": row.version}
