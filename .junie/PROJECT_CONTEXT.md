# Kafka Project — Contexto do Projeto

## Stack

- **Backend:** Python 3.11 + FastAPI (producer) + kafka-python (consumer)
- **Mensageria:** Apache Kafka em modo KRaft (sem Zookeeper)
- **Infra:** Docker Compose

## Arquitetura

```
API (FastAPI/Producer) -> Kafka -> Consumer (Worker Python)
```

## Status Atual

Prototipo funcional de event-driven architecture. Producer envia eventos de
`pedido` e consumer processa. Sem persistencia, sem testes, sem observabilidade.

## Proximos Passos (ver BACKLOG.md)

1. Adicionar ferramentas de qualidade (ruff, mypy, pytest)
2. Migrar de kafka-python para aiokafka ou confluent-kafka
3. Implementar retry e DLQ
4. Adicionar PostgreSQL e persistir pedidos
5. Logs estruturados com structlog
