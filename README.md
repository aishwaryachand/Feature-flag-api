# Feature Flag API

A comprehensive feature flag management system built with FastAPI and PostgreSQL, featuring JWT authentication, role-based access control, and environment-specific feature flags.

## Features

- 🔐 **JWT Authentication** - Secure user login/signup with JWT tokens
- 👥 **Role-Based Access Control** - Admin and Developer roles with different permissions
- 🚩 **Feature Flag Management** - Full CRUD operations for feature flags
- 📁 **Project Organization** - Associate feature flags with projects
- 🌍 **Environment Support** - Dev, Staging, and Production environments
- 🎯 **User Group Targeting** - Optional targeting by user groups
- 📊 **Swagger Documentation** - Interactive API documentation
- 🐳 **Docker Support** - Easy deployment with Docker Compose
- 🔄 **Database Migrations** - Alembic for schema management

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT with python-jose
- **Password Hashing**: bcrypt
- **Documentation**: Swagger/OpenAPI

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

### Using Docker (Recommended)

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd feature-flag-api
   ```

2. **Start the services**:
   ```bash
   docker-compose up -d
   ```

3. **Run migrations**:
   ```bash
   docker-compose exec api alembic upgrade head
   ```

4. **Access the API**:
   - API: http://localhost:8000
   - Swagger Docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup environment**:
   ```bash
   cp env.example .env
   # Edit .env with your database credentials
   ```

3. **Start PostgreSQL** (using Docker):
   ```bash
   docker run -d --name postgres \
     -e POSTGRES_DB=feature_flags \
     -e POSTGRES_USER=postgres \
     -e POSTGRES_PASSWORD=password \
     -p 5432:5432 \
     postgres:15
   ```

4. **Run migrations**:
   ```bash
   alembic upgrade head
   ```

5. **Start the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Authentication

- `POST /api/v1/auth/signup` - Create a new user account
- `POST /api/v1/auth/token` - Login and get JWT token
- `GET /api/v1/auth/me` - Get current user info

### Users (Admin only)

- `GET /api/v1/users/` - List all users
- `GET /api/v1/users/{user_id}` - Get user details
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### Projects

- `GET /api/v1/projects/` - List user's projects
- `POST /api/v1/projects/` - Create new project
- `GET /api/v1/projects/{project_id}` - Get project details
- `PUT /api/v1/projects/{project_id}` - Update project
- `DELETE /api/v1/projects/{project_id}` - Delete project

### Feature Flags

- `GET /api/v1/feature-flags/` - List feature flags (with filters)
- `POST /api/v1/feature-flags/` - Create new feature flag
- `GET /api/v1/feature-flags/{flag_id}` - Get feature flag details
- `PUT /api/v1/feature-flags/{flag_id}` - Update feature flag
- `DELETE /api/v1/feature-flags/{flag_id}` - Delete feature flag
- `GET /api/v1/feature-flags/project/{project_id}` - Get project's feature flags

## Usage Examples

### 1. Create a User Account

```bash
curl -X POST "http://localhost:8000/api/v1/auth/signup" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "username": "admin",
    "password": "password123",
    "role": "admin"
  }'
```

### 2. Login and Get Token

```bash
curl -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=password123"
```

### 3. Create a Project

```bash
curl -X POST "http://localhost:8000/api/v1/projects/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Web App",
    "description": "A modern web application"
  }'
```

### 4. Create a Feature Flag

```bash
curl -X POST "http://localhost:8000/api/v1/feature-flags/" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "new_ui",
    "description": "Enable new user interface",
    "is_enabled": true,
    "environment": "dev",
    "project_id": 1,
    "user_group_targeting": "{\"groups\": [\"beta_users\"]}"
  }'
```

### 5. List Feature Flags

```bash
curl -X GET "http://localhost:8000/api/v1/feature-flags/?project_id=1&environment=dev" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Database Schema

### Users
- `id` (Primary Key)
- `email` (Unique)
- `username` (Unique)
- `hashed_password`
- `role` (admin/developer)
- `is_active`
- `created_at`
- `updated_at`

### Projects
- `id` (Primary Key)
- `name`
- `description`
- `owner_id` (Foreign Key to Users)
- `created_at`
- `updated_at`

### Feature Flags
- `id` (Primary Key)
- `name`
- `description`
- `is_enabled`
- `environment` (dev/staging/prod)
- `project_id` (Foreign Key to Projects)
- `created_by_id` (Foreign Key to Users)
- `user_group_targeting` (JSON string)
- `created_at`
- `updated_at`

## Environment Variables

Create a `.env` file with the following variables:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/feature_flags
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Code Formatting

```bash
# Install formatting tools
pip install black isort

# Format code
black .
isort .
```

## Security Considerations

1. **Change the SECRET_KEY** in production
2. **Use HTTPS** in production
3. **Configure CORS** properly for your domain
4. **Use strong passwords** and consider password policies
5. **Implement rate limiting** for production use
6. **Add input validation** for user_group_targeting JSON
7. **Consider adding audit logs** for feature flag changes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details 