# 🚀 Quick Start Guide

Get the Enterprise RAG Platform up and running in 5 minutes!

## Prerequisites

- Docker & Docker Compose installed
- OpenAI API key
- Pinecone account and API key
- AWS account (for S3 storage)

## 📦 Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/Enterprise-RAG-Platform.git
cd Enterprise-RAG-Platform
```

### 2. Set Up Environment Variables

```bash
cd backend
cp .env.example .env
```

Edit `.env` and add your credentials:

```env
# Required - Get these first!
SECRET_KEY=your-super-secret-key-at-least-32-chars
OPENAI_API_KEY=sk-your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_S3_BUCKET=your-bucket-name

# Optional - Can use defaults for local development
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/rag_platform
REDIS_URL=redis://redis:6379/0
```

### 3. Start the Platform

```bash
# Build Docker images
make build

# Start all services
make up

# Run database migrations
make migrate

# View logs (optional)
make logs
```

That's it! 🎉

## 🌐 Access the Platform

Once running, you can access:

- **API Documentation**: http://localhost:8000/docs
- **API Base URL**: http://localhost:8000/api/v1
- **Health Check**: http://localhost:8000/health
- **Celery Flower**: http://localhost:5555

## 🧪 Test the API

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "password": "SecurePassword123!",
    "full_name": "Admin User",
    "organization_name": "My Organization"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin@example.com",
    "password": "SecurePassword123!"
  }'
```

Save the `access_token` from the response.

### 3. Upload a Document

```bash
curl -X POST "http://localhost:8000/api/v1/documents/upload" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/your/document.pdf" \
  -F "title=My First Document"
```

### 4. Create a Conversation

```bash
curl -X POST "http://localhost:8000/api/v1/chat/conversations" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Chat"
  }'
```

### 5. Ask a Question

```bash
curl -X POST "http://localhost:8000/api/v1/chat/chat" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is this document about?",
    "conversation_id": "CONVERSATION_ID_FROM_STEP_4"
  }'
```

## 🎯 Interactive API Testing

The easiest way to test the API is using the built-in Swagger UI:

1. Go to http://localhost:8000/docs
2. Click "Authorize" button
3. Enter your access token
4. Try out any endpoint interactively!

## 📊 Monitor Background Tasks

View Celery task processing:

1. Go to http://localhost:5555
2. See active workers, tasks, and task history

## 🛠️ Common Commands

```bash
# View logs
make logs

# Stop all services
make down

# Restart services
make restart

# Access backend shell
make shell

# Run tests
make test

# Clean up everything
make clean
```

## 🔍 Troubleshooting

### Services won't start

```bash
# Check if ports are already in use
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL
lsof -i :6379  # Redis

# Clean and rebuild
make clean
make build
make up
```

### Database migration errors

```bash
# Reset database
docker-compose down -v
docker-compose up -d postgres
make migrate
```

### Can't connect to external services

- **OpenAI**: Verify your API key is valid
- **Pinecone**: Ensure your index exists and API key is correct
- **AWS S3**: Check bucket exists and credentials have proper permissions

### Document processing stuck

```bash
# Check Celery worker logs
docker-compose logs celery_worker

# Restart worker
docker-compose restart celery_worker
```

## 📚 Next Steps

Now that you're up and running:

1. **Read the [Full Documentation](README.md)** - Learn about all features
2. **Explore the [Architecture](ARCHITECTURE.md)** - Understand how it works
3. **Check [Contributing Guidelines](CONTRIBUTING.md)** - Start contributing
4. **Review [API Endpoints](README.md#-api-documentation)** - See all available APIs

## 🎓 Example Workflows

### Workflow 1: Document Q&A

1. Register and login
2. Upload multiple PDF documents
3. Wait for processing (check Flower dashboard)
4. Create a conversation
5. Ask questions about your documents
6. Get AI-powered answers with source citations

### Workflow 2: Multi-User Organization

1. Admin registers and creates organization
2. Admin invites users (create accounts)
3. Users upload documents to shared knowledge base
4. All users can query the collective knowledge
5. Admin monitors usage via analytics endpoints

### Workflow 3: Streaming Chat

1. Set up as above
2. Use `/api/v1/chat/chat/stream` endpoint
3. Receive real-time streaming responses
4. Better UX for long-form answers

## 🔐 Security Notes

For production deployment:

- ✅ Change all default passwords
- ✅ Use strong `SECRET_KEY` (32+ characters)
- ✅ Enable HTTPS
- ✅ Set proper CORS origins
- ✅ Configure rate limits
- ✅ Enable Sentry for error tracking
- ✅ Set up proper backups
- ✅ Use managed services (RDS, ElastiCache, etc.)

## 💡 Tips

- **Development**: Use `make logs -f` to follow logs in real-time
- **Testing**: The test database is separate from development
- **Performance**: Increase Celery workers for faster document processing
- **Debugging**: Check individual service logs with `docker-compose logs [service]`

## 🆘 Getting Help

- **Issues**: [GitHub Issues](https://github.com/yourusername/Enterprise-RAG-Platform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/Enterprise-RAG-Platform/discussions)
- **Email**: your-email@example.com

## 🎉 You're All Set!

You now have a fully functional enterprise RAG platform running locally. Start building amazing AI-powered applications!

---

**Happy Building! 🚀**

