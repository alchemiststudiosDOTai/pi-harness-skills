---
name: agents-md-mapper
description: This skill should be used when creating, refreshing, or validating a repository `AGENTS.md` so it stays concise, current, and grounded in repository evidence. Use when `AGENTS.md` is missing or stale, after refactors or tooling changes, when new docs become the system of record, or when adding lightweight drift checks.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(git:*)
  - Bash(ls:*)
hard-guards:
  - Treat `AGENTS.md` as a map, not a dump
  - Update only from repository evidence: files, docs, CI, commands, and git history
  - Prefer stable paths and exact commands over prose-heavy explanation
  - Keep `AGENTS.md` roughly under 100 lines unless repo complexity clearly requires more
  - Omit weak or speculative claims
  - Never include secrets, tokens, credentials, or environment values
---

# AGENTS.md Mapper

## Overview

Maintain a concise, current `AGENTS.md` for a repository as the codebase changes. Treat the file as a navigational map for future coding agents: show where to start, where important things live, how to validate changes, and which deeper docs outrank the map.

## When to Use

- Create a new `AGENTS.md` for a repository that does not have one
- Refresh an existing `AGENTS.md` that may be stale after refactors, path moves, package splits, or architecture changes
- Update the map after tooling, tests, CI, docs, or ownership signals changed
- Point `AGENTS.md` at new architecture docs, runbooks, or generated references that became the source of truth
- Add lightweight checks that detect drift between `AGENTS.md` and repository reality

## Core Contract

### 1. Keep the map compact

- Prefer roughly 90 to 100 lines
- Prefer bullets over paragraphs
- Prefer concrete paths and commands over abstract advice
- Link to deeper docs instead of copying them

### 2. Treat repository evidence as the source of truth

- Read the repository tree before writing claims about structure
- Read actual config files before listing commands
- Read CI workflows before describing validation
- Read docs and architecture references before summarizing boundaries
- Read recent git history before carrying forward old paths or retired modules

### 3. Optimize for agent legibility

- Surface entry points, domain boundaries, and validation commands first
- Make the navigation order obvious
- Remove stale or duplicated sections aggressively
- Normalize heading order so future updates stay mechanical

### 4. Omit unsupported detail

- If evidence is weak, omit the claim
- If a detail is volatile, point to its source doc instead of embedding it
- If two docs disagree, prefer the one supported by current code and CI

## Inputs to Inspect

Inspect repository evidence, not guesswork:

- Current top-level tree and major subdirectories
- Key top-level files such as `README`, `pyproject.toml`, `package.json`, `Cargo.toml`, `Makefile`, `justfile`, or task runner configs
- Existing `AGENTS.md`, if present
- `ARCHITECTURE.md`, `docs/`, runbooks, plans, references, and generated indexes
- CI workflows and automation config
- Recent git history, especially merges, path renames, retired modules, and tooling changes
- Ownership signals such as `CODEOWNERS`, package manifests, and boundary-enforcement config

## Workflow

### Step 1: Discover repository shape

- Collect the top-level tree and major subdirectories
- Identify package roots, module roots, and major domain folders
- Locate docs indexes, architecture docs, and runbooks
- Capture build, test, lint, and run entrypoints from real config files

### Step 2: Read the current map and deeper docs

- Open `AGENTS.md` if it exists
- Open the main onboarding docs first: `README`, architecture docs, and docs indexes
- Open the exact files that define task runner commands and CI gates
- Note which docs already serve as the system of record

### Step 3: Inspect recent change signals

- Review recent git history for renamed paths, new packages, retired directories, and workflow changes
- Check whether new docs or generated references replaced older explanations
- Check whether CI or task runners added or removed validation steps

### Step 4: Compare map versus reality

- Verify that listed paths still exist
- Verify that listed commands still exist and still match task runner or CI usage
- Verify that architecture or package boundaries still match current layout
- Verify that linked docs still exist and remain the best source of truth

### Step 5: Rewrite for compression and clarity

- Keep only high-value navigational content
- Collapse repeated guidance into one canonical section
- Replace prose-heavy explanations with stable file paths and exact commands
- Remove outdated paths, retired tools, and stale historical detail

### Step 6: Validate before finalizing

- Re-check every path and command
- Remove duplicate or unsupported claims
- Confirm the file remains short, scan-friendly, and grounded in current evidence

## What to Put in `AGENTS.md`

Include these sections when repository evidence supports them:

- Project overview
- Where to start
- Repository map
- Build, test, lint, and run commands
- Architecture or package boundaries
- Key docs and sources of truth
- Change rules or contribution guardrails
- Validation checklist

Exclude these unless they directly change navigation or implementation behavior:

- Long architectural essays
- Full style guides already documented elsewhere
- Exhaustive dependency lists
- Historical detail that does not affect current navigation
- Issue triage policy that does not change implementation work

## Decision Rules

- If a section grows past a few bullets, move detail to `docs/` or another source doc and link to it
- If commands differ between docs and CI, prefer the version backed by current config
- If the repository already has a strong docs index, make `AGENTS.md` point to it rather than restating it
- If a repo has no evidence for ownership or architecture boundaries, do not invent them

## Output Modes

Produce one of these outputs:

- A fresh `AGENTS.md`
- A focused patch for the existing `AGENTS.md`

Use the compact outline in `references/agents-md-outline.md` as a starting point when the repository supports those sections.

## Validation Checklist

- Every listed path exists
- Every listed command is defined in current repo config or CI
- Every linked source-of-truth doc exists
- Stale headings and duplicate sections are removed
- The file stays compact and navigable
- No secrets or environment values appear in the file

## Recommended Follow-Up Checks

When automation is requested, add lightweight drift checks such as:

- Fail if a linked path in `AGENTS.md` no longer exists
- Fail if a listed command disappears from CI or task runner config
- Flag missing references to new top-level domains after major tree changes
- Flag stale sections after large refactors or package moves

## Success Criteria

Consider the skill successful when:

- `AGENTS.md` is short and easy to scan
- Every listed path and command matches the current repository
- The file points to deeper sources of truth instead of copying them
- Stale guidance is removed
- Another coding agent can use `AGENTS.md` as a reliable repository map
