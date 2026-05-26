from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.contact import ContactRepo
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.auth import get_current_user
from app.models.user import User
from app.redis_client import redis_client
import json

router = APIRouter()

@router.post("/contact", response_model=ContactResponse, status_code=201)
async def create_contact(
    data: ContactCreate,
    session: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user)
):
    repo = ContactRepo(session)
    email_exsists = await repo.get_contact_by_email(data.email)
    if email_exsists:
        raise HTTPException(status_code=400, detail="Contact already exsists")
    phone_exsists = await repo.get_contact_by_phone(data.phone)
    if phone_exsists:
        raise HTTPException(status_code=400, detail="Contact already exists")
    if user.organization_id != data.organization_id:
        raise HTTPException(status_code=400, detail="Not allowed")
    contact = await repo.create_contact(data.organization_id, data.name, data.email, data.phone)
    keys = await redis_client.keys(f"contacts:{data.organization_id}:*")
    await redis_client.delete(*keys)
    return contact

@router.get("/contact/organization/{organization_id}")
async def get_all_organization_contact(
    organization_id: int,
    limit: int = 10,
    offset: int = 0,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    cache_key = f"contacts:{organization_id}:{limit}:{offset}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    repo = ContactRepo(session)
    if user.organization_id != organization_id:
        raise HTTPException(status_code=400, detail="Not allowed")
    result = await repo.get_contacts_by_organization_id(organization_id, limit, offset)
    await redis_client.set(cache_key, json.dumps([{"id": t.id, "organization_id": t.organization_id,"name": t.name,"phone": t.phone, "created_at": str(t.created_at) } for t in result]), ex=300)
    return result 

@router.get('/contact/{contact_id}')
async def get_contact_by_id(
    contact_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    cache_key = f"contact:{contact_id}"
    cached = await redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    repo = ContactRepo(session)
    contact = await repo.get_contact_by_id(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    if user.organization_id != contact.organization_id:
        raise HTTPException(status_code=400, detail="Not allowed")
    await redis_client.set(cache_key, json.dumps({"id": contact.id, "organization_id": contact.organization_id,"name": contact.name,"phone": contact.phone, "created_at": str(contact.created_at)}), ex=300)
    return contact
    