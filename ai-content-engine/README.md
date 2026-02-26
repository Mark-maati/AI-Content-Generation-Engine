# AI Content Generation Engine

An enterprise-grade, event-driven AI Content Generation Engine built with FastAPI, Kafka, and PostgreSQL. Designed for high-throughput, reliable, and cost-aware large language model (LLM) orchestration.

## Architecture Highlights
- **Event-Driven Pipeline**: Decoupled microservices communicating asynchronously via Apache Kafka.
- **Cost-Aware Routing**: Intelligent LLM routing (OpenAI, Anthropic, Gemini) balancing priority, payload complexity, and cost.
- **Strict Output Validation**: Multi-pass JSON extraction and stringent JSonschema validations.
- **Complete Persistence**: PostgreSQL state-management for generations coupled tightly with stateless consumers.

## Services Overview
| Service | Port | Description |
|-----------|------|-------------|
| `ingestion` | 8000 | Accepts configuration, handles rate limiting, and queues structural generation parameters. |
| `prompt-engine` | 8001 | Fetches templates and compiles Jinja2-based prompts. |
| `model-layer` | 8002 | Dynamically routes prompts to LLM providers and collects raw responses. |
| `output-validation` | 8003 | Parses raw output and validates against explicit JSON schemas. |
| `persistence` | 8004 | Stores terminal metadata and output artifacts in PostgreSQL & Elasticsearch. |

## Quickstart (Locally via Docker)

This repository includes a unified `docker-compose.yml` that stands up the entire cluster (Stateful Backends + 5 Custom Microservices).

### Prerequisites
- Docker & Docker Compose
- Minimum 8GB RAM allocated to Docker

### 1. Configure Environment
Copy the example environment variables:
```bash
cp .env.example .env
```
*(Add your provider API keys like `OPENAI_API_KEY` to the `.env` if you have implemented your concrete Adapters).*

### 2. Stand Up Core Infrastructure 
To start the backing databases (Kafka, ZooKeeper, Postgres, Redis, Elasticsearch):
```bash
docker-compose up -d postgres kafka zookeeper redis elasticsearch
```

### 3. Build & Run the Microservices
To build the unified Python 3.12 Dockerfile and boot the 5 stateless API/Consumer containers:
```bash
docker-compose up -d --build ingestion prompt-engine model-layer output-validation persistence
```

### 4. Verify System
Query the ingestion health check:
```bash
curl http://localhost:8000/api/v1/health
```

---

## Technical Stack
- **Framework**: FastAPI (Async API), Uvicorn
- **System Layer**: Python 3.12, UV (Fast packaging), Pydantic V2
- **Data Layer**: SQLAlchemy 2.0 (Async), PostgreSQL, Elasticsearch
- **Event Bus**: Apache Kafka (`aiokafka`)

## Implementation Standards
This codebase strictly adheres to standard structural validations, SQL injection prevention parameterized queries, and immutable object patterns across domains.
