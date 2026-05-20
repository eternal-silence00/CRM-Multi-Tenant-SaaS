from pydantic import BaseModel, ConfigDict

class ContactCreate(BaseModel):
    organization_id: int
    name: str
    email: str
    phone: str
    
class ContactResponse(BaseModel):
    id: int
    organization_id: int
    name: str
    email: str
    phone: str
    
    model_config = ConfigDict(from_attributes=True)