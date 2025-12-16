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

## Quick Start with Docker

```bash
cp .env.example .env
# Edit .env with your credentials

make build
make up
make migrate
```

Access:
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Flower (Celery): http://localhost:5555

## Local Development Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

cp .env.example .env
# Edit .env with your credentials

alembic upgrade head
python scripts/init_db.py

uvicorn app.main:app --reload
celery -A app.worker worker --loglevel=info
```

## Project Structure

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/   # API routes
│   │   └── dependencies/ # Auth & deps
│   ├── core/            # Config & security
│   ├── db/              # Database setup
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── services/        # Business logic
│   ├── middleware/      # Custom middleware
│   └── utils/           # Utilities
├── alembic/             # Migrations
├── scripts/             # Helper scripts
└── tests/               # Test suite
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/refresh` - Refresh token

### Documents
- `GET /api/v1/documents/` - List documents
- `POST /api/v1/documents/upload` - Upload document
- `GET /api/v1/documents/{id}` - Get document
- `PUT /api/v1/documents/{id}` - Update document
- `DELETE /api/v1/documents/{id}` - Delete document

### Chat
- `POST /api/v1/chat/conversations` - Create conversation
- `GET /api/v1/chat/conversations` - List conversations
- `POST /api/v1/chat/chat` - Send message
- `POST /api/v1/chat/chat/stream` - Stream chat (SSE)
- `POST /api/v1/chat/chat/workflow` - Chat with LangGraph

### Organizations
- `GET /api/v1/organizations/` - List orgs (admin)
- `POST /api/v1/organizations/` - Create org (admin)
- `GET /api/v1/organizations/{id}` - Get org
- `PUT /api/v1/organizations/{id}` - Update org
- `DELETE /api/v1/organizations/{id}` - Delete org

### Admin
- `GET /api/v1/admin/analytics/overview` - System overview
- `GET /api/v1/admin/analytics/organizations` - Org stats
- `GET /api/v1/admin/analytics/usage` - Usage metrics
- `GET /api/v1/admin/users` - List all users
- `PUT /api/v1/admin/users/{id}/activate` - Activate user
- `GET /api/v1/admin/documents/stats` - Document stats

## Testing

```bash
pytest
pytest -v
pytest --cov=app
```

## Docker Commands

```bash
make build      # Build images
make up         # Start services
make down       # Stop services
make logs       # View logs
make shell      # Backend shell
make migrate    # Run migrations
make test       # Run tests
make clean      # Clean containers
```

## Environment Variables

See `.env.example` for all configuration options.

Required:
- `SECRET_KEY` - JWT secret
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection
- `OPENAI_API_KEY` - OpenAI API key
- `PINECONE_API_KEY` - Pinecone API key
- `AWS_ACCESS_KEY_ID` - AWS credentials
- `AWS_SECRET_ACCESS_KEY` - AWS credentials

Optional:
- `LANGCHAIN_API_KEY` - LangSmith tracing
- `MLFLOW_TRACKING_URI` - MLflow tracking

