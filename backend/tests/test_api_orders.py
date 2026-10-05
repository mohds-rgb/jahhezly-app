from app.models import Order
def payload(seed, price="6.25", qty=2):
    return {
        "storeId": seed["store"].id,
        "items":[{"productId":seed["product"].id,"quantity":qty,"clientUnitPrice":price}],
        "note":"Portfolio demo",
    }

def test_stale_price_rejected(client,seeded):
    r=client.post("/v1/orders",json=payload(seeded,"5.00"),
                  headers={"X-Idempotency-Key":"price-1","X-Guest-Session":"guest-1"})
    assert r.status_code==409
    assert r.json()["code"]=="PRICE_CHANGED"

def test_idempotent_repeat_returns_same_order(client,seeded):
    headers={"X-Idempotency-Key":"same-key","X-Guest-Session":"guest-2"}
    first=client.post("/v1/orders",json=payload(seeded),headers=headers)
    second=client.post("/v1/orders",json=payload(seeded),headers=headers)
    assert first.status_code==201 and second.status_code==201
    assert first.json()==second.json()
    orders = seeded["db"].query(Order).count()
    assert orders == 1

def test_idempotency_key_reuse_different_payload_rejected(client,seeded):
    headers={"X-Idempotency-Key":"reuse-key","X-Guest-Session":"guest-3"}
    assert client.post("/v1/orders",json=payload(seeded),headers=headers).status_code==201
    r=client.post("/v1/orders",json=payload(seeded,qty=3),headers=headers)
    assert r.status_code==409
    assert r.json()["code"]=="CONFLICT"

def test_guest_order_is_owner_scoped(client,seeded):
    r=client.post("/v1/orders",json=payload(seeded),
                  headers={"X-Idempotency-Key":"own-1","X-Guest-Session":"owner-a"})
    order_id=r.json()["id"]
    denied=client.get(f"/v1/orders/{order_id}",headers={"X-Guest-Session":"owner-b"})
    assert denied.status_code==403
    assert denied.json()["code"]=="FORBIDDEN"


def test_customer_phone_is_persisted(client,seeded):
    response=client.post("/v1/orders",json={
        "storeId":seeded["store"].id,
        "items":[{"productId":seeded["product"].id,"quantity":1,"clientUnitPrice":"6.25"}],
        "customerPhone":"+963 944-123456",
    },headers={"X-Idempotency-Key":"phone-1","X-Guest-Session":"phone-guest"})
    assert response.status_code==201
    order=seeded["db"].get(Order,response.json()["id"])
    assert order.customer_phone=="+963944123456"


def test_cancel_uses_optimistic_version(client,seeded):
    create=client.post("/v1/orders",json=payload(seeded),headers={"X-Idempotency-Key":"cancel-1","X-Guest-Session":"cancel-guest"})
    order_id=create.json()["id"]
    stale=client.post(f"/v1/orders/{order_id}/cancel",headers={"X-Guest-Session":"cancel-guest","If-Match":"2"})
    assert stale.status_code==409
    assert stale.json()["code"]=="CONFLICT"
    fresh=client.post(f"/v1/orders/{order_id}/cancel",headers={"X-Guest-Session":"cancel-guest","If-Match":"1"})
    assert fresh.status_code==200
    assert fresh.json()["state"]=="CANCELLED"
