---
name: docs-frontmatter-ontology
description: Enforce repository Markdown docs with required YAML frontmatter and ontology_relations, and set up a pre-push hook that blocks pushes when any .md file except AGENTS.md is missing required frontmatter keys.
---

# Docs Frontmatter + Ontology Guard

Use this skill when a repo needs consistent documentation shape and enforcement.

## What this skill enforces

For every Markdown file (`*.md`) except `AGENTS.md`, require top-of-file YAML frontmatter with these keys:

- `title`
- `when_to_read`
- `summary`
- `ontology_relations`

`ontology_relations` entries must use this structure:

- `relation`
- `target`
- `note`

## Canonical document scaffold

Use this scaffold for new docs:

```md
---
title: "<Document Title>"
when_to_read:
  - "When <trigger/scenario #1>."
  - "When <trigger/scenario #2>."
summary: "<2-4 sentence practical summary of what this page explains and why it matters>."
ontology_relations:
  - relation: "depends_on"
    target: "<doc-path-or-concept-id>"
    note: "<why this relation exists>"
  - relation: "feeds"
    target: "<doc-path-or-concept-id>"
    note: "<what this doc contributes>"
---

# Purpose

# Scope

# Main content

## Flow / behavior

## Contracts / invariants

## Failure modes

# Related docs
```

## Enforcement steps

### 1) Add validator script

Create `scripts/check_markdown_frontmatter.py` that:

1. Enumerates markdown files from `git ls-files '*.md'`
2. Skips `AGENTS.md`
3. Validates YAML frontmatter exists at the very top of each file
4. Fails if any required key is missing
5. Exits non-zero with a clear per-file error list

### 2) Add pre-push hook in `.pre-commit-config.yaml`

Add a local hook:

```yaml
- repo: local
  hooks:
    - id: markdown-frontmatter-required
      name: Require markdown frontmatter (except AGENTS.md)
      entry: python3 scripts/check_markdown_frontmatter.py
      language: system
      files: \.md$
      exclude: (^|/)AGENTS\.md$
      stages: [pre-push]
```

### 3) Install and verify

```bash
pre-commit install --hook-type pre-push
pre-commit run markdown-frontmatter-required --hook-stage pre-push --all-files
```

## Behavior rules

- Do not exempt README or docs unless explicitly requested.
- Keep relation IDs and targets stable and reusable.
- If a document is missing frontmatter, add it before any content edits.
- If repo already has a docs template, align it to this schema.

## Completion checklist

- [ ] Every tracked `.md` file except `AGENTS.md` has required frontmatter keys
- [ ] `.pre-commit-config.yaml` includes the pre-push hook
- [ ] `scripts/check_markdown_frontmatter.py` exists and fails correctly on bad files
- [ ] Hook is installed for pre-push
