[Português](README.md) · **English**

# 🚀 Kafka Event-Driven Project

A study project on event-driven architecture with **Apache Kafka**, **Python (FastAPI + aiokafka)**, **PostgreSQL** and **Docker**.

---

## 🧠 Goal

Demonstrate a decoupled messaging flow with persistence, resilience and observability:

```text
API (Producer) → Kafka (pedidos) → Consumer → Postgres
                                       └─ failures → DLQ (pedidos-dlq)
```

---

## 🧩 Architecture

- **API (FastAPI)**: `POST /pedido` stores the order as `PENDENTE` in the database and publishes the event to Kafka; `GET /health` checks Kafka and database connectivity (503 when degraded).
- **Kafka (KRaft mode)**: event broker, no Zookeeper. Topics `pedidos` and `pedidos-dlq`, created by an init script.
- **Consumer (worker)**: validates the event, processes the payment with retry and exponential backoff, and marks the order `PAGO`. After exhausting retries it sends it to the DLQ and marks it `FALHADO`.
- **PostgreSQL 16**: order state (async SQLAlchemy). Without `DATABASE_URL` it falls back to local SQLite.

---

## 📂 Project Structure

```text
src/
├── api/        # API (producer)
├── consumer/   # worker (consumer)
├── core/       # config (Pydantic Settings), Kafka, database, models, JSON logs
└── scripts/    # helper scripts (topic creation)
tests/          # pytest
```

---

## ⚙️ Requirements

- Docker and Docker Compose
- Make (optional, but recommended)
- For local lint/tests: Python and `pip install -r requirements.txt`

---

## 🚀 Running

| Command | What it does |
|---|---|
| `make up` / `make up-d` | Start the environment (foreground / background) |
| `make down` | Stop the containers |
| `make clean` | Remove everything, including volumes |
| `make send` | Send a test event (`POST /pedido`) |
| `make logs`, `logs-api`, `logs-consumer` | All logs, API logs or consumer logs |

Or manually: `curl -X POST http://localhost:8000/pedido`.

### Example flow

1. `POST /pedido` stores the order (`PENDENTE`) and publishes to Kafka:

```json
{
  "pedido_id": "uuid",
  "status": "CRIADO"
}
```

2. The consumer processes it (JSON logs with `pedido_id`, `duracao_ms` and `tentativa`) and the order becomes `PAGO`.

---

## 🔧 Configuration

Via environment variables or a local environment file (`src/core/config.py`):

| Variable | Default |
|---|---|
| `KAFKA_BROKER` | `localhost:9092` |
| `TOPIC_PEDIDOS` / `TOPIC_DLQ` | `pedidos` / `pedidos-dlq` |
| `CONSUMER_GROUP` | `pagamento-service` |
| `RETRY_MAX` / `RETRY_BACKOFF_BASE_SECONDS` | `3` / `1.0` |
| `DATABASE_URL` | `sqlite+aiosqlite:///./kafka_project.db` |

---

## ✅ Quality

```bash
make lint     # ruff + mypy
make format   # ruff format + fix
make test     # pytest
```

CI (GitHub Actions) runs lint, tests, coverage and duplication checks on PRs to `develop`.

---

## 🔧 Debug and inspection

```bash
make consumer-groups   # list consumer groups
make describe-group    # describe the group
make kafka-shell       # shell into the Kafka container
```

---

## 🧠 Concepts applied

Event-Driven Architecture · Producer/Consumer · Kafka Topics · Consumer Groups · Offset Management (`auto_offset_reset=earliest`) · Retry with backoff and Dead Letter Queue · Asynchronous communication · Structured logs · Containerization.

---

## 📋 Backlog and history

Planning in [BACKLOG.md](BACKLOG.md); release history in [CHANGELOG.md](CHANGELOG.md).

---

## 👨‍💻 Author

Project built to study Kafka, messaging and distributed architecture.
