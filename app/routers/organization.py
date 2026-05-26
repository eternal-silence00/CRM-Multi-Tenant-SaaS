from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.organization import OrganizationRepo
from app.schemas.organization import OrganizationCreate, OrganizationResponse
from app.services.auth import get_current_user
from app.models.user import User
from app.schemas.auth import UserResponse

router = APIRouter()

@router.post("/organization", response_model=OrganizationResponse, status_code=201)
async def create_organization(
    data: OrganizationCreate,
    session: AsyncSession = Depends(get_db)
):
    repo = OrganizationRepo(session)
    organization_exists = await repo.get_organization_by_name(data.name)
    if organization_exists:
        raise HTTPException(status_code=400, detail="Organization already exists")
    organization = await repo.create_organization(name=data.name, description=data.description)
    return organization

@router.get("/organization/{org_id}/workers", response_model=list[UserResponse])
async def get_all_organizations_workers(
    org_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    repo = OrganizationRepo(session)
    organization_exists = await repo.get_organization_by_id(org_id)
    if not organization_exists:
        raise HTTPException(status_code=403, detail="Organization not found")
    if organization_exists.id != user.organization_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    result = await repo.get_all_organization_workers(org_id)
    return result 