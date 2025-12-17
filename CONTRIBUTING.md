# Contributing to Enterprise RAG Platform

Thank you for your interest in contributing to the Enterprise RAG Platform! This document provides guidelines and instructions for contributing to this project.

## 🤝 Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for everyone.

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Docker and Docker Compose
- Git
- PostgreSQL 15 (for local development)
- Redis 7 (for local development)

### Setting Up Development Environment

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/Enterprise-RAG-Platform.git
   cd Enterprise-RAG-Platform/backend
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements-dev.txt
   ```

4. **Set Up Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your local configuration
   ```

5. **Run Database Migrations**
   ```bash
   alembic upgrade head
   python scripts/init_db.py
   ```

6. **Start Development Server**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📝 Development Workflow

### Branching Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `bugfix/*` - Bug fixes
- `hotfix/*` - Urgent production fixes

### Creating a Feature Branch

```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name
```

### Making Changes

1. **Write Clear Code**
   - Follow PEP 8 style guidelines
   - Use type hints
   - Write docstrings for functions and classes
   - Keep functions small and focused

2. **Write Tests**
   - Add unit tests for new functions
   - Add integration tests for new endpoints
   - Maintain or improve code coverage
   - Run tests locally before committing

3. **Update Documentation**
   - Update README.md if adding new features
   - Update API documentation
   - Add docstrings to new functions
   - Update environment variable documentation

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest app/tests/test_chat.py

# Run tests in watch mode
pytest-watch
```

### Code Quality Checks

```bash
# Format code with black
black app/

# Sort imports
isort app/

# Type checking
mypy app/

# Linting
flake8 app/

# Run all checks
make lint
```

### Committing Changes

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add streaming support for chat responses
fix: resolve authentication token expiration issue
docs: update API documentation for document endpoints
test: add tests for RAG workflow
refactor: simplify vector store service
chore: update dependencies
```

Example:
```bash
git add .
git commit -m "feat: add support for CSV file uploads"
```

### Submitting a Pull Request

1. **Push Your Branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to GitHub and create a PR from your branch to `develop`
   - Fill out the PR template with details
   - Link any related issues
   - Request review from maintainers

3. **PR Requirements**
   - All tests must pass
   - Code coverage should not decrease
   - Code must follow style guidelines
   - Documentation must be updated
   - No merge conflicts

4. **Review Process**
   - Address reviewer feedback
   - Update your branch as needed
   - Keep the PR focused and small

## 🐛 Reporting Bugs

### Before Submitting a Bug Report
- Check if the bug has already been reported
- Ensure you're using the latest version
- Try to reproduce the issue

### How to Submit a Bug Report

Create an issue on GitHub with:
- **Title**: Clear, descriptive title
- **Description**: Detailed description of the bug
- **Steps to Reproduce**: Step-by-step instructions
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Environment**: OS, Python version, dependencies
- **Screenshots**: If applicable
- **Logs**: Relevant error messages or logs

## 💡 Suggesting Enhancements

### Feature Requests

Create an issue with:
- **Title**: Clear feature title
- **Problem**: What problem does this solve?
- **Solution**: Proposed solution
- **Alternatives**: Alternative solutions considered
- **Additional Context**: Any other relevant information

## 🏗️ Project Structure

```
backend/app/
├── api/v1/endpoints/    # API route handlers
├── core/                # Core configuration
├── db/                  # Database setup
├── models/              # SQLAlchemy models
├── schemas/             # Pydantic schemas
├── services/            # Business logic
├── middleware/          # Custom middleware
├── utils/               # Utility functions
└── tests/               # Test suite
```

## 📚 Development Guidelines

### API Development

1. **Use Dependency Injection**
   ```python
   from app.api.v1.dependencies.auth import get_current_user
   
   @router.get("/protected")
   async def protected_route(
       current_user: User = Depends(get_current_user)
   ):
       return {"user": current_user}
   ```

2. **Use Pydantic for Validation**
   ```python
   from pydantic import BaseModel, Field
   
   class DocumentCreate(BaseModel):
       title: str = Field(..., min_length=1, max_length=255)
       content: str
   ```

3. **Handle Errors Gracefully**
   ```python
   from fastapi import HTTPException, status
   
   if not document:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail="Document not found"
       )
   ```

### Database Operations

1. **Use Async Sessions**
   ```python
   async with AsyncSessionLocal() as db:
       result = await db.execute(select(User))
       users = result.scalars().all()
   ```

2. **Use Transactions**
   ```python
   async with db.begin():
       # Multiple operations
       db.add(user)
       db.add(document)
   ```

3. **Create Migrations**
   ```bash
   alembic revision --autogenerate -m "add new field"
   alembic upgrade head
   ```

### Testing Guidelines

1. **Use Fixtures**
   ```python
   @pytest.fixture
   async def test_user(db: AsyncSession):
       user = User(email="test@example.com")
       db.add(user)
       await db.commit()
       return user
   ```

2. **Test Edge Cases**
   - Invalid input
   - Missing data
   - Unauthorized access
   - Rate limiting

3. **Use Factories**
   ```python
   def create_test_document(**kwargs):
       defaults = {"title": "Test Doc", "content": "Content"}
       defaults.update(kwargs)
       return Document(**defaults)
   ```

## 🔒 Security

### Reporting Security Vulnerabilities

**Do not create public issues for security vulnerabilities.**

Instead, email security concerns to: your-email@example.com

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### Security Best Practices

- Never commit sensitive data (API keys, passwords)
- Use environment variables for configuration
- Validate all user input
- Use parameterized queries
- Implement rate limiting
- Follow OWASP guidelines

## 📄 Documentation

### Code Documentation

- Use docstrings for all public functions and classes
- Follow Google or NumPy docstring format
- Include type hints
- Document parameters and return values

Example:
```python
async def create_document(
    title: str,
    content: str,
    user_id: str,
    db: AsyncSession
) -> Document:
    """
    Create a new document in the database.
    
    Args:
        title: The document title
        content: The document content
        user_id: The ID of the user creating the document
        db: Database session
        
    Returns:
        Document: The created document
        
    Raises:
        ValueError: If title is empty
        DatabaseError: If database operation fails
    """
    # Implementation
```

### API Documentation

- All endpoints should have clear descriptions
- Document all parameters
- Provide example requests/responses
- Document error responses

## 🎯 Review Checklist

Before submitting a PR, ensure:

- [ ] Code follows PEP 8 style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] Commit messages follow conventions
- [ ] No merge conflicts
- [ ] Type hints are used
- [ ] Error handling is implemented
- [ ] No hardcoded values
- [ ] Environment variables are documented
- [ ] Database migrations are included (if needed)
- [ ] Breaking changes are documented

## 🙋 Questions?

Feel free to:
- Open a discussion on GitHub
- Join our community chat
- Email: your-email@example.com

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Enterprise RAG Platform! 🚀

