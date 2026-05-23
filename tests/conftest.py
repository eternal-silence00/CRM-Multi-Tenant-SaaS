import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db
from app.models.base import Base

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:password@db_test:5432/multi_tenant_saas_test"

test_engine = create_async_engine(TEST_DATABASE_URL)

TestSessionLocal = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()
    
async def override_get_db():
    async with TestSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        
@pytest.fixture(scope="session")
async def async_client():
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client
    app.dependency_overrides.clear()
    
@pytest.fixture(scope="session")
async def client_with_token():
    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        org_response = await client.post("/organization", json={
            "name": "Test Org",
            "description": "Test"
        })
        org_id = org_response.json()["id"]
        await client.post("/register",
                          json={
                              "email": "test@mail.com",
                              "password": "test123",
                              "organization_id": org_id
                          })
        response = await client.post("/login",
                                     json={
                                         "email": "test@mail.com",
                                         "password": "test123"
                                     })
        token = response.json()["access_token"]
        client.headers["Authorization"] = f"Bearer {token}"
        yield client
    app.dependency_overrides.clear()