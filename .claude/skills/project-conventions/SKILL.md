---
name: project-conventions
description: Regras do kafka-project (FastAPI producer, Kafka consumer, Docker). Conhecimento de fundo.
user-invocable: false
---

# Convencoes do kafka-project

## Arquitetura

- `src/api/` — FastAPI producer
- `src/consumer/` — worker Python consumer
- `src/core/` — configuracao Kafka compartilhada
- `src/scripts/` — scripts auxiliares (criacao de topicos)

## Kafka

- Modo KRaft (sem Zookeeper).
- Topicos criados via `src/scripts/create-topics.sh`.
- Consumer com `auto_offset_reset=earliest` e `enable_auto_commit=True`.

## Docker

- `docker-compose.yml` com 4 servicos: kafka, kafka-init, api, consumer.
- `PYTHONUNBUFFERED=1` para logs em tempo real.

## Processo

- Conventional Commits em pt-BR.
- Commitar documentacao separada do codigo.
