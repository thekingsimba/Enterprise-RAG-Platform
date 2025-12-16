from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum
import uuid


def generate_uuid():
    return str(uuid.uuid4())


class DocumentStatus(str, enum.Enum):
    UPLOADING = "uploading"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Document(Base):
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=generate_uuid)
    organization_id = Column(String, ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True)
    uploaded_by = Column(String, ForeignKey("users.id", ondelete="SET NULL"))
    
    filename = Column(String(500), nullable=False)
    file_type = Column(String(50))
    file_size = Column(Integer)
    s3_key = Column(String(1000))
    
    status = Column(SQLEnum(DocumentStatus), default=DocumentStatus.UPLOADING, index=True)
    num_chunks = Column(Integer, default=0)
    num_pages = Column(Integer)
    
    title = Column(String(500))
    description = Column(Text)
    tags = Column(JSON, default=list)
    metadata = Column(JSON, default=dict)
    
    error_message = Column(Text)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    processed_at = Column(DateTime(timezone=True))
    
    organization = relationship("Organization", back_populates="documents")
    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(String, primary_key=True, default=generate_uuid)
    document_id = Column(String, ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    
    content = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)
    
    vector_id = Column(String(100))
    
    page_number = Column(Integer)
    start_char = Column(Integer)
    end_char = Column(Integer)
    metadata = Column(JSON, default=dict)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    document = relationship("Document", back_populates="chunks")

