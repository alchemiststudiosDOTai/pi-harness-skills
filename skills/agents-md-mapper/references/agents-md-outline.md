# AGENTS.md Outline

Use this outline only when repository evidence supports each section. Remove unsupported headings rather than filling them with guesses.

```md
# AGENTS.md

## Project Overview
- One or two bullets on what the repository is and what it primarily ships

## Where To Start
- Primary onboarding doc: `README.md`
- Primary architecture doc: `ARCHITECTURE.md`
- Primary docs index: `docs/`

## Repository Map
- `src/` - main product code
- `tests/` - automated tests
- `docs/` - user and developer docs
- `.github/workflows/` - CI workflows

## Commands
- `...` - build
- `...` - test
- `...` - lint
- `...` - local run command

## Boundaries
- Domain or package boundaries backed by current layout or enforcement config

## Sources Of Truth
- `README.md`
- `ARCHITECTURE.md`
- `docs/...`
- CI workflow or task runner config paths

## Change Guardrails
- Repo-specific constraints that materially affect implementation work

## Validation Checklist
- Paths still exist
- Commands still match current config
- Linked docs still exist
- `AGENTS.md` stays concise
```

Compression rules:

- Prefer bullets over paragraphs
- Prefer stable paths over prose
- Keep the file near 100 lines
- Link outward instead of copying detailed policy
