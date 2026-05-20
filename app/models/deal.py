from sqlalchemy import Column, String, Integer, Float, TIMESTAMP, ForeignKey
from datetime import datetime, timezone
from app.models.base import Base
from sqlalchemy.orm import relationship

class Deal(Base):
    
    __tablename__ = "deal"
    
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey("contact.id"), nullable=False)
    title = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False, default="New")
    created_at = Column(TIMESTAMP(timezone=True), default= lambda: datetime.now(timezone.utc))
    
    contact = relationship("Contact", back_populates="deals")