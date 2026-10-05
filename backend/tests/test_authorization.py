def login(client):
    return client.post("/v1/auth/login",
        json={"email":"manager@test.example","password":"password-123"}
    ).json()["accessToken"]

def test_cross_store_denied(client,seeded):
    token=login(client)
    r=client.get(f"/v1/merchant/orders?store_id={seeded['other_store'].id}",
                 headers={"Authorization":f"Bearer {token}"})
    assert r.status_code==403
    assert r.json()["code"]=="FORBIDDEN"

def test_invalid_token_denied(client,seeded):
    r=client.get(f"/v1/merchant/orders?store_id={seeded['store'].id}",
                 headers={"Authorization":"Bearer invalid"})
    assert r.status_code==401
    assert r.json()["code"]=="UNAUTHORIZED"
