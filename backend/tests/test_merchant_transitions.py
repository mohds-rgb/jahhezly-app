def login(client):
    return client.post("/v1/auth/login",
        json={"email":"manager@test.example","password":"password-123"}
    ).json()["accessToken"]

def create_order(client,seed):
    return client.post("/v1/orders",
        json={"storeId":seed["store"].id,
              "items":[{"productId":seed["product"].id,"quantity":1,"clientUnitPrice":"6.25"}]},
        headers={"X-Idempotency-Key":"transition-key","X-Guest-Session":"transition-guest"}
    ).json()

def test_stale_version_rejected(client,seeded):
    token=login(client); order=create_order(client,seeded)
    h={"Authorization":f"Bearer {token}","If-Match":"1"}
    accepted=client.post(f"/v1/merchant/orders/{order['id']}/accept",headers=h)
    assert accepted.status_code==200 and accepted.json()["version"]==2
    stale=client.post(f"/v1/merchant/orders/{order['id']}/start-preparing",
                      headers={"Authorization":f"Bearer {token}","If-Match":"1"})
    assert stale.status_code==409 and stale.json()["code"]=="CONFLICT"
    fresh=client.post(f"/v1/merchant/orders/{order['id']}/start-preparing",
                      headers={"Authorization":f"Bearer {token}","If-Match":"2"})
    assert fresh.status_code==200 and fresh.json()["state"]=="PREPARING"

def test_terminal_state_rejected(client,seeded):
    token=login(client); order=create_order(client,seeded)
    for endpoint,version in [("accept",1),("start-preparing",2),("ready",3),("collect",4)]:
        r=client.post(f"/v1/merchant/orders/{order['id']}/{endpoint}",
                      headers={"Authorization":f"Bearer {token}","If-Match":str(version)})
        assert r.status_code==200
    r=client.post(f"/v1/merchant/orders/{order['id']}/start-preparing",
                  headers={"Authorization":f"Bearer {token}","If-Match":"5"})
    assert r.status_code==409 and r.json()["code"]=="INVALID_STATE_TRANSITION"
