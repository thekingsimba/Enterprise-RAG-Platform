# Enterprise RAG Platform - Architecture Documentation

## 📐 System Architecture Overview

The Enterprise RAG Platform is built using a modern, scalable microservices-inspired architecture with a focus on performance, maintainability, and production readiness.

## 🏛️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           Client Layer                               │
│  (Web Apps, Mobile Apps, Third-party Integrations)                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTPS/REST
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                      API Gateway Layer                               │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  FastAPI Application (app/main.py)                           │  │
│  │  - CORS Middleware                                           │  │
│  │  - Authentication Middleware                                 │  │
│  │  - Rate Limiting Middleware                                  │  │
│  │  - Logging Middleware                                        │  │
│  │  - Prometheus Metrics Middleware                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
┌───────────────▼─────────┐  ┌───────────▼──────────────────────────┐
│   API Endpoints Layer   │  │   Background Processing Layer        │
│  (app/api/v1/endpoints) │  │   (Celery Workers)                   │
│                         │  │                                      │
│  - Authentication       │  │  - Document Processing               │
│  - Documents            │  │  - Embedding Generation              │
│  - Chat                 │  │  - Vector Store Updates              │
│  - Organizations        │  │  - Scheduled Tasks                   │
│  - Admin                │  │  - Batch Operations                  │
│  - Users                │  │                                      │
└───────────┬─────────────┘  └───────────┬──────────────────────────┘
            │                            │
            │                            │
┌───────────▼────────────────────────────▼──────────────────────────┐
│                    Business Logic Layer                            │
│  (app/services)                                                    │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │ Chat Service │  │Document Svc  │  │ RAG Workflow (Graph) │   │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘   │
│         │                  │                      │               │
│  ┌──────▼───────┐  ┌──────▼───────┐  ┌──────────▼───────────┐   │
│  │  LLM Service │  │Embedding Svc │  │Vector Store Service  │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │Storage Svc   │  │Usage Track   │  │ MLflow Service       │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
└────────────────────────────┬───────────────────────────────────────┘
                             │
                ┌────────────┴────────────┐
                │                         │
┌───────────────▼─────────┐  ┌───────────▼──────────────────────────┐
│   Data Persistence      │  │   External Services                  │
│                         │  │                                      │
│  ┌──────────────────┐  │  │  ┌──────────────────────────────┐   │
│  │   PostgreSQL     │  │  │  │   OpenAI API                 │   │
│  │   - Users        │  │  │  │   - GPT-4 Turbo              │   │
│  │   - Organizations│  │  │  │   - text-embedding-3-small   │   │
│  │   - Documents    │  │  │  └──────────────────────────────┘   │
│  │   - Conversations│  │  │                                      │
│  │   - Messages     │  │  │  ┌──────────────────────────────┐   │
│  │   - Metrics      │  │  │  │   Pinecone Vector DB         │   │
│  └──────────────────┘  │  │  │   - Namespaced Indexes       │   │
│                         │  │  │   - Semantic Search          │   │
│  ┌──────────────────┐  │  │  └──────────────────────────────┘   │
│  │   Redis          │  │  │                                      │
│  │   - Cache        │  │  │  ┌──────────────────────────────┐   │
│  │   - Rate Limits  │  │  │  │   AWS S3                     │   │
│  │   - Sessions     │  │  │  │   - Document Storage         │   │
│  │   - Celery Queue │  │  │  │   - File Uploads             │   │
│  └──────────────────┘  │  │  └──────────────────────────────┘   │
└─────────────────────────┘  └──────────────────────────────────────┘
```

## 🔄 RAG Workflow Architecture (LangGraph)

The RAG system uses LangGraph to orchestrate a multi-step agentic workflow:

```
┌─────────────────────────────────────────────────────────────────┐
│                      RAG Workflow State                          │
│  - query: str                                                    │
│  - organization_id: str                                          │
│  - chat_history: List[Dict]                                      │
│  - rewritten_query: str                                          │
│  - context: str                                                  │
│  - sources: List[Dict]                                           │
│  - answer: str                                                   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Entry Point   │
                    └────────┬───────┘
                             │
                             ▼
                ┌────────────────────────┐
                │  1. Query Rewriting    │
                │                        │
                │  - Analyze history     │
                │  - Contextualize query │
                │  - Generate standalone │
                │    question            │
                └────────┬───────────────┘
                         │
                         ▼
                ┌────────────────────────┐
                │  2. Context Retrieval  │
                │                        │
                │  - Generate embedding  │
                │  - Query Pinecone      │
                │  - Rank results        │
                │  - Extract sources     │
                └────────┬───────────────┘
                         │
                         ▼
                ┌────────────────────────┐
                │  3. Answer Generation  │
                │                        │
                │  - Format context      │
                │  - Call LLM (GPT-4)    │
                │  - Generate response   │
                │  - Include sources     │
                └────────┬───────────────┘
                         │
                         ▼
                    ┌────────────┐
                    │    END     │
                    └────────────┘
```

## 🗄️ Database Schema

### Core Entities

```sql
-- Users Table
users
├── id (UUID, PK)
├── email (VARCHAR, UNIQUE)
├── hashed_password (VARCHAR)
├── full_name (VARCHAR)
├── organization_id (UUID, FK)
├── role (ENUM: admin, org_admin, user)
├── is_active (BOOLEAN)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

-- Organizations Table
organizations
├── id (UUID, PK)
├── name (VARCHAR, UNIQUE)
├── domain (VARCHAR)
├── is_active (BOOLEAN)
├── max_users (INTEGER)
├── max_documents (INTEGER)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

-- Documents Table
documents
├── id (UUID, PK)
├── title (VARCHAR)
├── filename (VARCHAR)
├── file_type (VARCHAR)
├── file_size (INTEGER)
├── s3_key (VARCHAR)
├── status (ENUM: pending, processing, completed, failed)
├── organization_id (UUID, FK)
├── uploaded_by (UUID, FK)
├── chunk_count (INTEGER)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

-- Conversations Table
conversations
├── id (UUID, PK)
├── title (VARCHAR)
├── user_id (UUID, FK)
├── organization_id (UUID, FK)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

-- Messages Table
messages
├── id (UUID, PK)
├── conversation_id (UUID, FK)
├── role (ENUM: user, assistant)
├── content (TEXT)
├── sources (JSONB)
├── token_count (INTEGER)
├── created_at (TIMESTAMP)
└── metadata (JSONB)

-- Usage Metrics Table
usage_metrics
├── id (UUID, PK)
├── organization_id (UUID, FK)
├── user_id (UUID, FK)
├── metric_type (ENUM: api_call, tokens, documents)
├── value (INTEGER)
├── timestamp (TIMESTAMP)
└── metadata (JSONB)
```

### Relationships

```
organizations (1) ──< (N) users
organizations (1) ──< (N) documents
users (1) ──< (N) conversations
conversations (1) ──< (N) messages
organizations (1) ──< (N) usage_metrics
users (1) ──< (N) usage_metrics
```

## 🔐 Authentication & Authorization Flow

```
┌──────────────┐
│    Client    │
└──────┬───────┘
       │
       │ 1. POST /auth/login
       │    {email, password}
       ▼
┌──────────────────────────┐
│   Auth Endpoint          │
│                          │
│  - Validate credentials  │
│  - Check user is_active  │
│  - Generate JWT tokens   │
└──────┬───────────────────┘
       │
       │ 2. Return tokens
       │    {access_token, refresh_token}
       ▼
┌──────────────┐
│    Client    │
│  (Store JWT) │
└──────┬───────┘
       │
       │ 3. API Request
       │    Authorization: Bearer <access_token>
       ▼
┌──────────────────────────┐
│  Auth Dependency         │
│  (get_current_user)      │
│                          │
│  - Verify JWT signature  │
│  - Check expiration      │
│  - Load user from DB     │
│  - Check permissions     │
└──────┬───────────────────┘
       │
       │ 4. User object
       ▼
┌──────────────────────────┐
│   Protected Endpoint     │
│   (Business Logic)       │
└──────────────────────────┘
```

## 📊 Data Flow: Document Upload & Processing

```
┌──────────────┐
│   Client     │
└──────┬───────┘
       │
       │ 1. POST /documents/upload
       │    multipart/form-data
       ▼
┌────────────────────────────┐
│  Upload Endpoint           │
│                            │
│  - Validate file type      │
│  - Check file size         │
│  - Generate unique ID      │
└──────┬─────────────────────┘
       │
       │ 2. Upload to S3
       ▼
┌────────────────────────────┐
│  Storage Service (S3)      │
│                            │
│  - Store file              │
│  - Return S3 key           │
└──────┬─────────────────────┘
       │
       │ 3. Create DB record
       ▼
┌────────────────────────────┐
│  PostgreSQL                │
│                            │
│  - Insert document record  │
│  - Status: pending         │
└──────┬─────────────────────┘
       │
       │ 4. Queue processing task
       ▼
┌────────────────────────────┐
│  Celery Queue (Redis)      │
│                            │
│  - Add task to queue       │
└──────┬─────────────────────┘
       │
       │ 5. Process document
       ▼
┌────────────────────────────┐
│  Celery Worker             │
│                            │
│  - Download from S3        │
│  - Parse document          │
│  - Chunk text              │
│  - Generate embeddings     │
│  - Store in Pinecone       │
│  - Update DB status        │
└──────┬─────────────────────┘
       │
       │ 6. Store vectors
       ▼
┌────────────────────────────┐
│  Pinecone Vector DB        │
│                            │
│  - Namespace: org_<id>     │
│  - Store embeddings        │
│  - Store metadata          │
└────────────────────────────┘
```

## 💬 Data Flow: Chat Request

```
┌──────────────┐
│   Client     │
└──────┬───────┘
       │
       │ 1. POST /chat/chat
       │    {query, conversation_id}
       ▼
┌────────────────────────────┐
│  Chat Endpoint             │
│                            │
│  - Validate input          │
│  - Load conversation       │
│  - Check permissions       │
└──────┬─────────────────────┘
       │
       │ 2. Execute RAG workflow
       ▼
┌────────────────────────────┐
│  RAG Workflow (LangGraph)  │
│                            │
│  Step 1: Rewrite Query     │
│  - Load chat history       │
│  - Call LLM for rewrite    │
└──────┬─────────────────────┘
       │
       │ 3. Get embedding
       ▼
┌────────────────────────────┐
│  Embedding Service         │
│                            │
│  - Call OpenAI API         │
│  - Get vector (1536 dims)  │
└──────┬─────────────────────┘
       │
       │ 4. Semantic search
       ▼
┌────────────────────────────┐
│  Vector Store Service      │
│                            │
│  - Query Pinecone          │
│  - Get top-k results       │
│  - Extract metadata        │
└──────┬─────────────────────┘
       │
       │ 5. Generate answer
       ▼
┌────────────────────────────┐
│  LLM Service               │
│                            │
│  - Format prompt           │
│  - Call GPT-4              │
│  - Stream response         │
└──────┬─────────────────────┘
       │
       │ 6. Save to DB
       ▼
┌────────────────────────────┐
│  PostgreSQL                │
│                            │
│  - Save user message       │
│  - Save assistant message  │
│  - Update conversation     │
└──────┬─────────────────────┘
       │
       │ 7. Track usage
       ▼
┌────────────────────────────┐
│  Usage Tracking Service    │
│                            │
│  - Count tokens            │
│  - Log API call            │
│  - Update metrics          │
└──────┬─────────────────────┘
       │
       │ 8. Return response
       ▼
┌──────────────┐
│   Client     │
│  {answer,    │
│   sources}   │
└──────────────┘
```

## 🔄 Caching Strategy

### Redis Cache Layers

1. **Rate Limiting Cache**
   - Key: `rate_limit:{user_id}:{endpoint}`
   - TTL: 60 seconds (per-minute) / 3600 seconds (per-hour)
   - Value: Request count

2. **Session Cache**
   - Key: `session:{user_id}`
   - TTL: 30 minutes
   - Value: User session data

3. **Document Metadata Cache**
   - Key: `document:{document_id}`
   - TTL: 5 minutes
   - Value: Document metadata

4. **Organization Settings Cache**
   - Key: `org:{org_id}:settings`
   - TTL: 10 minutes
   - Value: Organization configuration

## 📈 Scalability Considerations

### Horizontal Scaling

1. **API Layer**
   - Stateless FastAPI instances
   - Load balancer (Nginx/ALB)
   - Auto-scaling based on CPU/memory

2. **Worker Layer**
   - Multiple Celery workers
   - Task routing by queue
   - Auto-scaling based on queue length

3. **Database Layer**
   - PostgreSQL read replicas
   - Connection pooling
   - Query optimization with indexes

4. **Cache Layer**
   - Redis Cluster
   - Sentinel for high availability
   - Sharding for large datasets

### Vertical Scaling

- Increase instance sizes for compute-heavy operations
- Optimize vector dimensions for memory efficiency
- Database query optimization

## 🔍 Monitoring Architecture

```
┌────────────────────────────────────────────────────────┐
│                  Application Layer                      │
│  - Request/Response logging                            │
│  - Error tracking                                      │
│  - Performance metrics                                 │
└────────────┬───────────────────────────────────────────┘
             │
    ┌────────┼────────┬────────────┐
    │        │        │            │
    ▼        ▼        ▼            ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────────┐
│Prometheus│ │LangSmith│ │ Sentry │ │  MLflow    │
│          │ │         │ │        │ │            │
│- Metrics │ │- LLM    │ │- Errors│ │- Experiments│
│- Alerts  │ │  Traces │ │- APM   │ │- Models    │
└────────┘ └────────┘ └────────┘ └────────────┘
```

## 🛡️ Security Architecture

### Defense in Depth

1. **Network Layer**
   - HTTPS/TLS encryption
   - Rate limiting
   - DDoS protection

2. **Application Layer**
   - JWT authentication
   - RBAC authorization
   - Input validation
   - SQL injection prevention (ORM)
   - XSS prevention

3. **Data Layer**
   - Encrypted at rest (S3, RDS)
   - Encrypted in transit
   - Password hashing (bcrypt)
   - Secrets management (env vars)

4. **Infrastructure Layer**
   - VPC isolation
   - Security groups
   - IAM roles
   - Audit logging

## 🚀 Deployment Architecture

### Docker Compose (Development)

```
┌─────────────────────────────────────────┐
│          Docker Network                  │
│                                         │
│  ┌──────────┐  ┌──────────┐           │
│  │PostgreSQL│  │  Redis   │           │
│  │  :5432   │  │  :6379   │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  ┌──────────┐  ┌──────────┐           │
│  │ Backend  │  │  Celery  │           │
│  │  :8000   │  │  Worker  │           │
│  └──────────┘  └──────────┘           │
│                                         │
│  ┌──────────┐                          │
│  │  Flower  │                          │
│  │  :5555   │                          │
│  └──────────┘                          │
└─────────────────────────────────────────┘
```

### Production (AWS/Cloud)

```
┌─────────────────────────────────────────────────────┐
│                    Load Balancer                     │
│                  (ALB/Nginx)                        │
└────────────────────┬────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐      ┌─────────▼────────┐
│  API Instance  │      │  API Instance    │
│  (Container)   │ ...  │  (Container)     │
└────────────────┘      └──────────────────┘
        │                         │
        └────────────┬────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
┌───────▼────────┐      ┌─────────▼────────┐
│  RDS (Postgres)│      │  ElastiCache     │
│  (Multi-AZ)    │      │  (Redis)         │
└────────────────┘      └──────────────────┘
```

## 📝 Technology Decisions

### Why FastAPI?
- High performance (async support)
- Automatic API documentation
- Type safety with Pydantic
- Modern Python features
- Large ecosystem

### Why PostgreSQL?
- ACID compliance
- JSON support (JSONB)
- Full-text search
- Mature and reliable
- Excellent ORM support

### Why Pinecone?
- Managed vector database
- High performance at scale
- Namespace support (multi-tenancy)
- Easy integration
- No infrastructure management

### Why LangChain/LangGraph?
- Powerful LLM orchestration
- Agentic workflow support
- Built-in observability
- Active community
- Production-ready

### Why Celery?
- Mature task queue
- Distributed processing
- Flexible routing
- Monitoring with Flower
- Python-native

## 🔮 Future Architecture Enhancements

1. **Microservices Split**
   - Separate document processing service
   - Dedicated chat service
   - Analytics service

2. **Event-Driven Architecture**
   - Event bus (Kafka/RabbitMQ)
   - Event sourcing for audit trail
   - CQRS pattern

3. **Advanced Caching**
   - Query result caching
   - Embedding caching
   - CDN for static assets

4. **Multi-Region Deployment**
   - Geographic distribution
   - Data replication
   - Latency optimization

5. **GraphQL API**
   - Alternative to REST
   - Flexible queries
   - Real-time subscriptions

---

**Last Updated**: December 2025  
**Version**: 1.0.0

