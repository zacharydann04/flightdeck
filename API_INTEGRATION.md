# API Integration Guide

This document explains how FlightDeck is structured for future backend integration.

## Architecture Overview

FlightDeck follows a modular architecture that separates concerns:

```
flightdeck/
├── app.py                 # Application factory
├── run.py                 # Development server entry point
├── config/                # Configuration management
│   └── settings.py        # Environment-specific configs
├── models/                # Database models (ORM-agnostic structure)
│   ├── user.py
│   ├── post.py
│   ├── like.py
│   └── comment.py
├── services/              # Business logic layer
│   ├── auth_service.py    # Authentication logic
│   ├── post_service.py    # Post operations
│   └── media_service.py   # Media storage
├── routes/                # HTTP endpoints
│   ├── auth.py            # Auth routes
│   ├── posts.py           # Post routes
│   └── users.py           # User routes
├── templates/             # HTML templates
└── static/                # Static assets
```

## Future Integration Points

### 1. Backend Server Integration

The application is structured to easily separate the frontend and backend:

**Option A: Keep Flask as API Server**
- Convert routes to return JSON responses
- Add CORS support for frontend requests
- Implement JWT authentication instead of sessions
- See `API_ENDPOINTS.md` for endpoint specifications

**Option B: Replace with Different Backend**
- The service layer (`services/`) contains all business logic
- Port services to your backend framework (Node.js, Django, etc.)
- Models define the data structure clearly
- APIs already return JSON for like/comment endpoints

### 2. Database Migration

Currently uses SQLite. To migrate to PostgreSQL, MySQL, or other databases:

```python
# In config/settings.py, change:
SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/flightdeck'
# or
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/flightdeck'
```

Models use SQLAlchemy ORM, which supports:
- PostgreSQL
- MySQL
- SQLite
- Oracle
- Microsoft SQL Server

### 3. Authentication Enhancement

Current implementation supports password-based auth. Ready for:

**OAuth Integration:**
```python
# In services/auth_service.py
def authenticate_oauth(provider, oauth_id, user_data):
    # Implementation ready for Google, GitHub, Facebook, etc.
```

**JWT Implementation:**
- Replace Flask-Login with JWT tokens
- Add token generation in `auth_service.py`
- Update routes to validate JWT tokens
- Example in `config/settings.py` has AUTH_PROVIDER setting

### 4. RESTful API

The application has API-ready structure:

**Current API Endpoints:**
- `POST /post/<id>/like` - Returns JSON
- `POST /post/<id>/comment` - Returns JSON

**To Create Full REST API:**
1. Create new blueprint in `routes/api.py`
2. Add API versioning (already configured in `config/settings.py`)
3. Return JSON from all endpoints
4. Add API authentication (JWT)

Example structure:
```
/api/v1/auth/register
/api/v1/auth/login
/api/v1/posts
/api/v1/posts/<id>
/api/v1/posts/<id>/like
/api/v1/posts/<id>/comments
/api/v1/users/<username>
```

### 5. Media Storage Integration

`services/media_service.py` provides interface for various storage backends:

**AWS S3:**
```python
# Install boto3
pip install boto3

# Implement in media_service.py
def upload_s3(file, bucket_name, key):
    import boto3
    s3_client = boto3.client('s3')
    s3_client.upload_fileobj(file, bucket_name, key)
    return f'https://{bucket_name}.s3.amazonaws.com/{key}'
```

**CloudFlare R2/Images:**
```python
# Use CloudFlare API for image uploads
def upload_cloudflare(file, account_id):
    # Implementation with requests library
    pass
```

**Azure Blob Storage:**
```python
# Use azure-storage-blob package
from azure.storage.blob import BlobServiceClient
```

## Configuration Management

All configurable settings are in `config/settings.py`:

```python
# Database
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

# Media Storage
MEDIA_STORAGE_PROVIDER = os.environ.get('MEDIA_STORAGE_PROVIDER', 'local')

# Authentication
AUTH_PROVIDER = os.environ.get('AUTH_PROVIDER', 'local')

# API Settings
API_PREFIX = '/api/v1'
```

Use environment variables for production:
```bash
export DATABASE_URL="postgresql://..."
export MEDIA_STORAGE_PROVIDER="s3"
export AUTH_PROVIDER="oauth"
export SECRET_KEY="your-secret-key"
```

## Service Layer Pattern

All business logic is in the service layer, making it easy to:
- Write unit tests
- Switch frameworks
- Create API endpoints
- Add caching
- Implement rate limiting

Example:
```python
from services import PostService

# Create post (works with any route/controller)
post, error = PostService.create_post(user, content, image_url)

# Toggle like
liked, count = PostService.toggle_like(post, user)

# Add comment
comment, error = PostService.add_comment(post, user, content)
```

## Testing

Create tests using the service layer:

```python
from app import create_app
from services import AuthService, PostService

app = create_app('testing')

def test_create_post():
    with app.app_context():
        user, _ = AuthService.register_user('test', 'test@example.com', 'pass')
        post, error = PostService.create_post(user, 'Test post')
        assert post is not None
        assert error is None
```

## Deployment Considerations

### Production Setup

1. Use production WSGI server (Gunicorn, uWSGI):
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 'app:create_app("production")'
```

2. Use production database (PostgreSQL recommended)

3. Enable HTTPS (SESSION_COOKIE_SECURE=True)

4. Use environment variables for secrets

5. Set up media CDN for static assets

### Docker Support

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:create_app('production')"]
```

### Microservices Architecture

The modular structure allows splitting into microservices:
- **Auth Service**: `models/user.py` + `services/auth_service.py`
- **Post Service**: `models/post.py` + `services/post_service.py`
- **Media Service**: `services/media_service.py`
- **Frontend**: Static files served separately

## Next Steps

1. **Add API Documentation**: Use Swagger/OpenAPI for API specs
2. **Implement Caching**: Add Redis for session management and caching
3. **Add Message Queue**: Use Celery for background tasks
4. **Real-time Features**: Add WebSockets for live notifications
5. **Analytics**: Integrate analytics service for user insights
6. **CDN Integration**: Use CloudFlare or AWS CloudFront for static assets
