# CLAUDE.md — Kafka Event-Driven Project

> Carregado automaticamente no inicio de toda sessao neste projeto.

## Comece pelo snapshot (economia de contexto)

Para a maioria das tarefas, `docs/context-snapshot.md` traz o estado atual e
regras — comece por ele.

## Leia antes de tarefas que toquem no assunto

1. `.junie/PROJECT_CONTEXT.md` — stack, convencoes, status atual
2. `.junie/LEARNINGS.md` — erros recorrentes e regras aprendidas
3. `BACKLOG.md` — planejamento de melhorias

## Regras deste projeto

- FastAPI para a API (producer), worker Python separado (consumer).
- Kafka em modo KRaft (sem Zookeeper).
- Topicos criados via script de inicializacao.
- Consumer configurado com `auto_offset_reset=earliest`.
- `PYTHONUNBUFFERED=1` para logs no Docker.

## Ao final de uma sessao que mudou arquitetura ou aprendizado

Ofereca atualizar `.junie/PROJECT_CONTEXT.md` e `.junie/LEARNINGS.md`.
