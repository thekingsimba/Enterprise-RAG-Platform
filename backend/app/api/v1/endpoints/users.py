from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.schemas.user import User, UserUpdate
from app.models.user import User as UserModel
from app.api.v1.dependencies.auth import get_current_user, require_role, get_current_organization
from app.models.user import UserRole
from app.models.organization import Organization

router = APIRouter()


@router.get("/me", response_model=User)
async def get_current_user_info(
    current_user: UserModel = Depends(get_current_user)
):
    return current_user


@router.put("/me", response_model=User)
async def update_current_user(
    user_update: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    
    await db.commit()
    await db.refresh(current_user)
    
    return current_user


@router.get("/", response_model=List[User])
async def list_organization_users(
    current_user: UserModel = Depends(require_role(UserRole.ADMIN)),
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserModel).where(UserModel.organization_id == organization.id)
    )
    users = result.scalars().all()
    return users


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: UserModel = Depends(require_role(UserRole.ADMIN)),
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(UserModel).where(
            UserModel.id == user_id,
            UserModel.organization_id == organization.id
        )
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user_update.full_name is not None:
        user.full_name = user_update.full_name
    if user_update.role is not None:
        user.role = user_update.role
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    
    await db.commit()
    await db.refresh(user)
    
    return user

