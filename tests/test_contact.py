async def test_create_contact(client_with_token, user_org_id):
    response = await client_with_token.post("/contact", json={
        "organization_id": user_org_id,
        "name": "Test",
        "email": "contact@mail.com",
        "phone": "77328382343",
    })
    assert response.status_code == 201
    
async def test_create_contact_with_same_email(client_with_token, user_org_id):
    response = await client_with_token.post("/contact", json={
        "organization_id": user_org_id,
        "name": "Test",
        "email": "contact@mail.com",
        "phone": "77345354334",
    })
    assert response.status_code == 400
    
async def test_create_contact_with_same_phone(client_with_token, user_org_id):
    response = await client_with_token.post("/contact", json={
        "organization_id": user_org_id,
        "name": "Test",
        "email": "contact2@mail.com",
        "phone": "77328382343",
    })
    assert response.status_code == 400
    
async def test_get_all_contacts(client_with_token, user_org_id):
    response = await client_with_token.get(f"contact/organization/{user_org_id}")
    assert response.status_code == 200
    
async def test_get_contact_by_id(client_with_token, contact_id):
    response = await client_with_token.get(f"/contact/{contact_id}")
    assert response.status_code == 200
    
async def test_get_wrong_contact(client_with_token):
    response = await client_with_token.get("/contact/999")
    assert response.status_code == 404