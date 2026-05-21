from pydantic import BaseModel, ConfigDict
from typing import Optional

class DealCreate(BaseModel):
    contact_id: int
    title: str
    amount: float
    status: str
    
class DealResponse(BaseModel):
    id: int
    contact_id: int
    title: str
    amount: float 
    status: str
    
    model_config = ConfigDict(from_attributes=True)
    
class DealPatch(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    status: Optional[str] = None