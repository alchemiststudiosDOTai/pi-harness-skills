---
name: differential-session-runner
description: Run or continue a differential debugging session between two implementations, traces, captures, or outputs. Record artifact identity, exact commands, first mismatch progression, findings, validation, and next probe in a durable session log.
writes-to: memory-bank/evidence/
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
hard-guards:
  - Record exact commands, artifact paths, and hashes whenever available
  - Prefer continuing an existing session for the same artifact identity instead of creating duplicates
  - Do not claim a mismatch is fixed without validation evidence
  - Keep prior findings intact; append or mark superseded findings explicitly
---

# Differential Session Runner

Use this skill when debugging requires a **durable evidence trail** rather than ad hoc notes.

This skill is for workflows where you are comparing:

- original vs rewrite
- implementation A vs implementation B
- baseline trace vs candidate trace
- before vs after replay output
- captured artifact vs regenerated artifact

The goal is not only to investigate. The goal is to leave behind a **session artifact** another operator or agent can continue.

## When to Use

Use this skill when the user asks to:

- continue a differential debugging session
- compare two implementations and record mismatches
- create or update a debugging session log
- track replay / trace / capture divergence over time
- document what changed between mismatched and cleared runs

## Core Principle

**Every differential investigation should produce a reusable evidence packet.**

A good session artifact lets another operator answer:

- what exact artifact was investigated?
- how was it identified?
- what commands were run?
- where did the first mismatch appear?
- what was learned?
- what changed?
- what validation proves the current state?
- what should happen next?

## Preferred Storage

If the repo already has a native evidence location, use it.

Examples:
- `docs/.../sessions/`
- `docs/chunks/`
- `analysis/.../reports/`
- existing session indexes

If the repo does **not** already have a native convention, write to:

- `memory-bank/evidence/YYYY-MM-DD_HH-MM-SS_<topic>-session.md`
- optional index: `memory-bank/evidence/index.md`

## Workflow

### 1. Load the repo's evidence convention first

Before creating anything, search for:

- playbooks / runbooks
- session indexes
- prior session files
- report directories
- chunk/evidence templates

Read the relevant guidance and continue the repo's existing pattern.

### 2. Identify the artifact under investigation

Capture the strongest available identity for the artifact:

- artifact path
- SHA256 / content hash
- commit SHA
- case name / run id / replay id
- timestamp if needed

If a content hash is possible, record it early and use it as the main session identity.

### 3. Decide whether to continue or create

Search existing sessions for the artifact identity.

- If a session already exists for the same artifact/hash, append to that session.
- If the artifact identity is new, create a new session and update the session index if the repo has one.

### 4. Record baseline comparison commands

Capture the exact commands used for the first comparison step.

Examples:

```bash
python compare.py --baseline out/a.json --candidate out/b.json
pytest tests/test_replay.py -k case_17
mytool diff trace_a.cdt trace_b.cdt
```

Never summarize commands loosely. Record them exactly.

### 5. Record first mismatch progression

Capture the first relevant divergence and, if applicable, how it moved over time.

Examples:
- first bad tick
- first mismatched field
- first unexpected output line
- first extra/missing RNG draw
- first snapshot diff

If later fixes move the mismatch frontier, append the new progression rather than deleting the old one.

### 6. Record key findings

Write findings as evidence-backed observations, not guesses.

Good findings:
- identify the mismatched subsystem or callsite
- name the field or branch that diverged
- note whether the issue self-heals or persists
- connect the mismatch to a concrete code path or state transition

### 7. Record landed changes separately

If code changes are made during the investigation, capture them in a separate section:

- files changed
- short description of each change
- tests added or updated

If no changes were made, state that explicitly.

### 8. Record validation

List the validation commands and their results.

Examples:
- replay passes end-to-end
- diff result is now clean
- targeted tests pass
- health check passes

Do not write "fixed" without a validation section.

### 9. Set the next probe

Every session should end with one of:

- cleared / no next probe required
- one explicit next investigation target
- one blocked dependency or missing tool/input

## Recommended Session Template

```markdown
---
title: "<topic> – Differential Session"
phase: Evidence
date: "YYYY-MM-DD HH:MM:SS"
owner: "<agent_or_user>"
tags: [evidence, differential, <topic>]
---

## Artifact
- Path: `<path>`
- Identity: `<sha256|commit|case-id>`

## Baseline Commands
- `<exact command 1>`
- `<exact command 2>`

## First Mismatch Progression
- baseline: `<first mismatch>`
- after fix 1: `<new frontier>`
- after fix 2: `<cleared|new mismatch>`

## Key Findings
- finding 1
- finding 2

## Landed Changes
- `path/to/file` → change summary
- `tests/...` → validation coverage added

## Validation
- `<command>` → `<result>`
- `<command>` → `<result>`

## Outcome / Next Probe
- `<cleared | next probe | blocked reason>`
```

## Good Session Behavior

- preserve earlier mismatch states instead of overwriting them
- use hashes or artifact IDs to avoid ambiguous session naming
- record exact commands so another operator can replay the same evidence path
- separate findings from fixes
- separate fixes from validation

## Bad Session Behavior

- "Investigated replay issue and fixed some stuff"
- omitting the artifact identity
- omitting commands
- replacing prior mismatch history with the latest state only
- claiming success without validation evidence

## Output Requirements

A completed session artifact should make handoff possible with no hidden context.

It must include:

- artifact identity
- exact commands
- first mismatch progression
- key findings
- landed changes or explicit no-change note
- validation evidence
- next probe or clear outcome

## Handoff

After updating the session artifact:

- if the investigation uncovered code work, hand off to `plan-phase`
- if code work is already scoped in a plan, hand off to `execute-phase`
- if the investigation is complete, send the user the session path and a one-line status
