from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class MessageBase(BaseModel):
    role: str
    content: str


class MessageCreate(BaseModel):
    content: str = Field(..., min_length=1)


class MessageInDB(MessageBase):
    id: str
    conversation_id: str
    sources: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    tokens_used: Optional[int] = None
    cost: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class Message(MessageInDB):
    pass


class ConversationBase(BaseModel):
    title: Optional[str] = None


class ConversationCreate(ConversationBase):
    pass


class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    is_archived: Optional[bool] = None


class ConversationInDB(ConversationBase):
    id: str
    organization_id: str
    user_id: str
    is_archived: bool
    metadata: Dict[str, Any]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Conversation(ConversationInDB):
    messages: List[Message] = []


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)
    conversation_id: Optional[str] = None
    stream: bool = False


class ChatResponse(BaseModel):
    conversation_id: str
    message: Message
    sources: List[Dict[str, Any]] = []

