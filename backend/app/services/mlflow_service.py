import mlflow
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class MLflowService:
    def __init__(self):
        if settings.MLFLOW_TRACKING_URI:
            mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
            mlflow.set_experiment("rag-platform")
    
    def log_embedding_model(
        self,
        model_name: str,
        dimensions: int,
        performance_metrics: dict = None
    ):
        try:
            with mlflow.start_run(run_name=f"embedding_{model_name}"):
                mlflow.log_param("model_name", model_name)
                mlflow.log_param("dimensions", dimensions)
                
                if performance_metrics:
                    for key, value in performance_metrics.items():
                        mlflow.log_metric(key, value)
                
                logger.info(f"Logged embedding model: {model_name}")
        except Exception as e:
            logger.error(f"Error logging to MLflow: {e}")
    
    def log_rag_experiment(
        self,
        chunk_size: int,
        chunk_overlap: int,
        top_k: int,
        retrieval_accuracy: float = None,
        response_quality: float = None
    ):
        try:
            with mlflow.start_run(run_name="rag_experiment"):
                mlflow.log_param("chunk_size", chunk_size)
                mlflow.log_param("chunk_overlap", chunk_overlap)
                mlflow.log_param("top_k", top_k)
                
                if retrieval_accuracy:
                    mlflow.log_metric("retrieval_accuracy", retrieval_accuracy)
                if response_quality:
                    mlflow.log_metric("response_quality", response_quality)
                
                logger.info("Logged RAG experiment")
        except Exception as e:
            logger.error(f"Error logging RAG experiment: {e}")
    
    def log_llm_performance(
        self,
        model_name: str,
        avg_latency: float,
        avg_tokens: int,
        cost_per_query: float
    ):
        try:
            with mlflow.start_run(run_name=f"llm_{model_name}"):
                mlflow.log_param("model_name", model_name)
                mlflow.log_metric("avg_latency_seconds", avg_latency)
                mlflow.log_metric("avg_tokens", avg_tokens)
                mlflow.log_metric("cost_per_query", cost_per_query)
                
                logger.info(f"Logged LLM performance: {model_name}")
        except Exception as e:
            logger.error(f"Error logging LLM performance: {e}")


