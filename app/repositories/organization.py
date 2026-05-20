from sqlalchemy.ext.asyncio import AsyncSession
from app.models.organization import Organization
from app.models.user import User
from sqlalchemy import select

class OrganizationRepo:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_organization(
        self, name: str, description: str
    ):
        organization = Organization(name = name, description = description)
        self.session.add(organization)
        await self.session.flush()
        await self.session.refresh(organization)
        return organization
    
    async def get_all_organization_workers(self, organization_id: int):
        result = await self.session.execute(select(User).where(User.organization_id == organization_id))
        return result.scalars().all()
    
    async def get_organization_by_id(self, organization_id: int):
        result = await self.session.execute(select(Organization).where(Organization.id == organization_id))
        return result.scalar_one_or_none()
    
    async def get_organization_by_name(self, name: str):
        result = await self.session.execute(select(Organization).where(Organization.name == name))
        return result.scalar_one_or_none()
    
    