from sqlalchemy import Column, String, DateTime, ForeignKey, Text, JSON, Boolean, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(String, primary_key=True, default=generate_uuid)
    organization_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    title = Column(String(500))
    is_archived = Column(Boolean, default=False)
    
    conv_metadata = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    organization = relationship("Organization", back_populates="conversations")
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan", order_by="Message.created_at")


class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=generate_uuid)
    conversation_id = Column(String, ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    
    sources = Column(JSON, default=list)
    
    msg_metadata = Column(JSON, default=dict)
    tokens_used = Column(Integer)
    cost = Column(Integer)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    conversation = relationship("Conversation", back_populates="messages")

