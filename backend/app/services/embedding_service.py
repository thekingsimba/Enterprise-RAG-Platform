from typing import List
from openai import OpenAI
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.EMBEDDING_MODEL
    
    def create_embedding(self, text: str) -> List[float]:
        try:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error creating embedding: {e}")
            raise
    
    def create_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Error creating batch embeddings: {e}")
            raise
    
    def get_embedding_dimension(self) -> int:
        return settings.EMBEDDING_DIMENSIONS

