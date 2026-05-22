from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import deal, auth, contact, organization
from app.database import engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()
    
app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(deal.router)
app.include_router(contact.router)
app.include_router(organization.router)