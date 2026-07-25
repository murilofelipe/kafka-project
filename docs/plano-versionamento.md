# Plano — Política de Versionamento
### kafka-project · SemVer · Conventional Commits · Tags · CHANGELOG

Este projeto adota a política de versionamento baseada no padrão SemVer (Semantic Versioning) e Conventional Commits, replicada a partir do padrão estabelecido no `sition-web`.

## 1. Convenção Adotada
- **Versão**: `MAJOR.MINOR.PATCH` (SemVer)
- **Incremento**:
  - `fix:` -> PATCH (ex: 0.1.0 -> 0.1.1)
  - `feat:` -> MINOR (ex: 0.1.0 -> 0.2.0)
  - `feat!:` / `BREAKING CHANGE:` -> MAJOR (ex: 0.1.0 -> 1.0.0)
  - `docs/chore/refactor/test` -> sem incremento de versão.
- **Marcação**: Tag Git `vX.Y.Z` na branch de release/produção.
- **CHANGELOG.md**: Arquivo na raiz no formato Keep a Changelog.
