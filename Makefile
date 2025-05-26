.PHONY: help install test lint format run migrate clean services-up services-down services-stop services-status

# Variables
PYTHON = python3
PIP = pip3
UVICORN = uvicorn
ALEMBIC = alembic
DOCKER_COMPOSE = docker compose -f .devcontainer/docker-compose.yml --env-file=.env

help: ## Display this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk -F ':|##' '/^[^\t].+?:.*?##/ { printf "  %-20s %s\n", $$1, $$NF }' $(MAKEFILE_LIST)

install: ## Install dependencies
	$(PIP) install -r requirements.txt

test: ## Run tests
	pytest

lint: ## Run linting
	pylint app tests

format: ## Format code
	black app tests

services-up: ## Start all services (PostgreSQL, Redis)
	$(DOCKER_COMPOSE) up -d db redis

services-down: ## Stop and remove all services
	$(DOCKER_COMPOSE) down

services-stop: ## Stop services without removing them (can be restarted later)
	$(DOCKER_COMPOSE) stop

services-status: ## Check status of all services
	$(DOCKER_COMPOSE) ps

run: services-status ## Run development server (ensures services are up)
	@echo "Starting FastAPI server..."
	$(UVICORN) app.main:app --reload --host 0.0.0.0 --port 8000

migrate: ## Run database migrations
	$(ALEMBIC) upgrade head

migrate-create: ## Create new migration
	$(ALEMBIC) revision --autogenerate -m "$(message)"

migrate-downgrade: ## Downgrade database
	$(ALEMBIC) downgrade -1

clean: ## Clean up Python cache files
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +

db-reset: ## Reset database (drop and recreate)
	$(ALEMBIC) downgrade base
	$(ALEMBIC) upgrade head

dev: install services-up run ## Install dependencies, start services, and run development server 