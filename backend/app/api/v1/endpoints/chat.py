from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List

from app.db.session import get_db
from app.schemas.chat import (
    Conversation,
    ConversationCreate,
    ConversationUpdate,
    ChatRequest,
    ChatResponse,
    Message
)
from app.models.conversation import Conversation as ConversationModel, Message as MessageModel
from app.models.user import User
from app.models.organization import Organization
from app.api.v1.dependencies.auth import get_current_user, get_current_organization
import uuid

router = APIRouter()


@router.get("/conversations", response_model=List[Conversation])
async def list_conversations(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ConversationModel)
        .where(ConversationModel.user_id == current_user.id)
        .order_by(desc(ConversationModel.updated_at))
        .offset(skip)
        .limit(limit)
    )
    conversations = result.scalars().all()
    return conversations


@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ConversationModel).where(
            ConversationModel.id == conversation_id,
            ConversationModel.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    return conversation


@router.post("/conversations", response_model=Conversation, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    conversation_data: ConversationCreate,
    current_user: User = Depends(get_current_user),
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    conversation = ConversationModel(
        id=str(uuid.uuid4()),
        organization_id=organization.id,
        user_id=current_user.id,
        title=conversation_data.title
    )
    
    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)
    
    return conversation


@router.put("/conversations/{conversation_id}", response_model=Conversation)
async def update_conversation(
    conversation_id: str,
    conversation_update: ConversationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ConversationModel).where(
            ConversationModel.id == conversation_id,
            ConversationModel.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    if conversation_update.title is not None:
        conversation.title = conversation_update.title
    if conversation_update.is_archived is not None:
        conversation.is_archived = conversation_update.is_archived
    
    await db.commit()
    await db.refresh(conversation)
    
    return conversation


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ConversationModel).where(
            ConversationModel.id == conversation_id,
            ConversationModel.user_id == current_user.id
        )
    )
    conversation = result.scalar_one_or_none()
    
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )
    
    await db.delete(conversation)
    await db.commit()


@router.post("/chat", response_model=ChatResponse)
async def chat(
    chat_request: ChatRequest,
    current_user: User = Depends(get_current_user),
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    if chat_request.conversation_id:
        result = await db.execute(
            select(ConversationModel).where(
                ConversationModel.id == chat_request.conversation_id,
                ConversationModel.user_id == current_user.id
            )
        )
        conversation = result.scalar_one_or_none()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
    else:
        conversation = ConversationModel(
            id=str(uuid.uuid4()),
            organization_id=organization.id,
            user_id=current_user.id,
            title=chat_request.message[:50]
        )
        db.add(conversation)
        await db.flush()
    
    user_message = MessageModel(
        id=str(uuid.uuid4()),
        conversation_id=conversation.id,
        role="user",
        content=chat_request.message
    )
    db.add(user_message)
    
    assistant_message = MessageModel(
        id=str(uuid.uuid4()),
        conversation_id=conversation.id,
        role="assistant",
        content="This is a placeholder response. RAG implementation coming soon."
    )
    db.add(assistant_message)
    
    await db.commit()
    await db.refresh(assistant_message)
    
    return ChatResponse(
        conversation_id=conversation.id,
        message=assistant_message,
        sources=[]
    )

