from sqlalchemy import Column, ForeignKey, String, Integer
from app.models.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    
    organization = relationship("Organization", back_populates="users")