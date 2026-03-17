# @alchemiststudios/pi-harness-skills

Harness Engineering skill pack for [pi](https://www.npmjs.com/package/@mariozechner/pi-coding-agent): structured **Research → Plan → Execute → QA** workflows, plus mapping and ast-grep setup skills.

[![npm version](https://img.shields.io/npm/v/%40alchemiststudios%2Fpi-harness-skills?style=for-the-badge)](https://www.npmjs.com/package/@alchemiststudios/pi-harness-skills)
[![license](https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge)](./LICENSE)
[![pi package](https://img.shields.io/badge/pi-package-blue?style=for-the-badge)](https://shittycodingagent.ai/packages)

## Why this package

- **Operational workflow skills**: run consistent research/planning/execution/qa loops.
- **Reproducible artifacts**: phases write to `.artifacts/research`, `.artifacts/plan`, `.artifacts/execute`.
- **Practical tooling included**: structural scanning, symbol indexing, dependency tracing, ast-grep setup.

## Install

### npm

```bash
pi install npm:@alchemiststudios/pi-harness-skills
```

### Git

```bash
pi install git:github.com/alchemiststudiosDOTai/pi-harness-skills@v0.1.1
```

### Local path

```bash
pi install /absolute/path/to/pi-harness-package
```

## Included skills

| Skill | Purpose |
|---|---|
| `research-phase` | Factual codebase mapping + structural analysis outputs |
| `plan-phase` | Convert research into execution-ready implementation plans |
| `execute-phase` | Execute plans with gates, atomic commits, and a single execution log |
| `qa-from-execute` | QA changed areas only, without modifying source code |
| `harness-map` | Map a repo’s harness layers and operator surfaces |
| `ast-grep-setup` | Bootstrap ast-grep rules and rule tests |
| `agents-md-mapper` | Build/refresh evidence-grounded `AGENTS.md` |
| `differential-session-runner` | Durable differential debugging session workflow |

## Quick usage

```text
/skill:research-phase
/skill:plan-phase
/skill:execute-phase .artifacts/plan/<plan-file>.md
/skill:qa-from-execute .artifacts/execute/<execute-log>.md
```

Or let pi auto-load the matching skill from the prompt.

## Requirements

- pi coding agent
- Bash environment for included helper scripts (used by `research-phase`)

## License

MIT
