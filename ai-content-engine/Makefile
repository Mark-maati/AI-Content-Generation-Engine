.PHONY: install lint test migrate up down health seed

install:
	pip install -e shared[dev]
	pip install -e services/ingestion
	pip install -e services/prompt_engine
	pip install -e services/model_layer
	pip install -e services/output_validation
	pip install -e services/persistence

lint:
	ruff check .
	black --check .
	mypy shared/shared services/ingestion/ingestion services/prompt_engine/prompt_engine services/model_layer/model_layer services/output_validation/output_validation services/persistence/persistence

format:
	ruff check --fix .
	black .

test:
	pytest tests/ -v
	pytest services/ingestion/tests/ -v
	pytest services/prompt_engine/tests/ -v
	pytest services/model_layer/tests/ -v
	pytest services/output_validation/tests/ -v
	pytest services/persistence/tests/ -v

migrate:
	alembic upgrade head

migrate-down:
	alembic downgrade -1

migrate-create:
	alembic revision --autogenerate -m "$(msg)"

up:
	docker compose up -d

down:
	docker compose down

up-infra:
	docker compose up -d postgres redis kafka zookeeper elasticsearch

health:
	@echo "Checking service health..."
	@curl -sf http://localhost:8001/api/v1/health || echo "Ingestion: DOWN"
	@curl -sf http://localhost:8002/api/v1/health || echo "Prompt Engine: DOWN"
	@curl -sf http://localhost:8003/api/v1/health || echo "Model Layer: DOWN"
	@curl -sf http://localhost:8004/api/v1/health || echo "Output Validation: DOWN"
	@curl -sf http://localhost:8005/api/v1/health || echo "Persistence: DOWN"
