from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Dict, Any
from datetime import datetime, timedelta

from app.db.session import get_db
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.models.document import Document
from app.models.conversation import Conversation, Message
from app.models.usage_metrics import UsageMetrics
from app.api.v1.dependencies.auth import require_role

router = APIRouter()


@router.get("/analytics/overview")
async def get_analytics_overview(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    total_orgs = await db.scalar(select(func.count(Organization.id)))
    total_users = await db.scalar(select(func.count(User.id)))
    total_docs = await db.scalar(select(func.count(Document.id)))
    total_conversations = await db.scalar(select(func.count(Conversation.id)))
    
    return {
        "total_organizations": total_orgs,
        "total_users": total_users,
        "total_documents": total_docs,
        "total_conversations": total_conversations
    }


@router.get("/analytics/organizations")
async def get_organization_analytics(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Organization)
        .order_by(desc(Organization.created_at))
        .offset(skip)
        .limit(limit)
    )
    organizations = result.scalars().all()
    
    org_stats = []
    for org in organizations:
        user_count = await db.scalar(
            select(func.count(User.id)).where(User.organization_id == org.id)
        )
        doc_count = await db.scalar(
            select(func.count(Document.id)).where(Document.organization_id == org.id)
        )
        conv_count = await db.scalar(
            select(func.count(Conversation.id)).where(Conversation.organization_id == org.id)
        )
        
        org_stats.append({
            "id": org.id,
            "name": org.name,
            "tier": org.tier,
            "is_active": org.is_active,
            "users": user_count,
            "documents": doc_count,
            "conversations": conv_count,
            "created_at": org.created_at
        })
    
    return org_stats


@router.get("/analytics/usage")
async def get_usage_analytics(
    days: int = 30,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    start_date = datetime.utcnow() - timedelta(days=days)
    
    result = await db.execute(
        select(UsageMetrics)
        .where(UsageMetrics.date >= start_date)
        .order_by(UsageMetrics.date)
    )
    metrics = result.scalars().all()
    
    daily_stats = {}
    for metric in metrics:
        date_str = metric.date.strftime("%Y-%m-%d")
        if date_str not in daily_stats:
            daily_stats[date_str] = {
                "date": date_str,
                "api_calls": 0,
                "documents_uploaded": 0,
                "chat_messages": 0,
                "total_cost": 0.0
            }
        
        daily_stats[date_str]["api_calls"] += metric.api_calls
        daily_stats[date_str]["documents_uploaded"] += metric.documents_uploaded
        daily_stats[date_str]["chat_messages"] += metric.chat_messages
        daily_stats[date_str]["total_cost"] += metric.total_cost
    
    return list(daily_stats.values())


@router.get("/users")
async def list_all_users(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(User)
        .order_by(desc(User.created_at))
        .offset(skip)
        .limit(limit)
    )
    users = result.scalars().all()
    return users


@router.put("/users/{user_id}/activate")
async def activate_user(
    user_id: str,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = True
    await db.commit()
    await db.refresh(user)
    
    return {"message": "User activated", "user": user}


@router.put("/users/{user_id}/deactivate")
async def deactivate_user(
    user_id: str,
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    user.is_active = False
    await db.commit()
    await db.refresh(user)
    
    return {"message": "User deactivated", "user": user}


@router.get("/documents/stats")
async def get_document_stats(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: AsyncSession = Depends(get_db)
):
    total_docs = await db.scalar(select(func.count(Document.id)))
    
    status_counts = await db.execute(
        select(Document.status, func.count(Document.id))
        .group_by(Document.status)
    )
    
    status_breakdown = {status: count for status, count in status_counts}
    
    total_size = await db.scalar(select(func.sum(Document.file_size))) or 0
    
    return {
        "total_documents": total_docs,
        "status_breakdown": status_breakdown,
        "total_size_bytes": total_size,
        "total_size_mb": round(total_size / (1024 * 1024), 2)
    }


