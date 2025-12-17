from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.document import DocumentStatus


class DocumentBase(BaseModel):
    filename: str
    title: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = []


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None


class DocumentInDB(DocumentBase):
    id: str
    organization_id: str
    uploaded_by: Optional[str] = None
    file_type: Optional[str] = None
    file_size: Optional[int] = None
    s3_key: Optional[str] = None
    status: DocumentStatus
    num_chunks: int
    num_pages: Optional[int] = None
    doc_metadata: Dict[str, Any]
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Document(DocumentInDB):
    pass


class DocumentUploadResponse(BaseModel):
    document_id: str
    upload_url: str
    fields: Dict[str, str]


class DocumentChunkBase(BaseModel):
    content: str
    chunk_index: int
    page_number: Optional[int] = None


class DocumentChunk(DocumentChunkBase):
    id: str
    document_id: str
    vector_id: Optional[str] = None
    chunk_metadata: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

