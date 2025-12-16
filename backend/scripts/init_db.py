import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.db.session import AsyncSessionLocal
from app.db.init_db import init_db


async def main():
    print("Initializing database...")
    async with AsyncSessionLocal() as db:
        await init_db(db)
    print("Database initialization complete!")


if __name__ == "__main__":
    asyncio.run(main())

