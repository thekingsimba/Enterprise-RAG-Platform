.PHONY: help build up down logs shell migrate test clean

help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make logs     - View logs"
	@echo "  make shell    - Open backend shell"
	@echo "  make migrate  - Run database migrations"
	@echo "  make test     - Run tests"
	@echo "  make clean    - Clean up containers and volumes"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started. Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"
	@echo "Flower: http://localhost:5555"

down:
	docker-compose down

logs:
	docker-compose logs -f

shell:
	docker-compose exec backend bash

migrate:
	docker-compose exec backend alembic upgrade head

test:
	docker-compose exec backend pytest

clean:
	docker-compose down -v
	docker system prune -f


