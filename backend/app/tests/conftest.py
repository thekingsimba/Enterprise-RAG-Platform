import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient

from app.main import app
from app.db.session import Base, get_db
from app.core.config import settings

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost:5432/rag_platform_test"

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    async with TestingSessionLocal() as session:
        yield session
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
async def test_user(db_session: AsyncSession):
    from app.models.user import User
    from app.models.organization import Organization
    from app.core.security import get_password_hash
    import uuid
    
    org = Organization(
        id=str(uuid.uuid4()),
        name="Test Organization",
        slug="test-org",
        tier="free"
    )
    db_session.add(org)
    await db_session.flush()
    
    user = User(
        id=str(uuid.uuid4()),
        email="test@example.com",
        hashed_password=get_password_hash("testpassword123"),
        full_name="Test User",
        organization_id=org.id,
        role="admin",
        is_active=True
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    return user


@pytest.fixture
async def auth_headers(client: AsyncClient, test_user):
    from app.core.security import create_access_token
    
    token = create_access_token(data={"sub": test_user.id})
    return {"Authorization": f"Bearer {token}"}


