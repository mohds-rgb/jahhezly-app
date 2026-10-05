from app.security.passwords import hash_password, verify_password

def test_password_hash_verifies():
    hashed=hash_password("valid-password")
    assert hashed.startswith("scrypt$")
    assert verify_password("valid-password",hashed)
    assert not verify_password("wrong-password",hashed)

def test_catalog_route_is_public(client,seeded):
    r=client.get(f"/v1/stores/{seeded['store'].id}/catalog")
    assert r.status_code==200
    assert r.json()[0]["name"]=="Test Milk"


def test_invalid_customer_phone_rejected(client,seeded):
    r=client.post("/v1/orders",json={
        "storeId":seeded["store"].id,
        "items":[{"productId":seeded["product"].id,"quantity":1,"clientUnitPrice":"6.25"}],
        "customerPhone":"not-a-phone",
    },headers={"X-Idempotency-Key":"bad-phone","X-Guest-Session":"guest-phone"})
    assert r.status_code==422


def test_duplicate_product_lines_rejected(client,seeded):
    r=client.post("/v1/orders",json={
        "storeId":seeded["store"].id,
        "items":[
            {"productId":seeded["product"].id,"quantity":1,"clientUnitPrice":"6.25"},
            {"productId":seeded["product"].id,"quantity":1,"clientUnitPrice":"6.25"},
        ],
    },headers={"X-Idempotency-Key":"duplicate-lines","X-Guest-Session":"guest-duplicate"})
    assert r.status_code==422
