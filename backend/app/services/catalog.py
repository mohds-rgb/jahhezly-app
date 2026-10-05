from datetime import datetime, timezone
from decimal import Decimal
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..domain.errors import conflict, invalid, not_found
from ..models import Product, ProductAvailability, ProductPrice, Store
from .audit import record_audit

def now_utc():
    return datetime.now(timezone.utc)

def current_price(db: Session, product_id: str):
    now = now_utc()
    return db.scalar(
        select(ProductPrice).where(
            ProductPrice.product_id == product_id,
            ProductPrice.status == "ACTIVE",
            ProductPrice.effective_from <= now,
            (ProductPrice.effective_to.is_(None) | (ProductPrice.effective_to > now)),
        ).order_by(ProductPrice.effective_from.desc())
    )

def availability_for(db, product_id):
    row = db.get(ProductAvailability, product_id)
    return row.state if row else "UNAVAILABLE"

def list_catalog(db, store_id):
    store = db.get(Store, store_id)
    if not store or not store.active:
        raise not_found("Store not found.")
    products = db.scalars(
        select(Product).where(Product.store_id == store_id, Product.active.is_(True))
        .order_by(Product.category, Product.name)
    ).all()
    result=[]
    today=now_utc().date()
    for p in products:
        price=current_price(db,p.id)
        synced=price.effective_from if price else None
        result.append({
            "id":p.id,"sku":p.sku,"name":p.name,"nameAr":p.name_ar,
            "description":p.description,"descriptionAr":p.description_ar,
            "category":p.category,"categoryAr":p.category_ar,"unitLabel":p.unit_label,"active":p.active,
            "availability":availability_for(db,p.id),
            "price":price.amount if price else None,
            "currency":price.currency if price else None,
            "priceLastSyncedAt":synced,
            "stale": price is None or synced.date() < today,
        })
    return result

def list_categories(db, store_id):
    if not db.get(Store, store_id):
        raise not_found("Store not found.")
    return list(db.scalars(
        select(Product.category).where(Product.store_id == store_id, Product.active.is_(True))
        .distinct().order_by(Product.category)
    ).all())

def create_product(db, *, actor_id, organization_id, payload, correlation_id):
    store=db.get(Store,payload.storeId)
    if not store: raise not_found("Store not found.")
    product=Product(
        id=str(uuid.uuid4()), store_id=store.id, sku=payload.sku.strip(),
        name=payload.name.strip(), name_ar=payload.nameAr.strip() if payload.nameAr else None,
        description=payload.description.strip(), description_ar=payload.descriptionAr.strip() if payload.descriptionAr else None,
        category=payload.category.strip(), category_ar=payload.categoryAr.strip() if payload.categoryAr else None,
        unit_label=payload.unitLabel.strip(),
        image_ref=payload.imageRef, active=True, version=1,
    )
    db.add(product); db.flush()
    db.add(ProductAvailability(product_id=product.id,state="UNAVAILABLE",updated_by=actor_id,version=1))
    record_audit(db,actor_id=actor_id,organization_id=organization_id,store_id=store.id,
                 aggregate_id=product.id,action="product_created",
                 after={"sku":product.sku,"name":product.name},correlation_id=correlation_id)
    return product

def patch_product(db, *, actor_id, organization_id, product_id, payload, correlation_id):
    product=db.get(Product,product_id)
    if not product: raise not_found("Product not found.")
    before={"name":product.name,"active":product.active}
    fields=[("name","name"),("nameAr","name_ar"),("description","description"),("descriptionAr","description_ar"),
            ("category","category"),("categoryAr","category_ar"),("unitLabel","unit_label"),
            ("imageRef","image_ref"),("active","active")]
    for src,dst in fields:
        value=getattr(payload,src)
        if value is not None: setattr(product,dst,value.strip() if isinstance(value,str) else value)
    product.version += 1
    record_audit(db,actor_id=actor_id,organization_id=organization_id,store_id=product.store_id,
                 aggregate_id=product.id,action="product_updated",before=before,
                 after={"name":product.name,"active":product.active},correlation_id=correlation_id)
    return product

def set_price(db, *, actor_id, organization_id, product_id, payload, correlation_id):
    product=db.get(Product,product_id)
    if not product: raise not_found("Product not found.")
    now=now_utc()
    active=current_price(db,product.id)
    before={"amount":str(active.amount),"currency":active.currency} if active else None
    if active:
        active.effective_to=now
        active.status="EXPIRED"
    row=ProductPrice(
        id=str(uuid.uuid4()),product_id=product.id,amount=payload.amount.quantize(Decimal("0.01")),
        currency=payload.currency.upper(),effective_from=now,status="ACTIVE",created_by=actor_id,version=1
    )
    db.add(row); db.flush()
    record_audit(db,actor_id=actor_id,organization_id=organization_id,store_id=product.store_id,
                 aggregate_id=product.id,action="price_changed",before=before,
                 after={"amount":str(row.amount),"currency":row.currency},correlation_id=correlation_id)
    return row

def set_availability(db, *, actor_id, organization_id, product_id, state, correlation_id):
    if state not in {"AVAILABLE","UNAVAILABLE"}: raise invalid("Invalid availability state.")
    product=db.get(Product,product_id)
    if not product: raise not_found("Product not found.")
    row=db.get(ProductAvailability,product.id)
    before={"state":row.state} if row else None
    if row is None:
        row=ProductAvailability(product_id=product.id,state=state,updated_by=actor_id,version=1); db.add(row)
    else:
        row.state=state; row.updated_by=actor_id; row.updated_at=now_utc(); row.version+=1
    record_audit(db,actor_id=actor_id,organization_id=organization_id,store_id=product.store_id,
                 aggregate_id=product.id,action="availability_changed",before=before,
                 after={"state":state},correlation_id=correlation_id)
    return row
