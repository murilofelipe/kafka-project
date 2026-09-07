# Kafka Project — Aprendizados

> Regras aprendidas durante o desenvolvimento.

## Kafka

- Migrado de kafka-python para aiokafka (Story 2.1). Producer/consumer sao
  assincronos: usar `await ...send_and_wait()` e `async for msg in consumer`.
  Producer da API vive no `lifespan` do FastAPI; consumer roda em `asyncio.run`.
- Consumer com `auto_offset_reset=earliest` garante processar mensagens
  perdidas, mas pode reprocessar duplicatas.

## Docker

- `PYTHONUNBUFFERED=1` e essencial para ver logs em tempo real no Docker.
- kafka-init depende do script `create-topics.sh` para criar topicos.

## Codigo

- Nao ha testes automatizados. Diretorio `tests/` esta vazio.
- Diretorio `src/producer/` esta vazio — logica de producao vive em `src/api/main.py`.
