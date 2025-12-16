from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from app.db.session import get_db
from app.schemas.user import UserCreate, UserLogin, User
from app.schemas.token import Token, RefreshTokenRequest
from app.schemas.organization import OrganizationCreate, Organization
from app.models.user import User as UserModel
from app.models.organization import Organization as OrganizationModel
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
import uuid

router = APIRouter()


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserModel).where(UserModel.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if user_data.organization_id:
        org_result = await db.execute(
            select(OrganizationModel).where(OrganizationModel.id == user_data.organization_id)
        )
        organization = org_result.scalar_one_or_none()
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Organization not found"
            )
    else:
        organization = OrganizationModel(
            id=str(uuid.uuid4()),
            name=f"{user_data.email}'s Organization",
            slug=user_data.email.split('@')[0] + '-' + str(uuid.uuid4())[:8],
            tier="free"
        )
        db.add(organization)
        await db.flush()
    
    user = UserModel(
        id=str(uuid.uuid4()),
        email=user_data.email,
        full_name=user_data.full_name,
        hashed_password=get_password_hash(user_data.password),
        organization_id=organization.id,
        role="admin" if not user_data.organization_id else "member"
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/login", response_model=Token)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(UserModel).where(UserModel.email == credentials.email))
    user = result.scalar_one_or_none()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    user.last_login = datetime.utcnow()
    await db.commit()
    
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: AsyncSession = Depends(get_db)
):
    payload = decode_token(refresh_data.refresh_token)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    access_token = create_access_token(data={"sub": user.id})
    new_refresh_token = create_refresh_token(data={"sub": user.id})
    
    return Token(access_token=access_token, refresh_token=new_refresh_token)

