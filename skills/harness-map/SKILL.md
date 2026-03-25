---
name: harness-map
description: "Map a repository's mechanical harness layers: canonical check command, local and CI gates, architecture boundaries, structural rules, behavioral verification, docs ratchets, evidence workflows, and operator-facing surfaces. Use when you need to understand how a repo keeps change safe."
writes-to: HARNESS.md
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash(find:*)
  - Bash(rg:*)
  - Bash(grep:*)
  - Bash(git:*)
hard-guards:
  - Facts first - identify what exists before making recommendations
  - Include exact file paths and line anchors when applicable
  - Do not modify source code while mapping the harness unless explicitly asked
  - Distinguish local gates, CI gates, policy layers, evidence layers, and operator surfaces
---

# Harness Map

Map the repository's **actual harness**: the mechanical checks, policies, workflows, and artifacts that make change safe.

This skill is narrower than generic codebase research. It is specifically for answering questions like:

- "What is the harness in this repo?"
- "What does `check` actually run?"
- "Which layers are local vs CI vs docs vs evidence?"
- "How is architecture enforced here?"
- "What operator surfaces teach agents how to use the harness?"

## Core Principle

**Map the harness as implemented, not as imagined.**

Prefer:
- commands that actually run
- config files that actually enforce policy
- CI workflows that actually gate merges
- docs and playbooks that actually structure investigations
- agent/operator files that actually expose the workflow

Avoid:
- aspirational architecture prose without enforcement
- recommendations before the map exists
- broad codebase summaries that skip the gate structure

## What Counts as Harness

A repo harness usually includes some or all of these layers:

1. **Canonical local command**
   - `just check`, `make check`, `task check`, `npm test`, etc.
2. **Architecture boundaries**
   - Import Linter, dependency-cruiser, Bazel visibility, custom dependency tests
3. **Structural rules**
   - ast-grep, semgrep, custom lint rules, codemod rule tests
4. **Behavioral verification**
   - unit/integration tests, snapshots, goldens, deterministic checks, build verification
5. **Docs ratchets**
   - docs link checks, nav checks, metadata/frontmatter checks, allowlists
6. **CI decomposition**
   - matrix jobs or separate workflows that mirror harness gates
7. **Evidence workflows**
   - session logs, diff reports, chunk docs, experiment records, replay/debug artifacts
8. **Operator surface**
   - `AGENTS.md`, `.codex/`, environment files, repo-local skills, slash commands

## When to Use

Use this skill when the user asks to:

- map or explain the harness
- identify all gate layers in a repo
- compare local checks with CI checks
- document how architectural constraints are enforced
- understand how agents/operators are expected to use the repo safely

## Workflow

### 1. Find the canonical local entrypoint

Inspect common entrypoint files first:

- `justfile`
- `Makefile`
- `package.json`
- `pyproject.toml`
- task runner config files

Capture:
- the canonical command name
- every subcommand it runs
- whether it chains all gates or only a subset

### 2. Find CI gate execution

Inspect CI workflows:

- `.github/workflows/*.yml`
- other CI configs (`.gitlab-ci.yml`, `buildkite`, etc.)

Capture:
- job names
- matrix dimensions
- whether `fail-fast` is enabled
- which local gates are mirrored in CI
- which gates only exist in CI

### 3. Find architecture enforcement

Look for:

- Import Linter / grimp
- dependency-cruiser
- layering tests
- package-boundary configs
- forbidden import tests

Capture:
- contract names
- source and forbidden modules
- ignore lists / allowed exceptions
- exact config path

### 4. Find structural rule enforcement

Look for:

- `sgconfig.yml`, ast-grep rule directories
- semgrep configs
- custom lint rule packages
- rule tests and snapshots

Capture:
- rule config files
- rule directories
- test directories
- snapshot/baseline locations
- any custom parser or language extensions

### 5. Find behavioral verification layers

Look for:

- test commands
- snapshot directories
- golden outputs
- deterministic helpers
- numerical equivalence docs
- build verification steps

Capture:
- exact commands
- test conventions docs
- locations of snapshots/goldens
- special validation steps outside the main test runner

### 6. Find docs ratchets

Look for:

- docs check scripts
- nav validation
- broken-link validation
- frontmatter/tag checks
- allowlists / baselines

Capture:
- categories of docs failures
- allowlist file paths
- whether the check behaves as a ratchet

### 7. Find evidence workflows

Look for:

- chunk docs
- debugging session logs
- replay/trace diff playbooks
- benchmark result docs
- evidence indexes

Capture:
- index files
- per-session or per-chunk docs
- required evidence fields
- exact commands recorded in those artifacts

### 8. Find operator-facing surfaces

Look for:

- `AGENTS.md`
- `.codex/environments/*`
- `.codex/skills/*`
- command docs
- plugin manifests

Capture:
- setup / run / test actions
- repo-local skills that wrap harness flows
- operator instructions that point to real commands

### 9. Synthesize the harness map

Write the harness map directly to the repository root as:

`HARNESS.md`

This file serves as the single source of truth for how this repository keeps change safe. Write it in a style that a new developer or agent can use to understand the harness immediately.

Recommended structure:

```markdown
---
title: "<repo> – Harness Map"
phase: Research
date: "YYYY-MM-DD HH:MM:SS"
owner: "<agent_or_user>"
tags: [research, harness, <repo>]
---

# <repo> – Harness Map

A living map of the mechanical checks, policies, workflows, and artifacts that make change safe in this repository.

## Canonical Entry Point
- `path:line-line` → command and subcommands

## Harness Layers

### Layer 1: Local Checks
| Check | Command | Config | Enforces |
|-------|---------|--------|----------|
| ... | ... | ... | ... |

### Layer 2: Architecture Boundaries
| Contract | Source | Forbidden | Config |
|----------|--------|-----------|--------|
| ... | ... | ... | ... |

### Layer 3: Structural Rules
| Rule Set | Config | Test Location | Notes |
|----------|--------|---------------|-------|
| ... | ... | ... | ... |

### Layer 4: Behavioral Verification
| Test Suite | Command | Snapshot/Golden Location | Notes |
|------------|---------|--------------------------|-------|
| ... | ... | ... | ... |

### Layer 5: Docs Ratchet
| Check | Command | Allowlist | Notes |
|-------|---------|-----------|-------|
| ... | ... | ... | ... |

### Layer 6: CI Matrix
| Job | Triggers | Gate | Config |
|-----|----------|------|--------|
| ... | ... | ... | ... |

### Layer 7: Evidence Workflow
| Artifact | Location | Triggers | Format |
|----------|----------|----------|--------|
| ... | ... | ... | ... |

### Layer 8: Operator Surface
| Surface | Location | Purpose | Usage |
|---------|----------|---------|-------|
| ... | ... | ... | ... |

## Command Chain
Ordered list of checks as executed by the canonical entry point:
1. ...
2. ...
3. ...

## Quick Reference
- **Run all local checks:** `...`
- **Run CI locally:** `...`
- **Add a new check:** ...

## Source Index
| File | What It Contributes |
|------|-------------------|
| `path:line-line` | ... |
```

## Output Requirements

Write the harness map to `HARNESS.md` in the repository root. This file must:

- identify the **single best local entrypoint** if one exists
- show where each layer is enforced
- distinguish between **enforced config** and **descriptive docs**
- include exact file paths
- include line numbers when they materially improve traceability
- describe what exists before suggesting changes
- use tables for scannable layer summaries
- include a quick reference section for operators

## Good Output Example

```markdown
# myrepo – Harness Map

## Canonical Entry Point
- `justfile:22-29` defines `check *args:` and runs Ruff, Import Linter, ty, docs checks, ast-grep, pytest, and Zig checks.

## Harness Layers

### Layer 2: Architecture Boundaries
| Contract | Source | Forbidden | Config |
|----------|--------|-----------|--------|
| core-api | src/core | src/plugins | pyproject.toml:80-110 |

### Layer 6: CI Matrix
| Job | Triggers | Gate | Config |
|-----|----------|------|--------|
| test | push | all checks | .github/workflows/ci.yml:13-79 |
```

## Bad Output Example

```markdown
The repo appears to care about quality and uses several tools.
It has some tests and some linting.
```

## Handoff

After generating `HARNESS.md`:

- commit it to the repo so it stays current
- use `plan-phase` if the user wants to add or improve a harness layer
- compare two repos' `HARNESS.md` files to understand their differences
