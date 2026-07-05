---
name: commit-project
description: Cria commits no padrao do kafka-project (Conventional Commits em pt-BR).
disable-model-invocation: true
---

# Commit no padrao kafka-project

## Formato

```
<tipo>(<escopo>): <descricao em pt-BR>
```

- **tipo:** `feat`, `fix`, `chore`, `refactor`, `docs`, `test`.
- **escopo:** `producer`, `consumer`, `kafka`, `api`, `infra`.

## Regras

- Documentacao em commit separado do codigo.
- Staging cirurgico.
- Nao commitar direto em `main`/`develop`.
