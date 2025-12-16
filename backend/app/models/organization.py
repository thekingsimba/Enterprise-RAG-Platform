from sqlalchemy import Column, String, Boolean, DateTime, Integer, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    
    tier = Column(String(50), default="free")
    is_active = Column(Boolean, default=True)
    
    max_documents = Column(Integer, default=100)
    max_storage_mb = Column(Integer, default=1000)
    max_users = Column(Integer, default=5)
    
    current_documents = Column(Integer, default=0)
    current_storage_mb = Column(Integer, default=0)
    current_users = Column(Integer, default=0)
    
    settings = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="organization", cascade="all, delete-orphan")
    conversations = relationship("Conversation", back_populates="organization", cascade="all, delete-orphan")

