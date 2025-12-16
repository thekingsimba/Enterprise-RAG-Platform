from celery import Celery
from app.core.config import settings
from app.services.document_service import DocumentService
from app.db.session import AsyncSessionLocal
import asyncio

celery_app = Celery(
    "rag_platform",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)


@celery_app.task(name="process_document")
def process_document_task(document_id: str, file_path: str):
    async def _process():
        async with AsyncSessionLocal() as db:
            document_service = DocumentService()
            return await document_service.process_document(document_id, file_path, db)
    
    return asyncio.run(_process())

