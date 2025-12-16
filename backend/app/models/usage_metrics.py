from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.sql import func
from app.db.session import Base
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class UsageMetrics(Base):
    __tablename__ = "usage_metrics"

    id = Column(String, primary_key=True, default=generate_uuid)
    organization_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    
    api_calls = Column(Integer, default=0)
    documents_uploaded = Column(Integer, default=0)
    embeddings_created = Column(Integer, default=0)
    chat_messages = Column(Integer, default=0)
    
    prompt_tokens = Column(Integer, default=0)
    completion_tokens = Column(Integer, default=0)
    total_tokens = Column(Integer, default=0)
    
    embedding_cost = Column(Float, default=0.0)
    llm_cost = Column(Float, default=0.0)
    storage_cost = Column(Float, default=0.0)
    total_cost = Column(Float, default=0.0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

