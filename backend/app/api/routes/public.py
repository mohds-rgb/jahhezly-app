from fastapi import APIRouter, Depends, Header, Request
from sqlalchemy.orm import Session

from ...db import get_db
from ...models import Store
from ...schemas import CategoryOut, CatalogItemOut, CreateOrderRequest, OrderOut, StoreOut
from ...services.catalog import list_catalog, list_categories
from ...services.orders import cancel_customer_order, get_customer_order, submit_order

router = APIRouter(prefix="/v1", tags=["customer"])

def correlation_id(request: Request) -> str:
    return request.headers.get("X-Correlation-Id", request.state.correlation_id)

@router.get("/stores", response_model=list[StoreOut])
def stores(db: Session = Depends(get_db)):
    return db.query(Store).filter(Store.active.is_(True)).order_by(Store.name).all()

@router.get("/stores/{store_id}/catalog", response_model=list[CatalogItemOut])
def catalog(store_id: str, db: Session = Depends(get_db)):
    return list_catalog(db, store_id)

@router.get("/stores/{store_id}/categories", response_model=list[CategoryOut])
def categories(store_id: str, db: Session = Depends(get_db)):
    return [CategoryOut(value=value) for value in list_categories(db, store_id)]

@router.post("/orders", response_model=OrderOut, status_code=201)
def create_order(
    payload: CreateOrderRequest,
    request: Request,
    db: Session = Depends(get_db),
    idempotency_key: str | None = Header(default=None, alias="X-Idempotency-Key"),
    guest_session: str | None = Header(default=None, alias="X-Guest-Session"),
):
    response, _replayed = submit_order(
        db, payload=payload, idempotency_key=idempotency_key or "",
        guest_session=guest_session or "", correlation_id=correlation_id(request),
    )
    return response

@router.get("/orders/{order_id}", response_model=OrderOut)
def get_order(
    order_id: str,
    db: Session = Depends(get_db),
    guest_session: str | None = Header(default=None, alias="X-Guest-Session"),
):
    return get_customer_order(db, order_id, guest_session or "")

@router.post("/orders/{order_id}/cancel", response_model=OrderOut)
def cancel_order(
    order_id: str,
    request: Request,
    expected_version: int = Header(..., alias="If-Match"),
    db: Session = Depends(get_db),
    guest_session: str | None = Header(default=None, alias="X-Guest-Session"),
):
    return cancel_customer_order(db, order_id, guest_session or "", correlation_id(request), expected_version)
