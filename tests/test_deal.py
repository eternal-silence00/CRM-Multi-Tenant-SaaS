async def test_create_deal(client_with_token, deal_contact_id):
    response = await client_with_token.post("/deal", json={
        "contact_id": deal_contact_id,
        "title": "Test Deal",
        "amount": 1000.0,
        "status": "New"
    })
    assert response.status_code == 201

async def test_get_deal_by_id(client_with_token, deal_id):
    response = await client_with_token.get(f"/deal/{deal_id}")
    assert response.status_code == 200

async def test_get_wrong_deal(client_with_token):
    response = await client_with_token.get("/deal/999")
    assert response.status_code == 404

async def test_get_all_organization_deals(client_with_token, user_org_id):
    response = await client_with_token.get(f"/deal/organization/{user_org_id}")
    assert response.status_code == 200

async def test_patch_deal(client_with_token, deal_id):
    response = await client_with_token.patch(f"/deal/{deal_id}", json={
        "status": "Won"
    })
    assert response.status_code == 200

async def test_delete_deal(client_with_token, deal_id):
    response = await client_with_token.delete(f"/deal/{deal_id}")
    assert response.status_code == 200