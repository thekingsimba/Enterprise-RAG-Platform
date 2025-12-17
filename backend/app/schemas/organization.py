from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class OrganizationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255)


class OrganizationCreate(OrganizationBase):
    tier: str = "free"


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    tier: Optional[str] = None
    max_documents: Optional[int] = None
    max_storage_mb: Optional[int] = None
    max_users: Optional[int] = None
    settings: Optional[Dict[str, Any]] = None


class OrganizationInDB(OrganizationBase):
    id: str
    tier: str
    is_active: bool
    max_documents: int
    max_storage_mb: int
    max_users: int
    current_documents: int
    current_storage_mb: int
    current_users: int
    org_settings: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Organization(OrganizationInDB):
    pass

