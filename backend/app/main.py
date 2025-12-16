from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import redis.asyncio as redis

from app.core.config import settings
from app.api.v1.api import api_router
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.rate_limiter import RateLimitMiddleware

redis_client = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global redis_client
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
    
    if settings.ENVIRONMENT == "development":
        from app.db.session import AsyncSessionLocal
        from app.db.init_db import init_db
        async with AsyncSessionLocal() as db:
            await init_db(db)
    
    yield
    await redis_client.close()


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)


@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(api_router, prefix=settings.API_V1_PREFIX)

