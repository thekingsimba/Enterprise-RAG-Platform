import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_conversation(client: AsyncClient, auth_headers):
    response = await client.post(
        "/api/v1/chat/conversations",
        headers=auth_headers,
        json={"title": "Test Conversation"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Conversation"
    assert "id" in data


@pytest.mark.asyncio
async def test_list_conversations(client: AsyncClient, auth_headers):
    response = await client.get(
        "/api/v1/chat/conversations",
        headers=auth_headers
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_conversation(client: AsyncClient, auth_headers, db_session, test_user):
    from app.models.conversation import Conversation
    import uuid
    
    conv = Conversation(
        id=str(uuid.uuid4()),
        organization_id=test_user.organization_id,
        user_id=test_user.id,
        title="Test Conv"
    )
    db_session.add(conv)
    await db_session.commit()
    
    response = await client.get(
        f"/api/v1/chat/conversations/{conv.id}",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == conv.id
    assert data["title"] == "Test Conv"


@pytest.mark.asyncio
async def test_update_conversation(client: AsyncClient, auth_headers, db_session, test_user):
    from app.models.conversation import Conversation
    import uuid
    
    conv = Conversation(
        id=str(uuid.uuid4()),
        organization_id=test_user.organization_id,
        user_id=test_user.id,
        title="Original"
    )
    db_session.add(conv)
    await db_session.commit()
    
    response = await client.put(
        f"/api/v1/chat/conversations/{conv.id}",
        headers=auth_headers,
        json={"title": "Updated"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"


@pytest.mark.asyncio
async def test_delete_conversation(client: AsyncClient, auth_headers, db_session, test_user):
    from app.models.conversation import Conversation
    import uuid
    
    conv = Conversation(
        id=str(uuid.uuid4()),
        organization_id=test_user.organization_id,
        user_id=test_user.id,
        title="To Delete"
    )
    db_session.add(conv)
    await db_session.commit()
    
    response = await client.delete(
        f"/api/v1/chat/conversations/{conv.id}",
        headers=auth_headers
    )
    assert response.status_code == 204


