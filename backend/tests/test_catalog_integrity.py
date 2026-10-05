from decimal import Decimal
from app.models import ProductPrice
from app.services.catalog import current_price,set_price

def test_price_history_preserved(seeded,db):
    class Payload:
        amount=Decimal("6.75")
        currency="DEM"
    old=seeded["price"]
    set_price(db,actor_id=seeded["user"].id,organization_id=seeded["org"].id,
              product_id=seeded["product"].id,payload=Payload(),correlation_id="test")
    db.commit()
    active=current_price(db,seeded["product"].id)
    assert active.amount==Decimal("6.75")
    historic=db.get(ProductPrice,old.id)
    assert historic.status=="EXPIRED"
    assert historic.effective_to is not None
