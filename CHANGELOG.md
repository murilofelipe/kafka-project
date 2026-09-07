# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-09-07
### Added
- Banco de dados relacional: PostgreSQL via SQLAlchemy async, com engine/session/`init_models()`/`ping()`, criação de tabelas no lifespan do FastAPI e serviço `db` (postgres:16-alpine) no docker-compose (Stories 3.1 e 3.2).
- Persistência do estado do pedido: modelo `Pedido`, gravação como `PENDENTE` no `POST /pedido` antes de publicar o evento, e transição para `PAGO` no sucesso ou `FALHADO` ao cair na DLQ (Story 3.2).
- Resiliência do consumer: retry com backoff exponencial (`retry_max` tentativas) e Dead Letter Queue `pedidos-dlq` com producer dedicado, mais validação do evento antes do processamento (Story 2.2).
- Configuração dinâmica com Pydantic Settings: classe `Settings` central para Kafka, retry/DLQ e `database_url`, substituindo `os.getenv` (Story 4.1).
- Observabilidade: logs estruturados em JSON (`JsonFormatter` + `setup_logging`) com metadados (`pedido_id`, `duracao_ms`, `tentativa`) no producer, consumer e `kafka_config`; endpoint `GET /health` que testa conectividade com Kafka e banco (503 se degradado) (Story 4.2).
- Suíte de testes automatizados com pytest cobrindo `Settings`, serialização Kafka, retry do producer, `POST /pedido` e `processar_evento`, com integração Kafka mockada e cobertura via `make test` (Story 1.2).
- Tooling de qualidade: configuração de ruff, mypy e pytest em `pyproject.toml`, alvos `make lint/format/test` e workflows de CI que rodam ruff/mypy/pytest, cobertura e duplicações em PRs para `develop` (Story 1.1).
- Skill `/release` para o processo de release ponta a ponta (bump de versão, changelog, PR para `main`, tag e back-merge).

### Changed
- Cliente Kafka migrado de `kafka-python` para `aiokafka`: producer/consumer assíncronos com retry, producer no lifespan do FastAPI com `send_and_wait`, e consumer com `async for` (Story 2.1).

## [0.1.0] - 2026-07-05
### Added
- Initial project planning, architecture definition and backlog setup.
