from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.core.security import get_password_hash
import uuid
import logging

logger = logging.getLogger(__name__)


async def init_db(db: AsyncSession) -> None:
    result = await db.execute(select(User).limit(1))
    if result.scalar_one_or_none():
        logger.info("Database already initialized")
        return
    
    logger.info("Initializing database with default data...")
    
    default_org = Organization(
        id=str(uuid.uuid4()),
        name="Default Organization",
        slug="default",
        tier="enterprise",
        max_documents=1000,
        max_storage_mb=10000,
        max_users=50
    )
    db.add(default_org)
    await db.flush()
    
    admin_user = User(
        id=str(uuid.uuid4()),
        email="admin@example.com",
        hashed_password=get_password_hash("admin123"),
        full_name="Admin User",
        organization_id=default_org.id,
        role=UserRole.ADMIN,
        is_active=True,
        is_verified=True
    )
    db.add(admin_user)
    
    await db.commit()
    logger.info("Database initialized successfully")
    logger.info("Admin user created: admin@example.com / admin123")


