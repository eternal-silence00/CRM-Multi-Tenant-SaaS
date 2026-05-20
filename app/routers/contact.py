from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.repositories.contact import ContactRepo
from app.schemas.contact import ContactCreate, ContactResponse
from app.services.auth import get_current_user
from app.models.user import User

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
    return contact

@router.get("/contact/organization/{organization_id}")
async def get_all_organization_contact(
    organization_id: int,
    limit: int = 10,
    offset: int = 0,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    repo = ContactRepo(session)
    if user.organization_id != organization_id:
        raise HTTPException(status_code=400, detail="Not allowed")
    result = await repo.get_contacts_by_organization_id(organization_id, limit, offset)
    return result 

@router.get('/contact/{contact_id}')
async def get_contact_by_id(
    contact_id: int,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db)
):
    repo = ContactRepo(session)
    contact = await repo.get_contact_by_id(contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    if user.organization_id != contact.organization_id:
        raise HTTPException(status_code=400, detail="Not allowed")
    return contact
    