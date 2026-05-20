from sqlalchemy import Column, String, Integer, TIMESTAMP
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.models.base import Base

class Organization(Base):
    
    __tablename__ = "organization"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    contacts = relationship("Contact", back_populates="organization")
    users = relationship("User", back_populates="organization")