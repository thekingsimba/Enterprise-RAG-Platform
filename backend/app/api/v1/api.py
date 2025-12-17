from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, documents, chat, organizations, admin, metrics

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
api_router.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(metrics.router, tags=["metrics"])

