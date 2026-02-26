# AI Content Generation Engine

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade, event-driven AI Content Generation Engine built with FastAPI, Kafka, and PostgreSQL. Designed for high-throughput, reliable, and cost-aware large language model (LLM) orchestration.

## 🏗️ Architecture Overview

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌──────────────┐    ┌─────────────┐
│  Ingestion  │───▶│   Prompt    │───▶│    Model    │───▶│    Output    │───▶│ Persistence │
│   Service   │    │   Engine    │    │    Layer    │    │  Validation  │    │   Service   │
└─────────────┘    └─────────────┘    └─────────────┘    └──────────────┘    └─────────────┘
       │                  │                  │                  │                  │
       └──────────────────┴──────────────────┴──────────────────┴──────────────────┘
                                         │
                                   Apache Kafka
                              (Event-Driven Pipeline)
```

### Key Features

- **Event-Driven Pipeline**: Decoupled microservices communicating asynchronously via Apache Kafka
- **Cost-Aware Routing**: Intelligent LLM routing (OpenAI, Anthropic, Gemini) balancing priority, payload complexity, and cost
- **Strict Output Validation**: Multi-pass JSON extraction and stringent JSON Schema validations
- **Complete Persistence**: PostgreSQL state-management with stateless consumers
- **Horizontal Scalability**: Each service scales independently based on load
- **Fault Tolerance**: Automatic retries, dead-letter queues, and graceful degradation

## 📦 Services Overview

| Service | Port | Description |
|---------|------|-------------|
| `ingestion` | 8000 | Accepts requests, handles rate limiting, validates input, and queues generation parameters |
| `prompt-engine` | 8001 | Fetches templates and compiles Jinja2-based prompts with variable substitution |
| `model-layer` | 8002 | Dynamically routes prompts to LLM providers and collects raw responses |
| `output-validation` | 8003 | Parses raw LLM output and validates against explicit JSON schemas |
| `persistence` | 8004 | Stores generation metadata and output artifacts in PostgreSQL & Elasticsearch |

## 🚀 Quickstart

### Prerequisites

- Docker & Docker Compose (v2.0+)
- Minimum 8GB RAM allocated to Docker
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/Mark-maati/AI-Content-Generation-Engine.git
cd AI-Content-Generation-Engine/ai-content-engine
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Add your LLM provider API keys to `.env`:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GOOGLE_API_KEY=...
```

### 3. Start Infrastructure

Start the backing services (Kafka, ZooKeeper, PostgreSQL, Redis, Elasticsearch):

```bash
docker-compose up -d postgres kafka zookeeper redis elasticsearch
```

### 4. Build & Run Microservices

```bash
docker-compose up -d --build ingestion prompt-engine model-layer output-validation persistence
```

### 5. Verify System

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Expected response:
# {"status": "healthy", "service": "ingestion", "timestamp": "..."}
```

## 📡 API Usage

### Create a Generation Request

```bash
curl -X POST http://localhost:8000/api/v1/generations \
  -H "Content-Type: application/json" \
  -d '{
    "template_id": "uuid-of-template",
    "parameters": {
      "topic": "artificial intelligence",
      "tone": "professional"
    },
    "options": {
      "mode": "async",
      "priority": "normal"
    }
  }'
```

### Get Generation Status

```bash
curl http://localhost:8000/api/v1/generations/{generation_id}
```

### List Templates

```bash
curl http://localhost:8000/api/v1/templates
```

## 🛠️ Development

### Local Development Setup

```bash
# Install dependencies using UV (recommended)
pip install uv
uv sync

# Or using pip
pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start a service locally
uvicorn services.ingestion.ingestion.main:app --reload --port 8000
```

### Running Tests

```bash
# Unit tests
pytest services/ingestion/tests/
pytest services/prompt_engine/tests/
pytest services/model_layer/tests/

# End-to-end tests
pytest tests/e2e/
```

### Using Make Commands

```bash
make dev          # Start development environment
make test         # Run all tests
make lint         # Run linters
make format       # Format code
make migrate      # Run database migrations
```

## 🏛️ Project Structure

```
ai-content-engine/
├── docker-compose.yml      # Full stack orchestration
├── Dockerfile              # Base service image
├── alembic.ini             # Database migration config
├── pyproject.toml          # Python project config
├── requirements.txt        # Dependencies
├── shared/                 # Shared libraries
│   ├── config.py           # Central configuration
│   ├── database.py         # Database connections
│   ├── events/             # Kafka event schemas
│   ├── kafka/              # Kafka producer/consumer
│   ├── middleware/         # Auth, correlation, error handling
│   ├── models/             # SQLAlchemy models
│   └── schemas/            # Pydantic schemas
├── services/
│   ├── ingestion/          # Input ingestion service
│   ├── prompt_engine/      # Prompt compilation service
│   ├── model_layer/        # LLM routing service
│   ├── output_validation/  # Output validation service
│   └── persistence/        # Storage service
└── tests/
    └── e2e/                # End-to-end tests
```

## ⚙️ Technical Stack

| Layer | Technology |
|-------|-----------|
| **API Framework** | FastAPI (async), Uvicorn |
| **Language** | Python 3.12 |
| **Validation** | Pydantic V2 |
| **Database** | PostgreSQL 15, SQLAlchemy 2.0 (async) |
| **Message Queue** | Apache Kafka (aiokafka) |
| **Caching** | Redis |
| **Search** | Elasticsearch |
| **Containerization** | Docker, Docker Compose |

## 📊 Performance Targets

| Metric | Target |
|--------|--------|
| P50 Latency (input validation) | < 200ms |
| P95 Queue-to-Completion | < 30s |
| Concurrent Requests | 1,000+ per deployment |
| Burst Capacity | 10x with graceful degradation |
| Monthly Uptime | 99.9% |

## 🔒 Security Features

- JWT-based authentication
- Role-based access control (RBAC)
- Input sanitization and XSS prevention
- SQL injection prevention via parameterized queries
- Rate limiting per user/organization
- Audit logging for all operations

## 📝 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://...` |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker addresses | `localhost:9092` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` |
| `OPENAI_API_KEY` | OpenAI API key | - |
| `ANTHROPIC_API_KEY` | Anthropic API key | - |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📚 Documentation

- [Product Requirements Document](../AI-Content-Generation-Engine-PRD.md) - Detailed system specifications
- [API Documentation](http://localhost:8000/docs) - Interactive Swagger UI (when running locally)

---

Built with ❤️ for enterprise AI content generation
