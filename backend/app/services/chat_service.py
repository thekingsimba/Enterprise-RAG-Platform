from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.conversation import Conversation, Message
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.services.llm_service import LLMService
import logging

logger = logging.getLogger(__name__)


class ChatService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()
        self.llm_service = LLMService()
    
    async def retrieve_context(
        self,
        query: str,
        organization_id: str,
        top_k: int = 5
    ) -> tuple[str, List[Dict[str, Any]]]:
        try:
            query_embedding = self.embedding_service.create_embedding(query)
            
            namespace = f"org_{organization_id}"
            results = self.vector_store_service.query_vectors(
                query_vector=query_embedding,
                namespace=namespace,
                top_k=top_k
            )
            
            context_parts = []
            sources = []
            
            for idx, match in enumerate(results):
                metadata = match.metadata
                score = match.score
                
                content = metadata.get("content", match.id)
                filename = metadata.get("filename", "Unknown")
                
                context_parts.append(
                    f"[Document {idx + 1}]\n"
                    f"Source: {filename}\n"
                    f"Content: {content}\n"
                    f"Relevance: {score:.2f}\n"
                )
                
                sources.append({
                    "chunk_id": match.id,
                    "document_id": metadata.get("document_id"),
                    "filename": filename,
                    "score": float(score),
                    "content": content[:200],
                    "page_number": metadata.get("page_number")
                })
            
            context = "\n\n".join(context_parts)
            
            return context, sources
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return "", []
    
    async def get_chat_history(
        self,
        conversation_id: str,
        db: AsyncSession,
        limit: int = 10
    ) -> List[Dict[str, str]]:
        try:
            result = await db.execute(
                select(Message)
                .where(Message.conversation_id == conversation_id)
                .order_by(Message.created_at.desc())
                .limit(limit)
            )
            messages = result.scalars().all()
            
            history = []
            for msg in reversed(messages):
                history.append({
                    "role": msg.role,
                    "content": msg.content
                })
            
            return history
            
        except Exception as e:
            logger.error(f"Error getting chat history: {e}")
            return []
    
    async def generate_answer(
        self,
        query: str,
        organization_id: str,
        conversation_id: Optional[str] = None,
        db: Optional[AsyncSession] = None
    ) -> tuple[str, List[Dict[str, Any]]]:
        try:
            context, sources = await self.retrieve_context(
                query=query,
                organization_id=organization_id,
                top_k=5
            )
            
            chat_history = []
            if conversation_id and db:
                chat_history = await self.get_chat_history(conversation_id, db)
            
            if not context:
                answer = "I couldn't find any relevant information in the knowledge base to answer your question."
            else:
                answer = await self.llm_service.generate_response(
                    query=query,
                    context=context,
                    chat_history=chat_history
                )
            
            return answer, sources
            
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise

