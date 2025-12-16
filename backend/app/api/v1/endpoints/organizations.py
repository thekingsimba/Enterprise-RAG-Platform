from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.schemas.organization import Organization, OrganizationCreate, OrganizationUpdate
from app.models.organization import Organization as OrganizationModel
from app.models.user import User, UserRole
from app.api.v1.dependencies.auth import get_current_user, require_role
import uuid

router = APIRouter()


@router.get("/", response_model=List[Organization])
async def list_organizations(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(OrganizationModel)
        .offset(skip)
        .limit(limit)
    )
    organizations = result.scalars().all()
    return organizations


@router.get("/{organization_id}", response_model=Organization)
async def get_organization(
    organization_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(OrganizationModel).where(OrganizationModel.id == organization_id)
    )
    organization = result.scalar_one_or_none()
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    if current_user.role != UserRole.ADMIN and current_user.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return organization


@router.post("/", response_model=Organization, status_code=status.HTTP_201_CREATED)
async def create_organization(
    organization_data: OrganizationCreate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(OrganizationModel).where(OrganizationModel.slug == organization_data.slug)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Organization slug already exists"
        )
    
    organization = OrganizationModel(
        id=str(uuid.uuid4()),
        name=organization_data.name,
        slug=organization_data.slug,
        tier=organization_data.tier or "free"
    )
    
    db.add(organization)
    await db.commit()
    await db.refresh(organization)
    
    return organization


@router.put("/{organization_id}", response_model=Organization)
async def update_organization(
    organization_id: str,
    organization_update: OrganizationUpdate,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(OrganizationModel).where(OrganizationModel.id == organization_id)
    )
    organization = result.scalar_one_or_none()
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    if organization_update.name is not None:
        organization.name = organization_update.name
    if organization_update.tier is not None:
        organization.tier = organization_update.tier
    if organization_update.is_active is not None:
        organization.is_active = organization_update.is_active
    if organization_update.max_documents is not None:
        organization.max_documents = organization_update.max_documents
    if organization_update.max_storage_mb is not None:
        organization.max_storage_mb = organization_update.max_storage_mb
    if organization_update.max_users is not None:
        organization.max_users = organization_update.max_users
    
    await db.commit()
    await db.refresh(organization)
    
    return organization


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization_id: str,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(OrganizationModel).where(OrganizationModel.id == organization_id)
    )
    organization = result.scalar_one_or_none()
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found"
        )
    
    await db.delete(organization)
    await db.commit()

