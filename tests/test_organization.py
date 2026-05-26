async def test_get_organization_workers(client_with_token, user_org_id):
    response = await client_with_token.get(f"/organization/{user_org_id}/workers")
    assert response.status_code == 200
    
async def test_get_wrong_organization_workers(client_with_token):
    response = await client_with_token.get("/organization/999/workers")
    assert response.status_code == 403