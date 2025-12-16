from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import redis.asyncio as redis
from app.core.config import settings
import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_client: redis.Redis):
        super().__init__(app)
        self.redis = redis_client
    
    async def dispatch(self, request: Request, call_next: Callable):
        if request.url.path.startswith("/api/"):
            client_ip = request.client.host
            user_id = getattr(request.state, "user_id", None)
            
            key = f"rate_limit:{user_id or client_ip}"
            
            try:
                current = await self.redis.get(key)
                
                if current and int(current) >= settings.RATE_LIMIT_PER_MINUTE:
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded"
                    )
                
                pipe = self.redis.pipeline()
                pipe.incr(key)
                pipe.expire(key, 60)
                await pipe.execute()
                
            except redis.RedisError:
                pass
        
        response = await call_next(request)
        return response

