async def test_register(async_client):
    org_response = await async_client.post("/organization", json={
        "name": "Auth Test Org",
        "description": "Test"
    })
    org_id = org_response.json()["id"]
    response = await async_client.post("/auth/register", json={
        "email": "test@mail.com",
        "password": "test123",
        "organization_id": org_id
    })
    assert response.status_code == 201
    
async def test_register_with_same_email(async_client):
    response = await async_client.post("/auth/register", json={
        "email": "test@mail.com",
        "password": "pass",
        "organization_id": 1
    })
    assert response.status_code == 400
    
async def test_login(async_client):
    response = await async_client.post("/auth/login", json={
        "email": "test@mail.com",
        "password": "test123"
    })
    assert response.status_code == 200
    
async def test_login_with_wrong_password(async_client):
    response = await async_client.post("/auth/login", json={
        "email": "test@mail.com",
        "password": "wrong"
    })
    assert response.status_code == 401
    
