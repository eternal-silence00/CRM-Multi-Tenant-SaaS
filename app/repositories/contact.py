from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.contact import Contact

class ContactRepo:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_contact(self, organization_id: int , name: str, email: str, phone: str):
        contact = Contact( organization_id = organization_id ,name=name, email=email, phone=phone)
        self.session.add(contact)
        await self.session.flush()
        await self.session.refresh(contact)
        return contact
    
    async def get_contact_by_email(self, email: str):
        result = await self.session.execute(select(Contact).where(Contact.email == email))
        return result.scalar_one_or_none()
    
    async def get_contact_by_phone(self, phone: str):
        result = await self.session.execute(select(Contact).where(Contact.phone == phone))
        return result.scalar_one_or_none()
    
    async def get_contact_by_id(self, id: int):
        result = await self.session.execute(select(Contact).where(Contact.id == id))
        return result.scalar_one_or_none()
    
    async def get_contacts_by_organization_id(self, organization_id: int, limit: int = 10, offset: int = 0):
        result = await self.session.execute(select(Contact).where(Contact.organization_id == organization_id).limit(limit).offset(offset))
        return result.scalars().all()