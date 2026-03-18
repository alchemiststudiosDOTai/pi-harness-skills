---
name: smart-git
description: Stage all local changes, generate a commit message with branch context, diff stats, and a truncated inline diff versus origin/<branch>, then commit and push with automatic rebase-and-retry when remote is ahead.
---

# Smart Git

Use this skill when you want to quickly commit and push current repository changes with a high-signal commit message.

## Defaults

- Assume current local working changes are intended to be committed and pushed.
- Include inline diff in commit body by default.
- Default maximum inline diff lines: `200`.
- If no upstream exists, create one on first push.

## Workflow

### 1) Context Snapshot

Collect and report:
- Current branch
- Upstream branch (if configured)
- Ahead/behind status
- Whether there are local changes to commit

### 2) Fetch and Pre-Commit Diff

1. Determine current branch.
2. Fetch `origin/<branch>` if it exists.
3. Compute diff stats against `origin/<branch>`.
4. Build a truncated unified diff (max 200 lines unless user overrides).

### 3) Stage and Commit

1. If there are no changes, exit cleanly and report "nothing to commit".
2. Stage all changes.
3. Generate commit message with:
   - Title: short branch-aware summary
   - `Changes Summary:` section (diff stats)
   - `Detailed Diffs` section (truncated unified diff)
4. Commit staged changes.

### 4) Push Strategy

1. If upstream is missing, run first push with upstream set.
2. Otherwise push normally.
3. If push fails because remote moved ahead:
   - Pull/rebase onto remote branch
   - Retry push once
4. If retry still fails, report conflict state and stop.

## Commit Message Template

```text
<short summary>

Branch: <branch>

Changes Summary:
<diff --stat output>

Detailed Diffs (truncated to <N> lines):
<unified diff snippet>
```

## Validation

After push, verify:
- Last commit message contains `Changes Summary:`
- Last commit message contains `Detailed Diffs`
- Local branch is synced (or conflict state is clearly reported)
- No staged leftovers remain unexpectedly

## Failure Handling

- No remote branch: continue with local commit and report push not possible
- Rebase conflicts: stop, report exact next manual commands
- Empty diff/stat output: still commit with clear note that remote baseline was unavailable

## Output Expectations

Always return a concise final summary containing:
- Branch pushed
- Commit SHA
- Upstream target
- Ahead/behind result
- Any manual follow-up required
