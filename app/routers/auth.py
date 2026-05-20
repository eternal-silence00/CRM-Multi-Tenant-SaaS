from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.auth import hash_password, verify_password, create_access_token
from app.schemas.auth import UserCreate, UserResponse, TokenResponse
from app.repositories.user import UserRepo
from app.repositories.organization import OrganizationRepo

router = APIRouter()

@router.post("/auth/register", response_model=UserResponse, status_code=201)
async def register(
    data: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    repo = UserRepo(session)
    org_repo = OrganizationRepo(session)
    organization_exists = await org_repo.get_organization_by_id(data.organization_id)
    if not organization_exists:
        raise HTTPException(status_code=400, detail="Organization does not exsists")
    user_exists = await repo.get_by_email(data.email)
    if user_exists:
        raise HTTPException(status_code=400, detail="User alredy exsists")
    hashed_password = hash_password(data.password)
    user = await repo.create_user(data.email, hashed_password, data.organization_id)
    return user

@router.post("/auth/login", response_model=TokenResponse, status_code=200)
async def login(
    data: UserCreate,
    session: AsyncSession = Depends(get_db)
):
    repo = UserRepo(session)
    user = await repo.get_by_email(data.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    verified = verify_password(data.password, user.hashed_password)
    if not verified:
        raise HTTPException(status_code=401, detail="Wronf password")
    token = create_access_token({"sub":str(user.id)})
    return {"access_token":token, "token_type": "bearer"}
            