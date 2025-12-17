import pytest
from httpx import AsyncClient
from io import BytesIO


@pytest.mark.asyncio
async def test_list_documents(client: AsyncClient, auth_headers):
    response = await client.get(
        "/api/v1/documents/",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_create_document(client: AsyncClient, auth_headers, db_session):
    response = await client.post(
        "/api/v1/documents/",
        headers=auth_headers,
        json={
            "filename": "test.pdf",
            "title": "Test Document",
            "description": "A test document"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "test.pdf"
    assert data["title"] == "Test Document"
    assert data["status"] == "uploading"


@pytest.mark.asyncio
async def test_get_document(client: AsyncClient, auth_headers, db_session, test_user):
    from app.models.document import Document
    import uuid
    
    doc = Document(
        id=str(uuid.uuid4()),
        organization_id=test_user.organization_id,
        uploaded_by=test_user.id,
        filename="test.pdf",
        title="Test Doc",
        status="completed"
    )
    db_session.add(doc)
    await db_session.commit()
    
    response = await client.get(
        f"/api/v1/documents/{doc.id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == doc.id
    assert data["filename"] == "test.pdf"


@pytest.mark.asyncio
async def test_update_document(client: AsyncClient, auth_headers, db_session, test_user):
    from app.models.document import Document
    import uuid
    
    doc = Document(
        id=str(uuid.uuid4()),
        organization_id=test_user.organization_id,
        uploaded_by=test_user.id,
        filename="test.pdf",
        title="Original Title",
        status="completed"
    )
    db_session.add(doc)
    await db_session.commit()
    
    response = await client.put(
        f"/api/v1/documents/{doc.id}",
        headers=auth_headers,
        json={"title": "Updated Title"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"


@pytest.mark.asyncio
async def test_delete_document(client: AsyncClient, auth_headers, db_session, test_user):
    from app.models.document import Document
    import uuid
    
    doc = Document(
        id=str(uuid.uuid4()),
        organization_id=test_user.organization_id,
        uploaded_by=test_user.id,
        filename="test.pdf",
        status="completed"
    )
    db_session.add(doc)
    await db_session.commit()
    
    response = await client.delete(
        f"/api/v1/documents/{doc.id}",
        headers=auth_headers
    )
    assert response.status_code == 204


