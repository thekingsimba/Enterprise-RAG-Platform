from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List
import os
import tempfile
from pathlib import Path

from app.db.session import get_db
from app.schemas.document import Document, DocumentCreate, DocumentUpdate
from app.models.document import Document as DocumentModel, DocumentStatus
from app.models.user import User
from app.models.organization import Organization
from app.api.v1.dependencies.auth import get_current_user, get_current_organization
from app.core.config import settings
from app.services.storage_service import StorageService
from app.services.usage_tracking_service import UsageTrackingService
from app.utils.file_validator import FileValidator
from app.worker import process_document_task
import uuid

router = APIRouter()


@router.get("/", response_model=List[Document])
async def list_documents(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DocumentModel)
        .where(DocumentModel.organization_id == organization.id)
        .order_by(desc(DocumentModel.created_at))
        .offset(skip)
        .limit(limit)
    )
    documents = result.scalars().all()
    return documents


@router.get("/{document_id}", response_model=Document)
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DocumentModel).where(
            DocumentModel.id == document_id,
            DocumentModel.organization_id == organization.id
        )
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document


@router.post("/", response_model=Document, status_code=status.HTTP_201_CREATED)
async def create_document(
    document_data: DocumentCreate,
    current_user: User = Depends(get_current_user),
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    document = DocumentModel(
        id=str(uuid.uuid4()),
        organization_id=organization.id,
        uploaded_by=current_user.id,
        filename=document_data.filename,
        title=document_data.title,
        description=document_data.description,
        tags=document_data.tags,
        status="uploading"
    )
    
    db.add(document)
    await db.commit()
    await db.refresh(document)
    
    return document


@router.put("/{document_id}", response_model=Document)
async def update_document(
    document_id: str,
    document_update: DocumentUpdate,
    current_user: User = Depends(get_current_user),
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DocumentModel).where(
            DocumentModel.id == document_id,
            DocumentModel.organization_id == organization.id
        )
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if document_update.title is not None:
        document.title = document_update.title
    if document_update.description is not None:
        document.description = document_update.description
    if document_update.tags is not None:
        document.tags = document_update.tags
    
    await db.commit()
    await db.refresh(document)
    
    return document


@router.post("/upload", response_model=Document, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    title: str = None,
    description: str = None,
    current_user: User = Depends(get_current_user),
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    file_extension = Path(file.filename).suffix.lower()
    
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type {file_extension} not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
        )
    
    if organization.current_documents >= organization.max_documents:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Document quota exceeded"
        )
    
    file_content = await file.read()
    file_size = len(file_content)
    
    is_valid, validation_message = FileValidator.validate_file(
        file_content, file.filename, settings.MAX_FILE_SIZE
    )
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=validation_message
        )
    
    document = DocumentModel(
        id=str(uuid.uuid4()),
        organization_id=organization.id,
        uploaded_by=current_user.id,
        filename=file.filename,
        file_type=file_extension,
        file_size=file_size,
        title=title or file.filename,
        description=description,
        status=DocumentStatus.UPLOADING
    )
    
    db.add(document)
    await db.commit()
    await db.refresh(document)
    
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
            tmp_file.write(file_content)
            tmp_file_path = tmp_file.name
        
        storage_service = StorageService()
        s3_key = f"{organization.id}/{document.id}/{file.filename}"
        
        if storage_service.upload_file(tmp_file_path, s3_key):
            document.s3_key = s3_key
            document.status = DocumentStatus.PROCESSING
            await db.commit()
            
            process_document_task.delay(document.id, tmp_file_path)
            
            organization.current_documents += 1
            organization.current_storage_mb += file_size / (1024 * 1024)
            await db.commit()
            
            await UsageTrackingService.track_document_upload(db, organization.id)
        else:
            document.status = DocumentStatus.FAILED
            document.error_message = "Failed to upload to S3"
            await db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload document"
            )
    
    except Exception as e:
        document.status = DocumentStatus.FAILED
        document.error_message = str(e)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )
    finally:
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
    
    await db.refresh(document)
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(DocumentModel).where(
            DocumentModel.id == document_id,
            DocumentModel.organization_id == organization.id
        )
    )
    document = result.scalar_one_or_none()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    from app.services.document_service import DocumentService
    doc_service = DocumentService()
    await doc_service.delete_document_vectors(document, db)
    
    organization.current_documents -= 1
    if document.file_size:
        organization.current_storage_mb -= document.file_size / (1024 * 1024)
    
    await db.delete(document)
    await db.commit()

