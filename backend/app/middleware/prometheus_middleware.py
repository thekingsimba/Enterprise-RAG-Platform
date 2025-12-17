from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
from app.api.v1.endpoints.metrics import (
    http_requests_total,
    http_request_duration_seconds
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        
        method = request.method
        endpoint = request.url.path
        status = response.status_code
        
        http_requests_total.labels(
            method=method,
            endpoint=endpoint,
            status=status
        ).inc()
        
        http_request_duration_seconds.labels(
            method=method,
            endpoint=endpoint
        ).observe(duration)
        
        return response

