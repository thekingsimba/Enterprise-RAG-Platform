from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
import os
import tempfile

from app.models.document import Document, DocumentChunk, DocumentStatus
from app.services.storage_service import StorageService
from app.services.embedding_service import EmbeddingService
from app.services.vector_store_service import VectorStoreService
from app.utils.document_parser import DocumentParser
from app.utils.chunking import TextChunker
import logging

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self):
        self.storage_service = StorageService()
        self.embedding_service = EmbeddingService()
        self.vector_store_service = VectorStoreService()
        self.document_parser = DocumentParser()
        self.text_chunker = TextChunker()
    
    async def process_document(
        self,
        document_id: str,
        file_path: str,
        db: AsyncSession
    ) -> bool:
        try:
            result = await db.execute(
                select(Document).where(Document.id == document_id)
            )
            document = result.scalar_one_or_none()
            
            if not document:
                logger.error(f"Document {document_id} not found")
                return False
            
            document.status = DocumentStatus.PROCESSING
            await db.commit()
            
            parsed_data = self.document_parser.parse_file(file_path)
            
            document.num_pages = parsed_data.get("num_pages")
            await db.commit()
            
            chunks = self.text_chunker.chunk_text(
                parsed_data["text"],
                metadata={
                    "document_id": document_id,
                    "filename": document.filename
                }
            )
            
            chunk_texts = [chunk["content"] for chunk in chunks]
            embeddings = self.embedding_service.create_embeddings_batch(chunk_texts)
            
            vectors = []
            for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
                chunk_id = str(uuid.uuid4())
                
                chunk_model = DocumentChunk(
                    id=chunk_id,
                    document_id=document_id,
                    content=chunk["content"],
                    chunk_index=idx,
                    vector_id=chunk_id,
                    metadata=chunk["metadata"]
                )
                db.add(chunk_model)
                
                vectors.append((
                    chunk_id,
                    embedding,
                    {
                        "document_id": document_id,
                        "chunk_index": idx,
                        "organization_id": document.organization_id
                    }
                ))
            
            namespace = f"org_{document.organization_id}"
            self.vector_store_service.upsert_vectors(vectors, namespace)
            
            document.num_chunks = len(chunks)
            document.status = DocumentStatus.COMPLETED
            await db.commit()
            
            logger.info(f"Successfully processed document {document_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error processing document {document_id}: {e}")
            
            result = await db.execute(
                select(Document).where(Document.id == document_id)
            )
            document = result.scalar_one_or_none()
            if document:
                document.status = DocumentStatus.FAILED
                document.error_message = str(e)
                await db.commit()
            
            return False
    
    async def delete_document_vectors(
        self,
        document: Document,
        db: AsyncSession
    ) -> bool:
        try:
            result = await db.execute(
                select(DocumentChunk).where(DocumentChunk.document_id == document.id)
            )
            chunks = result.scalars().all()
            
            vector_ids = [chunk.vector_id for chunk in chunks if chunk.vector_id]
            
            if vector_ids:
                namespace = f"org_{document.organization_id}"
                self.vector_store_service.delete_vectors(vector_ids, namespace)
            
            if document.s3_key:
                self.storage_service.delete_file(document.s3_key)
            
            return True
            
        except Exception as e:
            logger.error(f"Error deleting document vectors: {e}")
            return False

