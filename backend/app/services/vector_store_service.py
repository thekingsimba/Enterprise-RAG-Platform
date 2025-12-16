from typing import List, Dict, Any, Optional
from pinecone import Pinecone, ServerlessSpec
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class VectorStoreService:
    def __init__(self):
        self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index_name = settings.PINECONE_INDEX_NAME
        self._ensure_index_exists()
        self.index = self.pc.Index(self.index_name)
    
    def _ensure_index_exists(self):
        try:
            existing_indexes = [index.name for index in self.pc.list_indexes()]
            
            if self.index_name not in existing_indexes:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=settings.EMBEDDING_DIMENSIONS,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region=settings.AWS_REGION
                    )
                )
                logger.info(f"Created Pinecone index: {self.index_name}")
        except Exception as e:
            logger.error(f"Error ensuring index exists: {e}")
    
    def upsert_vectors(
        self,
        vectors: List[tuple],
        namespace: str
    ) -> bool:
        try:
            self.index.upsert(vectors=vectors, namespace=namespace)
            return True
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            return False
    
    def query_vectors(
        self,
        query_vector: List[float],
        namespace: str,
        top_k: int = 5,
        filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        try:
            results = self.index.query(
                vector=query_vector,
                namespace=namespace,
                top_k=top_k,
                filter=filter,
                include_metadata=True
            )
            return results.matches
        except Exception as e:
            logger.error(f"Error querying vectors: {e}")
            return []
    
    def delete_vectors(
        self,
        ids: List[str],
        namespace: str
    ) -> bool:
        try:
            self.index.delete(ids=ids, namespace=namespace)
            return True
        except Exception as e:
            logger.error(f"Error deleting vectors: {e}")
            return False
    
    def delete_namespace(self, namespace: str) -> bool:
        try:
            self.index.delete(delete_all=True, namespace=namespace)
            return True
        except Exception as e:
            logger.error(f"Error deleting namespace: {e}")
            return False

