# Enterprise RAG Platform - Backend

Production-grade RAG platform backend built with FastAPI, LangChain, and Pinecone.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL + SQLAlchemy
- **Cache**: Redis
- **Vector DB**: Pinecone
- **LLM**: OpenAI GPT-4
- **RAG**: LangChain + LangGraph
- **Task Queue**: Celery
- **Observability**: LangSmith + Prometheus

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

cp .env.example .env
# Edit .env with your credentials

alembic upgrade head

uvicorn app.main:app --reload
```

## Project Structure

```
backend/
├── app/
│   ├── api/v1/          # API endpoints
│   ├── core/            # Configuration & security
│   ├── db/              # Database setup
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── middleware/      # Custom middleware
│   └── utils/           # Utilities
├── alembic/             # Database migrations
└── tests/               # Tests
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

