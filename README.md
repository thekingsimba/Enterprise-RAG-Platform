# 🚀 Enterprise RAG Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688?style=flat&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-🦜-green)](https://www.langchain.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-316192?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-DC382D?style=flat&logo=redis&logoColor=white)](https://redis.io/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

A production-ready, enterprise-grade **Retrieval-Augmented Generation (RAG)** platform built with modern AI technologies. This platform enables organizations to build intelligent, context-aware chatbots powered by their own document repositories with advanced features like multi-tenancy, real-time monitoring, and agentic workflows.

> **🎯 Designed for Scale**: Multi-tenant architecture, async processing, comprehensive observability, and production-ready infrastructure.

---

## ✨ Key Features

### 🤖 Advanced RAG Capabilities
- **LangGraph Agentic Workflows** - Multi-step reasoning with query rewriting, retrieval, and generation
- **Semantic Search** - Vector-based document retrieval using Pinecone
- **Streaming Responses** - Real-time SSE-based chat streaming
- **Context-Aware Chat** - Maintains conversation history for coherent multi-turn dialogues
- **Source Attribution** - Provides document sources with relevance scores

### 🏢 Enterprise Features
- **Multi-Tenancy** - Complete organization-level isolation with namespaced vector stores
- **Role-Based Access Control (RBAC)** - Admin, organization admin, and user roles
- **Document Management** - Upload, process, and manage PDF, DOCX, TXT, CSV, and MD files
- **Usage Tracking & Analytics** - Comprehensive metrics for tokens, queries, and system performance
- **Rate Limiting** - Configurable per-minute and per-hour limits
- **Audit Logging** - Full request/response logging with middleware

### 🔒 Security & Authentication
- **JWT-based Authentication** - Access and refresh tokens with secure signing
- **Password Hashing** - Bcrypt-based secure password storage
- **Token Refresh Flow** - Automatic token rotation
- **User Activation System** - Admin-controlled user activation

### ⚡ Performance & Scalability
- **Asynchronous Architecture** - FastAPI with async/await throughout
- **Background Task Processing** - Celery workers for document processing
- **Redis Caching** - High-speed caching layer
- **Connection Pooling** - Optimized database connections with SQLAlchemy
- **Horizontal Scalability** - Stateless design ready for containerization

### 📊 Observability & Monitoring
- **Prometheus Metrics** - Request rates, latencies, and custom business metrics
- **LangSmith Tracing** - End-to-end LLM call tracing and debugging
- **MLflow Integration** - Experiment tracking for RAG optimization
- **Sentry Error Tracking** - Production error monitoring and alerting
- **Flower Dashboard** - Real-time Celery task monitoring

### 🛠️ Developer Experience
- **OpenAPI Documentation** - Auto-generated interactive API docs
- **Type Safety** - Pydantic models throughout for validation
- **Database Migrations** - Alembic-based schema versioning
- **Docker Compose** - One-command local development setup
- **Comprehensive Testing** - pytest with fixtures and async test support
- **Code Quality** - Structured architecture following best practices

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         API Layer (FastAPI)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Auth API   │  │Document API  │  │   Chat API   │   ...    │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└────────────────┬────────────────────────────────┬───────────────┘
                 │                                 │
       ┌─────────▼─────────┐             ┌────────▼────────┐
       │  Business Logic   │             │  RAG Workflow   │
       │   (Services)      │             │  (LangGraph)    │
       └─────────┬─────────┘             └────────┬────────┘
                 │                                 │
    ┌────────────▼────────────┐         ┌─────────▼──────────┐
    │   PostgreSQL (SQLAlchemy) │         │   Pinecone Vector   │
    │   - Users & Orgs          │         │   - Embeddings      │
    │   - Documents             │         │   - Namespaces      │
    │   - Conversations         │         └─────────┬──────────┘
    └───────────────────────────┘                   │
                                          ┌─────────▼──────────┐
    ┌───────────────────────────┐         │   OpenAI API        │
    │   Redis Cache             │         │   - GPT-4 Turbo     │
    │   - Rate Limiting         │         │   - Embeddings      │
    │   - Session Storage       │         └────────────────────┘
    └───────────────────────────┘

    ┌───────────────────────────┐         ┌────────────────────┐
    │   Celery Workers          │         │   AWS S3            │
    │   - Document Processing   │────────▶│   - File Storage    │
    │   - Async Tasks           │         └────────────────────┘
    └───────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend Framework
- **FastAPI** - Modern, high-performance Python web framework
- **Uvicorn** - Lightning-fast ASGI server
- **Pydantic** - Data validation and settings management

### Database & Caching
- **PostgreSQL 15** - Primary relational database
- **SQLAlchemy 2.0** - ORM with async support
- **Alembic** - Database migration management
- **Redis 7** - In-memory cache and session store

### AI & Machine Learning
- **LangChain** - LLM orchestration framework
- **LangGraph** - Agentic workflow orchestration
- **LangSmith** - LLM observability and debugging
- **OpenAI GPT-4** - Large language model
- **Pinecone** - Vector database for semantic search
- **tiktoken** - Token counting and management

### Task Processing
- **Celery** - Distributed task queue
- **Flower** - Real-time Celery monitoring
- **Redis** - Message broker and result backend

### Storage & File Processing
- **AWS S3** - Object storage
- **Boto3** - AWS SDK
- **PyPDF** - PDF parsing
- **python-docx** - DOCX parsing
- **Pillow** - Image processing

### Observability
- **Prometheus** - Metrics collection
- **Sentry** - Error tracking
- **MLflow** - Experiment tracking
- **Custom Middleware** - Request logging and usage tracking

### Security
- **python-jose** - JWT implementation
- **passlib** - Password hashing
- **bcrypt** - Cryptographic hashing

### Development & Testing
- **pytest** - Testing framework
- **httpx** - Async HTTP client for tests
- **Docker & Docker Compose** - Containerization
- **python-dotenv** - Environment management

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+ (for local development)
- OpenAI API Key
- Pinecone API Key
- AWS Account (for S3 storage)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/Enterprise-RAG-Platform.git
cd Enterprise-RAG-Platform/backend
```

### 2️⃣ Set Up Environment Variables
```bash
cp .env.example .env
# Edit .env with your API keys and credentials
```

Required environment variables:
```env
SECRET_KEY=your-secret-key-here
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=your-bucket-name
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/rag_platform
REDIS_URL=redis://redis:6379/0
```

### 3️⃣ Launch with Docker Compose
```bash
# Build and start all services
make build
make up

# Run database migrations
make migrate

# View logs
make logs
```

### 4️⃣ Access the Platform
- **API Documentation**: http://localhost:8000/docs
- **Backend API**: http://localhost:8000/api/v1
- **Celery Flower**: http://localhost:5555

---

## 📚 API Documentation

### Authentication Endpoints
```
POST   /api/v1/auth/register          # Register new user
POST   /api/v1/auth/login             # Login and get tokens
POST   /api/v1/auth/refresh           # Refresh access token
```

### Document Management
```
GET    /api/v1/documents              # List user's documents
POST   /api/v1/documents/upload       # Upload and process document
GET    /api/v1/documents/{id}         # Get document details
PUT    /api/v1/documents/{id}         # Update document metadata
DELETE /api/v1/documents/{id}         # Delete document and vectors
```

### Chat & RAG
```
POST   /api/v1/chat/conversations     # Create new conversation
GET    /api/v1/chat/conversations     # List user's conversations
POST   /api/v1/chat/chat              # Send chat message
POST   /api/v1/chat/chat/stream       # Stream chat response (SSE)
POST   /api/v1/chat/chat/workflow     # Use LangGraph agentic workflow
```

### Organization Management
```
GET    /api/v1/organizations          # List organizations (admin)
POST   /api/v1/organizations          # Create organization (admin)
GET    /api/v1/organizations/{id}     # Get organization details
PUT    /api/v1/organizations/{id}     # Update organization
DELETE /api/v1/organizations/{id}     # Delete organization
```

### Admin & Analytics
```
GET    /api/v1/admin/analytics/overview       # System overview stats
GET    /api/v1/admin/analytics/organizations  # Per-org analytics
GET    /api/v1/admin/analytics/usage          # Usage metrics
GET    /api/v1/admin/users                    # List all users
PUT    /api/v1/admin/users/{id}/activate      # Activate/deactivate user
GET    /api/v1/admin/documents/stats          # Document statistics
```

### Health & Metrics
```
GET    /health                        # Health check
GET    /metrics                       # Prometheus metrics
```

---

## 🏗️ Project Structure

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/          # API route handlers
│   │   │   ├── auth.py         # Authentication endpoints
│   │   │   ├── chat.py         # Chat & RAG endpoints
│   │   │   ├── documents.py    # Document management
│   │   │   ├── users.py        # User management
│   │   │   ├── organizations.py# Organization CRUD
│   │   │   ├── admin.py        # Admin analytics
│   │   │   └── metrics.py      # Metrics endpoint
│   │   └── dependencies/       # Dependency injection
│   │       └── auth.py         # Auth dependencies
│   ├── core/
│   │   ├── config.py           # Application settings
│   │   └── security.py         # Security utilities
│   ├── db/
│   │   ├── base.py             # SQLAlchemy base
│   │   ├── session.py          # Database sessions
│   │   └── init_db.py          # DB initialization
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── organization.py
│   │   ├── document.py
│   │   ├── conversation.py
│   │   └── usage_metrics.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   ├── document.py
│   │   ├── chat.py
│   │   └── token.py
│   ├── services/               # Business logic layer
│   │   ├── chat_service.py     # Chat orchestration
│   │   ├── document_service.py # Document processing
│   │   ├── embedding_service.py# Text embedding
│   │   ├── llm_service.py      # LLM integration
│   │   ├── rag_workflow.py     # LangGraph workflow
│   │   ├── vector_store_service.py # Pinecone operations
│   │   ├── storage_service.py  # S3 operations
│   │   └── usage_tracking_service.py
│   ├── middleware/             # Custom middleware
│   │   ├── logging_middleware.py
│   │   ├── rate_limiter.py
│   │   ├── prometheus_middleware.py
│   │   └── usage_tracking_middleware.py
│   ├── utils/                  # Utility functions
│   │   ├── chunking.py         # Text chunking
│   │   ├── document_parser.py  # File parsing
│   │   └── file_validator.py   # File validation
│   ├── tests/                  # Test suite
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_chat.py
│   │   └── test_documents.py
│   ├── main.py                 # FastAPI application
│   └── worker.py               # Celery worker
├── alembic/                    # Database migrations
│   └── versions/
├── scripts/                    # Helper scripts
│   ├── init_db.py
│   └── create_migration.sh
├── docker-compose.yml          # Multi-container setup
├── Dockerfile                  # Backend container
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── Makefile                    # Automation commands
└── README.md                   # Backend documentation
```

---

## 🧪 Development

### Local Setup (Without Docker)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Set up environment
cp .env.example .env
# Edit .env with your configuration

# Start PostgreSQL and Redis locally
# Then run migrations
alembic upgrade head

# Initialize database with default data
python scripts/init_db.py

# Start development server
uvicorn app.main:app --reload --port 8000

# In another terminal, start Celery worker
celery -A app.worker worker --loglevel=info
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_auth.py

# Run with verbose output
pytest -v
```

### Docker Commands (via Makefile)
```bash
make build          # Build Docker images
make up             # Start all services
make down           # Stop all services
make logs           # View logs
make shell          # Access backend shell
make migrate        # Run database migrations
make test           # Run tests in container
make clean          # Remove containers and volumes
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

---

## 🎯 Key Implementation Highlights

### LangGraph Agentic Workflow
The RAG system uses LangGraph to create a sophisticated multi-step reasoning pipeline:

1. **Query Rewriting** - Analyzes chat history and rewrites queries for better retrieval
2. **Context Retrieval** - Performs semantic search in Pinecone with relevance scoring
3. **Answer Generation** - Generates responses with GPT-4 using retrieved context

```python
# Simplified workflow structure
workflow = StateGraph(RAGState)
workflow.add_node("rewrite_query", self.rewrite_query)
workflow.add_node("retrieve_context", self.retrieve_context)
workflow.add_node("generate_answer", self.generate_answer)
workflow.set_entry_point("rewrite_query")
workflow.add_edge("rewrite_query", "retrieve_context")
workflow.add_edge("retrieve_context", "generate_answer")
```

### Multi-Tenant Vector Store
Each organization gets isolated namespaces in Pinecone:
```python
namespace = f"org_{organization_id}"
results = vector_store.query_vectors(
    query_vector=embedding,
    namespace=namespace,
    top_k=5
)
```

### Async Document Processing
Documents are processed asynchronously via Celery:
```python
@celery_app.task
async def process_document(document_id: str):
    # Parse document
    # Generate embeddings
    # Store in Pinecone
    # Update database status
```

### Rate Limiting Middleware
Protects API from abuse with Redis-backed rate limiting:
```python
class RateLimitMiddleware:
    async def __call__(self, request: Request):
        # Check rate limit in Redis
        # Track per-user or per-IP
        # Return 429 if exceeded
```

---

## 📊 Monitoring & Observability

### Prometheus Metrics
Custom metrics exposed at `/metrics`:
- `http_requests_total` - Total HTTP requests by endpoint and method
- `http_request_duration_seconds` - Request latency histogram
- `active_users` - Current active users
- `documents_processed_total` - Total documents processed
- `chat_messages_total` - Total chat messages
- `token_usage_total` - Total tokens consumed

### LangSmith Tracing
Every LLM call is traced with:
- Full prompt and completion
- Token counts
- Latency metrics
- Error tracking
- Chain visualization

### Sentry Integration
Production errors are captured with:
- Full stack traces
- Request context
- User information
- Performance monitoring

---

## 🔐 Security Best Practices

✅ **JWT Authentication** with secure token rotation  
✅ **Password Hashing** using bcrypt  
✅ **SQL Injection Protection** via SQLAlchemy ORM  
✅ **CORS Configuration** for controlled access  
✅ **Rate Limiting** to prevent abuse  
✅ **Input Validation** with Pydantic  
✅ **Environment Variable Management** - No secrets in code  
✅ **RBAC** - Role-based access control  
✅ **Audit Logging** - Full request/response logging  

---

## 🌟 Advanced Features

### Real-Time Streaming
Server-Sent Events (SSE) for streaming chat responses:
```python
@router.post("/chat/stream")
async def stream_chat():
    async def generate():
        async for chunk in llm_service.stream():
            yield f"data: {chunk}\n\n"
    return StreamingResponse(generate())
```

### Background Task Processing
Celery workers handle long-running tasks:
- Document parsing and embedding
- Bulk data operations
- Scheduled analytics computation

### Usage Tracking
Comprehensive tracking of:
- Token consumption per organization
- API call volumes
- Cost estimation
- Rate limit status

---

## 📈 Performance Optimization

- **Connection Pooling** - Reused database connections
- **Redis Caching** - Frequently accessed data cached
- **Async I/O** - Non-blocking operations throughout
- **Batch Processing** - Bulk embeddings for efficiency
- **Lazy Loading** - SQLAlchemy relationships loaded on demand
- **Index Optimization** - Database indexes on foreign keys
- **Vector Search Optimization** - Pinecone namespacing for faster queries

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Salomon Ayah**

- GitHub: [@salomonayah](https://github.com/salomonayah)
- LinkedIn: [linkedin.com/in/salomonayah](https://linkedin.com/in/salomonayah)

---

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- LangChain team for the powerful LLM orchestration tools
- OpenAI for GPT-4 and embeddings
- Pinecone for vector database infrastructure

---

## 📧 Contact

For questions or collaboration opportunities, feel free to reach out!

**Project Status**: 🟢 Active Development

---

<div align="center">

**⭐ If you found this project useful, please consider giving it a star! ⭐**

Made with ❤️ and ☕ by Salomon Ayah

</div>

