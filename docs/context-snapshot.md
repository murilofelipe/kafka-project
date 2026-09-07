# Kafka Project — Snapshot de Contexto

> Leia isto primeiro em toda sessao.

## O que e

Projeto de estudo de arquitetura orientada a eventos com Apache Kafka,
FastAPI (producer) e worker Python (consumer). Dockerizado.

## Estado atual

Producer/consumer assincronos (aiokafka). Pedidos persistidos em Postgres
(SQLAlchemy async), retry com backoff + DLQ (`pedidos-dlq`), config via
Pydantic Settings (`src/core/config.py`), logs JSON estruturados e
endpoint `/health`. Testes em `tests/` (pytest, `make test`).

## Regras

- Kafka em modo KRaft, sem Zookeeper.
- Topicos criados via script de inicializacao.
- Conventional Commits em pt-BR.
