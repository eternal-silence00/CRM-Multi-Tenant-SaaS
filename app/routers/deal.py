from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.deal import DealRepo
from app.repositories.contact import ContactRepo
from app.schemas.deal import DealCreate, DealResponse, DealPatch
from app.services.auth import get_current_user
from app.models.user import User
from app.redis_client import redis_client
import json

router = APIRouter()


@router.post("/deal", response_model=DealResponse, status_code=201)
async def create_deal(
    data: DealCreate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    repo = DealRepo(session)
    cont_repo = ContactRepo(session)
    contact = await cont_repo.get_contact_by_id(data.contact_id)
    if not contact:
        raise HTTPException(status_code=400, detail= "Contact not found")
    if user.organization_id != contact.organization_id:
        raise HTTPException(status_code=400, detail="Not allowed")
    deal = await repo.create_deal(data.contact_id, data.title, data.amount)
    keys = await redis_client.keys(f"deals:{contact.organization_id}:*")
    if keys:
        await redis_client.delete(*keys)
    return deal 


@router.get("/deal/organization/{organization_id}")
async def get_all_organization_deals(
    organization_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = 10,
    offset: int = 0
):
    cache_key = f"deals:{organization_id}:{limit}:{offset}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    repo = DealRepo(session)
    if user.organization_id != organization_id:
        raise HTTPException(status_code=400, detail="Not allowed")
    result = await repo.get_all_organization_deals(organization_id, limit, offset)
    await redis_client.set(cache_key, json.dumps([{"id": t.id, "contact_id": t.contact_id, "title": t.title, "amount": t.amount, "status": t.status, "created_at": str(t.created_at)} for t in result]), ex=300)
    return result


@router.get("/deal/{deal_id}")
async def get_deal_by_id(
    deal_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    cache_key = f"deal:{deal_id}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    repo = DealRepo(session)
    cont_repo = ContactRepo(session)
    deal = await repo.get_deal_by_id(deal_id)
    if not deal: 
        raise HTTPException(status_code=404, detail="Deal not found")
    contact = await cont_repo.get_contact_by_id(deal.contact_id)
    if not contact:
        raise HTTPException(status_code=400, detail="Error, contact not found")
    if user.organization_id != contact.organization_id:
        raise HTTPException(status_code=400, detail="Not allowed")
    await redis_client.set(cache_key, json.dumps({"id": deal.id, "contact_id": deal.contact_id, "title": deal.title, "amount": deal.amount, "status": deal.status, "created_at": str(deal.created_at)}), ex=300)
    return deal


@router.patch("/deal/{deal_id}")
async def patch_deal(
    deal_id: int,
    updates: DealPatch,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    repo = DealRepo(session)
    cont_repo = ContactRepo(session)
    
    deal = await repo.get_deal_by_id(deal_id)
    if not deal: 
        raise HTTPException(status_code=404, detail="Deal not found")
    contact = await cont_repo.get_contact_by_id(deal.contact_id)
    if not contact:
        raise HTTPException(status_code=400, detail="Error, contact not found")
    if user.organization_id != contact.organization_id:
        raise HTTPException(status_code=400, detail="Not allowed")
    await repo.patch_deal(deal, updates)
    keys = await redis_client.keys(f"deals:{contact.organization_id}:*")
    if keys:
        await redis_client.delete(*keys)
    return deal 


@router.delete("/deal/{deal_id}")
async def delete_deal(
    deal_id: int,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    repo = DealRepo(session)
    cont_repo = ContactRepo(session)
    deal = await repo.get_deal_by_id(deal_id)
    if not deal:
        raise HTTPException(status_code=404, detail="Deal not found")
    contact = await cont_repo.get_contact_by_id(deal.contact_id)
    if not contact:
        raise HTTPException(status_code=400, detail="Error, contact not found")
    if contact.organization_id != user.organization_id:
        raise HTTPException(status_code=400, detail="Not allowed")
    await repo.delete_deal(deal_id)
    keys = await redis_client.keys(f"deals:{contact.organization_id}:*")
    if keys:
        await redis_client.delete(*keys)
    return 


    