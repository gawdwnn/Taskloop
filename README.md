# Task Management API

A multi-tenant task management API built with FastAPI, SQLAlchemy, and PostgreSQL.

## Features

- Multi-tenant architecture with data isolation
- JWT-based authentication
- Task management with status tracking
- User management within tenant context
- Role-based access control
- RESTful API design

## Tech Stack

- FastAPI - Web framework
- SQLAlchemy - ORM
- PostgreSQL - Database
- Redis - Caching
- Alembic - Database migrations
- Pydantic - Data validation
- JWT - Authentication
- Pytest - Testing

## Development Environment

This project uses Dev Containers to provide a consistent development environment. The setup includes:

- Python 3.12 development environment
- PostgreSQL 16 database
- Redis 7 cache
- VS Code/Cursor extensions for Python, Docker, and PostgreSQL
- Git and GitHub CLI tools

### Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop)
- [VS Code](https://code.visualstudio.com/) or [Cursor](https://cursor.sh/)
- [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Getting Started

1. Clone the repository:

```bash
git clone <repository-url>
cd task-management-api
```

2. Open in VS Code/Cursor:

```bash
code .  # For VS Code
# or
cursor .  # For Cursor
```

3. When prompted, click "Reopen in Container" or use the command palette (F1) and select "Dev Containers: Reopen in Container"

4. The development container will be built and started automatically. This includes:

   - Setting up the Python environment
   - Installing dependencies
   - Starting PostgreSQL and Redis services
   - Configuring VS Code/Cursor extensions

5. Once the container is ready, you can:
   - Run the development server: `uvicorn app.main:app --reload`
   - Access the API documentation: <http://localhost:8000/docs>
   - Connect to PostgreSQL using the connection details in the environment variables
   - Use Redis for caching

### Services

The development environment includes the following services:

- **App Server**: FastAPI application (port 8000)
- **PostgreSQL**: Database server (port 5432)
  - Username: postgres
  - Password: postgres
  - Database: task_management
- **Redis**: Cache server (port 6379)

### Database Management

The PostgreSQL database is automatically created and configured. Data is persisted in a Docker volume.

To reset the database:

1. Stop the containers
2. Remove the volumes:

```bash
docker-compose -f .devcontainer/docker-compose.yml down -v
```

3. Reopen in container

### Project Structure

```
app/
├── api/            # API routes
├── core/           # Core functionality
├── db/             # Database configuration
├── models/         # SQLAlchemy models
├── schemas/        # Pydantic schemas
├── services/       # Business logic
└── utils/          # Utility functions
tests/              # Test files
.devcontainer/      # Dev Container configuration
```

## API Documentation

Once the server is running, visit:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>

## Testing

Run tests with:

```bash
pytest
```

## Development Commands

The project includes a Makefile with common development commands:

```bash
# Show all available commands
make help

# Service Management
make services-up      # Start PostgreSQL and Redis
make services-down    # Stop all services
make services-status  # Check service status

# Development
make install         # Install dependencies
make run            # Run development server (requires services to be up)
make dev            # Install dependencies, start services, and run server

# Code Quality
make test           # Run tests
make format         # Format code
make lint           # Run linting

# Database
make migrate        # Run database migrations
make migrate-create message="migration message"  # Create new migration
make db-reset       # Reset database

# Maintenance
make clean          # Clean up Python cache files
```

You can also use these commands through VS Code/Cursor tasks:

1. Press `Cmd/Ctrl + Shift + P`
2. Type "Tasks: Run Task"
3. Select the desired task

## Environment Variables and Secrets Management

The application uses environment variables for configuration and secrets management. Here's how it works:

### Local Development

1. Create a `.env` file in the project root (it's gitignored)
2. Copy the example values from `app/config.py` and modify as needed
3. Never commit the `.env` file to version control

### Environment Variables

The following environment variables are used:

#### Database Configuration

- `POSTGRES_USER`: PostgreSQL username
- `POSTGRES_PASSWORD`: PostgreSQL password
- `POSTGRES_DB`: Database name
- `DATABASE_URL`: Full database URL (auto-generated if not provided)

#### Redis Configuration

- `REDIS_URL`: Redis connection URL

#### Application Configuration

- `APP_ENV`: Environment (development/production)
- `DEBUG`: Debug mode
- `SECRET_KEY`: Application secret key
- `API_V1_PREFIX`: API version prefix

#### Security

- `JWT_SECRET_KEY`: JWT signing key
- `JWT_ALGORITHM`: JWT algorithm
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration

### Production Deployment

For production:

1. Use a secure secrets management service (e.g., AWS Secrets Manager, HashiCorp Vault)
2. Never use default values for secrets
3. Rotate secrets regularly
4. Use different secrets for different environments

### Accessing Settings

In your code, import the settings:

```python
from app.core.config import settings

# Use settings
database_url = settings.DATABASE_URL
jwt_secret = settings.JWT_SECRET_KEY
```
