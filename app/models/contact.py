from sqlalchemy import Column, ForeignKey, String, Integer, TIMESTAMP
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
from app.models.base import Base

class Contact(Base):
    
    __tablename__ = "contact"
    
    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey("organization.id"), nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    organization = relationship("Organization", back_populates="contacts")
    deals = relationship("Deal", back_populates="contact")
    