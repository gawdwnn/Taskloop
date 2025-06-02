.PHONY: help install test lint format run migrate clean services-up services-down services-stop services-status venv

# Variables
PYTHON = python3.12
PIP = pip3.12
UVICORN = uvicorn
ALEMBIC = alembic
DOCKER_COMPOSE = docker compose
VENV_DIR = venv
VENV_BIN = $(VENV_DIR)/bin
VENV_ACTIVATE = . $(VENV_BIN)/activate

help: ## Display this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk -F ':|##' '/^[^\t].+?:.*?##/ { printf "  %-20s %s\n", $$1, $$NF }' $(MAKEFILE_LIST)

venv: ## Create virtual environment if it doesn't exist
	@if [ ! -d "$(VENV_DIR)" ]; then \
		echo "Creating virtual environment with Python 3.12..."; \
		$(PYTHON) -m venv $(VENV_DIR) || (echo "\nError: Python 3.12 not found. Please install it with: brew install python@3.12" && exit 1); \
	fi

install: venv ## Install dependencies in virtual environment
	@echo "Installing dependencies..."
	@$(VENV_ACTIVATE) && $(VENV_BIN)/pip install -r requirements.txt

test: venv ## Run tests
	@$(VENV_ACTIVATE) && pytest

lint: venv ## Run linting
	@$(VENV_ACTIVATE) && pylint app tests

format: venv ## Format code
	@$(VENV_ACTIVATE) && black app tests

services-up: ## Start all services (PostgreSQL, Redis)
	$(DOCKER_COMPOSE) up -d db redis

services-down: ## Stop and remove all services
	$(DOCKER_COMPOSE) down

services-stop: ## Stop services without removing them (can be restarted later)
	$(DOCKER_COMPOSE) stop

services-status: ## Check status of all services
	$(DOCKER_COMPOSE) ps

# Docker environment commands
docker-dev: services-up ## Start development environment
	ENVIRONMENT=development $(DOCKER_COMPOSE) up -d api

docker-prod: services-up ## Start production environment
	ENVIRONMENT=production $(DOCKER_COMPOSE) up -d api

docker-logs: ## View Docker container logs
	$(DOCKER_COMPOSE) logs -f 

run: venv services-status ## Run development server (ensures services are up)
	@echo "Starting FastAPI server..."
	@$(VENV_ACTIVATE) && $(VENV_BIN)/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

migrate: venv ## Run database migrations
	@PYTHONPATH=$(shell pwd) $(VENV_ACTIVATE) && $(VENV_BIN)/alembic upgrade head

migrate-create: venv ## Create new migration
	@PYTHONPATH=$(shell pwd) $(VENV_ACTIVATE) && $(VENV_BIN)/alembic revision --autogenerate -m "$(message)"

migrate-downgrade: venv ## Downgrade database
	@PYTHONPATH=$(shell pwd) $(VENV_ACTIVATE) && $(VENV_BIN)/alembic downgrade -1

migrate-history: venv ## List all migrations
	@$(VENV_ACTIVATE) && $(VENV_BIN)/alembic history

clean: ## Clean up Python cache files
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".coverage" -exec rm -r {} +
	find . -type d -name "htmlcov" -exec rm -r {} +

db-reset: venv ## Reset database (drop and recreate)
	@$(VENV_ACTIVATE) && $(VENV_BIN)/alembic downgrade base
	@$(VENV_ACTIVATE) && $(VENV_BIN)/alembic upgrade head

dev: install services-up run ## Install dependencies, start services, and run development server
