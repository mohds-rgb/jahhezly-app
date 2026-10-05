import json
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

import os
from sqlalchemy import select

from .db import Base, SessionLocal, engine
from .models import (
    MerchantOrganization, Store, StaffMembership, StaffUser, Product,
    ProductAvailability, ProductPrice,
)
from .security.passwords import hash_password

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "demo"

def load_demo():
    merchants = json.loads((DATA / "merchants.json").read_text(encoding="utf-8"))
    catalog = json.loads((DATA / "catalog.json").read_text(encoding="utf-8"))
    return merchants, catalog

def seed():
    password = os.getenv("JAHHEZLY_DEMO_STAFF_PASSWORD")
    if not password:
        raise SystemExit("Refusing to seed without JAHHEZLY_DEMO_STAFF_PASSWORD.")
    Base.metadata.create_all(bind=engine)
    merchants, catalog = load_demo()
    db = SessionLocal()
    try:
        staff = db.scalar(select(StaffUser).where(StaffUser.email == "demo.manager@jahhezly.local"))
        if not staff:
            staff = StaffUser(
                id=str(uuid.uuid4()), email="demo.manager@jahhezly.local",
                display_name="Demo Merchant Manager",
                password_hash=hash_password(password), active=True,
            )
            db.add(staff); db.flush()

        product_by_merchant = {}
        for merchant in merchants["merchants"]:
            org = db.scalar(select(MerchantOrganization).where(MerchantOrganization.name == merchant["name"]))
            if not org:
                org = MerchantOrganization(id=str(uuid.uuid4()), name=merchant["name"])
                db.add(org); db.flush()

            for idx, branch in enumerate(merchant["branches"], start=1):
                store = db.scalar(select(Store).where(Store.name == branch["name"]))
                if not store:
                    store = Store(
                        id=str(uuid.uuid4()), organization_id=org.id, name=branch["name"],
                        city=merchant.get("city"), district=merchant.get("district"),
                        branch_code=f"BR-{idx:02d}", active=True,
                    )
                    db.add(store); db.flush()
                membership = db.scalar(select(StaffMembership).where(
                    StaffMembership.user_id == staff.id, StaffMembership.store_id == store.id
                ))
                if not membership:
                    db.add(StaffMembership(
                        id=str(uuid.uuid4()), user_id=staff.id, organization_id=org.id,
                        store_id=store.id, role="MERCHANT_ADMIN", active=True,
                    ))
                product_by_merchant.setdefault(merchant["name"], []).append(store)

        db.flush()
        for item in catalog["products"]:
            stores = product_by_merchant.get(item["merchant"], [])
            for store in stores:
                sku = f"{item['sku']}-{store.branch_code}"
                product = db.scalar(select(Product).where(Product.store_id == store.id, Product.sku == sku))
                if not product:
                    product = Product(
                        id=str(uuid.uuid4()), store_id=store.id, sku=sku,
                        name=item["name_en"], name_ar=item["name_ar"],
                        description=item.get("description_en", ""), description_ar=item.get("description_ar"),
                        category=item["category_en"], category_ar=item.get("category_ar"),
                        unit_label=item["unit"], active=True, version=1,
                    )
                    db.add(product); db.flush()
                    db.add(ProductAvailability(product_id=product.id, state="AVAILABLE", updated_by=staff.id, version=1))
                    db.add(ProductPrice(
                        id=str(uuid.uuid4()), product_id=product.id, amount=Decimal(str(item["price_syp"])),
                        currency="SYP", effective_from=datetime.now(timezone.utc), status="ACTIVE",
                        created_by=staff.id, version=1,
                    ))
        db.commit()
        print("Jahhezly demo data seeded.")
        print("email=demo.manager@jahhezly.local")
        print("password=<value supplied to JAHHEZLY_DEMO_STAFF_PASSWORD>")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
