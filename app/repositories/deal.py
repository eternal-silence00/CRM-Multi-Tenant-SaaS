from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.deal import Deal
from app.models.contact import Contact
from app.schemas.deal import DealPatch

class DealRepo:
    
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def create_deal(self, contact_id: int, title: str, amount: float):
        deal = Deal(contact_id=contact_id, title=title, amount=amount )
        self.session.add(deal)
        await self.session.flush()
        await self.session.refresh(deal)
        return deal
    
    async def delete_deal(self, deal_id):
        result = await self.session.execute(select(Deal).where(Deal.id == deal_id))
        deal = result.scalar_one_or_none()
        await self.session.delete(deal)
        await self.session.flush()
    
    async def patch_deal(self, deal: Deal, data: DealPatch):
        updates = data.model_dump(exclude_unset=True)
        for keys, values in updates.items():
            setattr(deal, keys, values)
        return deal
    
    async def get_deal_by_id(self, deal_id: int):
        result = await self.session.execute(select(Deal).where(Deal.id == deal_id))
        return result.scalar_one_or_none()
    
    async def get_all_organization_deals(self, organization_id: int, limit: int = 10, offset: int = 0):
        result = await self.session.execute(
            select(Deal)
            .join(Contact, Deal.contact_id == Contact.id)
            .where(Contact.organization_id == organization_id)
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()