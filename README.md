**Português** · [English](README.en.md)

# 🚀 Kafka Event-Driven Project

Projeto de estudo de arquitetura orientada a eventos com **Apache Kafka**, **Python (FastAPI + aiokafka)**, **PostgreSQL** e **Docker**.

---

## 🧠 Objetivo

Demonstrar um fluxo de mensageria desacoplada, com persistência, resiliência e observabilidade:

```text
API (Producer) → Kafka (pedidos) → Consumer → Postgres
                                       └─ falhas → DLQ (pedidos-dlq)
```

---

## 🧩 Arquitetura

- **API (FastAPI)**: `POST /pedido` grava o pedido como `PENDENTE` no banco e publica o evento no Kafka; `GET /health` testa a conectividade com Kafka e banco (503 se degradado).
- **Kafka (modo KRaft)**: broker de eventos, sem Zookeeper. Tópicos `pedidos` e `pedidos-dlq`, criados por script de inicialização.
- **Consumer (worker)**: valida o evento, processa o pagamento com retry e backoff exponencial e marca o pedido como `PAGO`. Após esgotar as tentativas, envia para a DLQ e marca `FALHADO`.
- **PostgreSQL 16**: estado dos pedidos (SQLAlchemy async). Sem `DATABASE_URL`, cai para SQLite local.

---

## 📂 Estrutura do Projeto

```text
src/
├── api/        # API (producer)
├── consumer/   # worker (consumer)
├── core/       # config (Pydantic Settings), Kafka, banco, modelos, logs JSON
└── scripts/    # scripts auxiliares (criação de tópicos)
tests/          # pytest
```

---

## ⚙️ Requisitos

- Docker e Docker Compose
- Make (opcional, mas recomendado)
- Para lint/testes locais: Python e `pip install -r requirements.txt`

---

## 🚀 Como rodar

| Comando | O que faz |
|---|---|
| `make up` / `make up-d` | Sobe o ambiente (em primeiro plano / em background) |
| `make down` | Para os containers |
| `make clean` | Remove tudo, incluindo volumes |
| `make send` | Envia um evento de teste (`POST /pedido`) |
| `make logs`, `logs-api`, `logs-consumer` | Logs gerais, da API ou do consumer |

Ou manualmente: `curl -X POST http://localhost:8000/pedido`.

### Exemplo de fluxo

1. `POST /pedido` grava o pedido (`PENDENTE`) e publica no Kafka:

```json
{
  "pedido_id": "uuid",
  "status": "CRIADO"
}
```

2. O consumer processa (logs em JSON, com `pedido_id`, `duracao_ms` e `tentativa`) e o pedido passa a `PAGO`.

---

## 🔧 Configuração

Via variáveis de ambiente ou arquivo de ambiente local (`src/core/config.py`):

| Variável | Padrão |
|---|---|
| `KAFKA_BROKER` | `localhost:9092` |
| `TOPIC_PEDIDOS` / `TOPIC_DLQ` | `pedidos` / `pedidos-dlq` |
| `CONSUMER_GROUP` | `pagamento-service` |
| `RETRY_MAX` / `RETRY_BACKOFF_BASE_SECONDS` | `3` / `1.0` |
| `DATABASE_URL` | `sqlite+aiosqlite:///./kafka_project.db` |

---

## ✅ Qualidade

```bash
make lint     # ruff + mypy
make format   # ruff format + fix
make test     # pytest
```

O CI (GitHub Actions) roda lint, testes, cobertura e duplicações nos PRs para `develop`.

---

## 🔧 Debug e inspeção

```bash
make consumer-groups   # lista consumer groups
make describe-group    # detalha o grupo
make kafka-shell       # acessa o container Kafka
```

---

## 🧠 Conceitos aplicados

Event-Driven Architecture · Producer/Consumer · Kafka Topics · Consumer Groups · Offset Management (`auto_offset_reset=earliest`) · Retry com backoff e Dead Letter Queue · Comunicação assíncrona · Logs estruturados · Dockerização.

---

## 📋 Backlog e histórico

Planejamento em [BACKLOG.md](BACKLOG.md) e histórico de versões em [CHANGELOG.md](CHANGELOG.md).

---

## 👨‍💻 Autor

Projeto desenvolvido para estudo de Kafka, mensageria e arquitetura distribuída.
