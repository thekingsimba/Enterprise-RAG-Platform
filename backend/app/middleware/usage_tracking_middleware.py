from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.db.session import AsyncSessionLocal
from app.services.usage_tracking_service import UsageTrackingService
import logging

logger = logging.getLogger(__name__)


class UsageTrackingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        response = await call_next(request)
        
        if request.url.path.startswith("/api/v1/") and hasattr(request.state, "organization_id"):
            try:
                async with AsyncSessionLocal() as db:
                    await UsageTrackingService.track_api_call(
                        db, request.state.organization_id
                    )
            except Exception as e:
                logger.error(f"Error tracking API call: {e}")
        
        return response

