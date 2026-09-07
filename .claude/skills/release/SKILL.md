---
name: release
description: Executa o processo de release do kafka-project (bump de versão, CHANGELOG, tag vX.Y.Z, back-merge) ponta a ponta. Invocação apenas pelo usuário — ex. "inicia o release", "lança a versão", "atualiza a tag".
disable-model-invocation: true
---

# Release do kafka-project

Processo determinístico — siga os passos na ordem, sem pular. Se algo não
bater com o esperado, **pare e pergunte** em vez de improvisar.

Política de versão: `docs/plano-versionamento.md` (SemVer + Conventional
Commits, sem sufixo `-SNAPSHOT`). Fonte da verdade da versão:
`[project] version` em `pyproject.toml`. Gotchas: `.junie/LEARNINGS.md`.

**Regra de ouro:** todo o processo roda numa `git worktree` isolada — a
working tree/branch ativa do usuário nunca é tocada. Nunca `git stash` na
working tree principal para destravar hook algum.

## 1. Pré-checagem

```bash
git fetch origin --tags
ULTIMA_TAG=$(git tag --sort=-v:refname | head -1)          # ex. v0.1.0
git merge-base --is-ancestor "$ULTIMA_TAG" origin/main && echo "OK: tag em main"
git show origin/main:pyproject.toml | grep '^version'
git log "$ULTIMA_TAG..origin/develop" --no-merges --format='%s'
```

Determinar a **próxima versão** pelos commits de `$ULTIMA_TAG..origin/develop`:

- algum `feat!:` ou `BREAKING CHANGE:` → bump **MAJOR**
- senão algum `feat:` → bump **MINOR**
- senão algum `fix:` → bump **PATCH**
- só `docs/chore/refactor/test` → **não há release a fazer**, pare e avise.

## 2. Confirmar a versão com o usuário

**Pare e use `AskUserQuestion`** mostrando a versão calculada (`vX.Y.Z`) e o
resumo dos commits. Só continue com confirmação explícita.

## 3. Worktree isolada

```bash
WT=/tmp/claude-release-vX.Y.Z
git worktree add "$WT" -b release/vX.Y.Z origin/develop
cd "$WT"
```

Todo passo daqui até o cleanup (passo 13) roda dentro de `$WT`.

## 4. Bump de versão

Editar `pyproject.toml`: `version = "X.Y.Z"` (sem sufixo).

## 5. CHANGELOG — delegar a um subagente Sonnet descartável

Não leia os commits na sessão principal. Delegue via Agent tool, `model:
"sonnet"` (agente novo, sem `subagent_type: "fork"`). Prompt autocontido com:

- `$ULTIMA_TAG` e o comando
  `git log $ULTIMA_TAG..origin/develop --no-merges --format='%s' | grep -E '^(feat|fix)'`.
- Instrução: **curar por tema, não 1 bullet por commit**; mesmo tom/tamanho
  da entrada mais recente de `CHANGELOG.md` (abrir como referência).
- Formato Keep a Changelog: `## [X.Y.Z] - YYYY-MM-DD` com `### Added` /
  `### Fixed` / `### Changed` (só seções com conteúdo).
- Devolver **só o bloco Markdown**, nada mais.

Inserir o bloco retornado logo acima da entrada `## [$ULTIMA_TAG]` (sem o `v`).

## 6. Lint + testes

```bash
make lint
make test
```

Ambos têm que passar limpo antes de prosseguir.

## 7. Commit

```bash
git add CHANGELOG.md pyproject.toml
git commit -m "chore(release): vX.Y.Z

<resumo de 3-5 linhas dos temas principais>"
```

Nunca `git add -A` — só os 2 arquivos do release.

## 8. Push + PR

```bash
git push -u origin release/vX.Y.Z
gh pr create --base main --head release/vX.Y.Z \
  --title "chore(release): vX.Y.Z" --body "..."
```

`--base main` **sempre explícito**.

## 9. Aguardar o CI

```bash
gh pr checks <numero-do-pr>
```

`Code Quality and Coverage` (quality.yml) é informativo — não bloqueia o
merge, mas espere terminar e confira que passou.

## 10. Confirmar o merge com o usuário

**Pare e use `AskUserQuestion`.** Merge em `main` é irreversível na prática
— confirmar sempre, mesmo que o usuário já tenha pedido "inicia o release".

## 11. Merge + tag

```bash
gh pr merge <numero-do-pr> --merge --delete-branch=false
git fetch origin
git tag vX.Y.Z origin/main      # sempre em origin/main, nunca na main local
git push origin vX.Y.Z
```

**Confirme com `AskUserQuestion` de novo antes do push da tag** — mesma
classe de ação irreversível.

## 12. Back-merge main → develop

```bash
git -C "$WT" fetch origin
git -C "$WT" checkout -B develop origin/develop
git -C "$WT" merge origin/main
git -C "$WT" push origin develop
```

Conflito em `CHANGELOG.md`/`pyproject.toml` quase sempre significa que um
release anterior pulou o back-merge — investigue a causa raiz.

## 13. Cleanup

```bash
git worktree remove "$WT" --force
```

## 14. Reportar ao usuário

Versão lançada, link do PR, tag publicada, `develop` de volta em sincronia
com `main`.
