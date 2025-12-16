from typing import List, Dict, Any, Optional, AsyncGenerator
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0.7,
            openai_api_key=settings.OPENAI_API_KEY,
            streaming=True
        )
    
    def format_messages(
        self,
        query: str,
        context: str,
        chat_history: List[Dict[str, str]] = None
    ) -> List:
        messages = [
            SystemMessage(content="""You are a helpful AI assistant with access to a knowledge base.
Answer questions based on the provided context. If you cannot find the answer in the context, say so clearly.
Always cite your sources by mentioning which documents or sections you're referencing.""")
        ]
        
        if chat_history:
            for msg in chat_history:
                if msg["role"] == "user":
                    messages.append(HumanMessage(content=msg["content"]))
                elif msg["role"] == "assistant":
                    messages.append(AIMessage(content=msg["content"]))
        
        context_message = f"""Context from knowledge base:
{context}

Question: {query}"""
        
        messages.append(HumanMessage(content=context_message))
        
        return messages
    
    async def generate_response(
        self,
        query: str,
        context: str,
        chat_history: List[Dict[str, str]] = None
    ) -> str:
        try:
            messages = self.format_messages(query, context, chat_history)
            response = await self.llm.ainvoke(messages)
            return response.content
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    async def generate_response_stream(
        self,
        query: str,
        context: str,
        chat_history: List[Dict[str, str]] = None
    ) -> AsyncGenerator[str, None]:
        try:
            messages = self.format_messages(query, context, chat_history)
            
            async for chunk in self.llm.astream(messages):
                if chunk.content:
                    yield chunk.content
        except Exception as e:
            logger.error(f"Error streaming response: {e}")
            raise

