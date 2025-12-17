from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, date
from app.models.usage_metrics import UsageMetrics
import uuid
import logging

logger = logging.getLogger(__name__)


class UsageTrackingService:
    @staticmethod
    async def track_api_call(
        db: AsyncSession,
        organization_id: str
    ):
        await UsageTrackingService._increment_metric(
            db, organization_id, "api_calls", 1
        )
    
    @staticmethod
    async def track_document_upload(
        db: AsyncSession,
        organization_id: str
    ):
        await UsageTrackingService._increment_metric(
            db, organization_id, "documents_uploaded", 1
        )
    
    @staticmethod
    async def track_embeddings(
        db: AsyncSession,
        organization_id: str,
        count: int,
        cost: float
    ):
        await UsageTrackingService._increment_metric(
            db, organization_id, "embeddings_created", count
        )
        await UsageTrackingService._increment_metric(
            db, organization_id, "embedding_cost", cost
        )
        await UsageTrackingService._increment_metric(
            db, organization_id, "total_cost", cost
        )
    
    @staticmethod
    async def track_chat_message(
        db: AsyncSession,
        organization_id: str,
        prompt_tokens: int,
        completion_tokens: int,
        cost: float
    ):
        await UsageTrackingService._increment_metric(
            db, organization_id, "chat_messages", 1
        )
        await UsageTrackingService._increment_metric(
            db, organization_id, "prompt_tokens", prompt_tokens
        )
        await UsageTrackingService._increment_metric(
            db, organization_id, "completion_tokens", completion_tokens
        )
        await UsageTrackingService._increment_metric(
            db, organization_id, "total_tokens", prompt_tokens + completion_tokens
        )
        await UsageTrackingService._increment_metric(
            db, organization_id, "llm_cost", cost
        )
        await UsageTrackingService._increment_metric(
            db, organization_id, "total_cost", cost
        )
    
    @staticmethod
    async def _increment_metric(
        db: AsyncSession,
        organization_id: str,
        metric_name: str,
        value: float
    ):
        try:
            today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
            
            result = await db.execute(
                select(UsageMetrics).where(
                    UsageMetrics.organization_id == organization_id,
                    UsageMetrics.date == today
                )
            )
            metric = result.scalar_one_or_none()
            
            if not metric:
                metric = UsageMetrics(
                    id=str(uuid.uuid4()),
                    organization_id=organization_id,
                    date=today
                )
                db.add(metric)
                await db.flush()
            
            current_value = getattr(metric, metric_name, 0) or 0
            setattr(metric, metric_name, current_value + value)
            
            await db.commit()
            
        except Exception as e:
            logger.error(f"Error tracking metric {metric_name}: {e}")
            await db.rollback()
    
    @staticmethod
    def calculate_embedding_cost(num_tokens: int, model: str = "text-embedding-3-small") -> float:
        if model == "text-embedding-3-small":
            return (num_tokens / 1_000_000) * 0.02
        elif model == "text-embedding-3-large":
            return (num_tokens / 1_000_000) * 0.13
        return 0.0
    
    @staticmethod
    def calculate_llm_cost(
        prompt_tokens: int,
        completion_tokens: int,
        model: str = "gpt-4-turbo-preview"
    ) -> float:
        if model == "gpt-4-turbo-preview":
            prompt_cost = (prompt_tokens / 1_000_000) * 10.00
            completion_cost = (completion_tokens / 1_000_000) * 30.00
            return prompt_cost + completion_cost
        elif model == "gpt-3.5-turbo":
            prompt_cost = (prompt_tokens / 1_000_000) * 0.50
            completion_cost = (completion_tokens / 1_000_000) * 1.50
            return prompt_cost + completion_cost
        return 0.0

