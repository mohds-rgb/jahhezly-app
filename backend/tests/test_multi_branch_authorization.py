from app.models import StaffMembership

def login(client):
    return client.post("/v1/auth/login", json={"email":"manager@test.example","password":"password-123"}).json()["accessToken"]

def test_user_with_second_membership_can_access_that_branch(client, seeded):
    db = seeded["db"]
    db.add(StaffMembership(
        id="second-membership",
        user_id=seeded["user"].id,
        organization_id=seeded["org"].id,
        store_id=seeded["other_store"].id,
        role="STORE_MANAGER",
        active=True,
    ))
    db.commit()
    token = login(client)
    r = client.get(f"/v1/merchant/orders?store_id={seeded['other_store'].id}", headers={"Authorization":f"Bearer {token}"})
    assert r.status_code == 200


def test_inconsistent_org_membership_is_not_authorized(client, seeded):
    from app.models import MerchantOrganization
    import uuid
    other_org = MerchantOrganization(id=str(uuid.uuid4()), name="Other Org")
    db = seeded["db"]
    db.add(other_org)
    db.add(StaffMembership(
        id="bad-membership", user_id=seeded["user"].id, organization_id=other_org.id,
        store_id=seeded["other_store"].id, role="STORE_MANAGER", active=True,
    ))
    db.commit()
    token = login(client)
    r = client.get(f"/v1/merchant/orders?store_id={seeded['other_store'].id}", headers={"Authorization":f"Bearer {token}"})
    assert r.status_code == 403
