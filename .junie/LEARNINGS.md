# Kafka Project — Aprendizados

> Regras aprendidas durante o desenvolvimento.

## Kafka

- kafka-python esta desatualizado e pode ter problemas com Python 3.12+.
  Planejar migracao para aiokafka ou confluent-kafka.
- Consumer com `auto_offset_reset=earliest` garante processar mensagens
  perdidas, mas pode reprocessar duplicatas.

## Docker

- `PYTHONUNBUFFERED=1` e essencial para ver logs em tempo real no Docker.
- kafka-init depende do script `create-topics.sh` para criar topicos.

## Codigo

- Nao ha testes automatizados. Diretorio `tests/` esta vazio.
- Diretorio `src/producer/` esta vazio — logica de producao vive em `src/api/main.py`.
