import uuid
from datetime import datetime, timezone
from decimal import Decimal

from app.models import MerchantOrganization, Store, StaffUser, StaffMembership, Product, ProductPrice, ProductAvailability
from app.security.passwords import hash_password

def seed_graph(db):
    org=MerchantOrganization(id=str(uuid.uuid4()),name="Test Organization")
    store=Store(id=str(uuid.uuid4()),organization_id=org.id,name="Test Store A",active=True)
    other=Store(id=str(uuid.uuid4()),organization_id=org.id,name="Test Store B",active=True)
    user=StaffUser(id=str(uuid.uuid4()),email="manager@test.example",display_name="Test Manager",
                   password_hash=hash_password("password-123"),active=True)
    membership=StaffMembership(id=str(uuid.uuid4()),user_id=user.id,organization_id=org.id,store_id=store.id,
                               role="STORE_MANAGER",active=True)
    product=Product(id=str(uuid.uuid4()),store_id=store.id,sku="P-001",name="Test Milk",description="Test",
                    category="Dairy",unit_label="1L",active=True,version=1)
    availability=ProductAvailability(product_id=product.id,state="AVAILABLE",updated_by=user.id,version=1)
    price=ProductPrice(id=str(uuid.uuid4()),product_id=product.id,amount=Decimal("6.25"),currency="DEM",
                       effective_from=datetime.now(timezone.utc),status="ACTIVE",created_by=user.id,version=1)
    db.add_all([org,store,other,user,membership,product,availability,price])
    db.commit()
    return {"org":org,"store":store,"other_store":other,"user":user,"product":product,"price":price}
