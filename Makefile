.PHONY: help build up down restart logs test clean setup

# Default target
help:
	@echo "RAG System - Available Commands"
	@echo "================================"
	@echo "setup     - Initial setup (create .env from template)"
	@echo "build     - Build Docker containers"
	@echo "up        - Start all services"
	@echo "down      - Stop all services"
	@echo "restart   - Restart all services"
	@echo "logs      - View logs from all services"
	@echo "logs-api  - View API logs only"
	@echo "logs-db   - View database logs only"
	@echo "test      - Run API tests"
	@echo "clean     - Remove containers, volumes, and images"
	@echo "shell-api - Open shell in API container"
	@echo "shell-db  - Open PostgreSQL shell"

# Initial setup
setup:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✓ Created .env file from template"; \
		echo "⚠ Please edit .env and add your OPENAI_API_KEY"; \
	else \
		echo "✓ .env file already exists"; \
	fi
	@mkdir -p uploads
	@echo "✓ Created uploads directory"

# Build containers
build:
	docker-compose build

# Start services
up:
	docker-compose up -d
	@echo "✓ Services started"
	@echo "API: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

# Start services with logs
up-logs:
	docker-compose up

# Stop services
down:
	docker-compose down

# Restart services
restart:
	docker-compose restart

# View all logs
logs:
	docker-compose logs -f

# View API logs
logs-api:
	docker-compose logs -f api

# View database logs
logs-db:
	docker-compose logs -f db

# Run tests
test:
	@chmod +x test_api.sh
	@./test_api.sh

# Run Phase 2 tests
test-chat:
	@echo "Running Phase 2 chat tests..."
	@docker-compose exec api python test_chat.py

# Run Phase 3 tests
test-documents:
	@echo "Running Phase 3 document tests..."
	@docker-compose exec api python test_documents.py

# Run Phase 4 tests
test-database:
	@echo "Running Phase 4 database tests..."
	@docker-compose exec api python test_database.py

# Run Phase 5 tests
test-search:
	@echo "Running Phase 5 search tests..."
	@docker-compose exec api python test_search.py

# Run Phase 6 tests (Final Phase!)
test-rag:
	@echo "Running Phase 6 RAG tests..."
	@docker-compose exec api python test_rag.py

# Run all tests
test-all: test test-chat test-documents test-database test-search test-rag
	@echo ""
	@echo "🎉 All phases tested!"

# Clean everything
clean:
	docker-compose down -v --rmi all
	@echo "✓ Cleaned all containers, volumes, and images"

# Clean volumes only
clean-volumes:
	docker-compose down -v
	@echo "✓ Cleaned volumes"

# Open shell in API container
shell-api:
	docker-compose exec api /bin/bash

# Open PostgreSQL shell
shell-db:
	docker-compose exec db psql -U raguser -d ragdb

# Run database migrations
migrate:
	@echo "Running database migrations..."
	@docker-compose exec api python -c "from database import db_manager; db_manager.create_tables(); print('✓ Tables created')"

# Check database status
db-status:
	@echo "Checking database status..."
	@docker-compose exec api python -c "from database import db_manager; print('Documents:', db_manager.get_table_count('documents')); print('Chunks:', db_manager.get_table_count('document_chunks'))"

# Check service status
status:
	docker-compose ps

# Rebuild and restart
rebuild: down build up
	@echo "✓ Rebuilt and restarted all services"