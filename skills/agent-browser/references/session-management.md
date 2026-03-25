---
title: "agent-browser session management"
link: "agent-browser-session-management"
type: reference
ontological_relations:
  - relates_to: [[agent-browser]]
tags: [reference, agent-browser, sessions, state, persistence]
uuid: "auto-generated"
created_at: "2026-03-25T00:00:00Z"
---

# Session Management

Managing browser sessions, state persistence, and concurrent automations.

## Session Types

| Type | Use Case | Persistence |
|------|----------|-------------|
| Default | Single automation | Lost on close |
| Named `--session` | Isolated tasks | Manual save/load |
| `--session-name` | Recurring tasks | Auto-save on close |
| `--profile` | Persistent profile | Permanent |

## Named Sessions

Isolate multiple browser instances.

```bash
# Session 1: Shopping site
agent-browser --session shop open https://shop.example.com

# Session 2: Bank site
agent-browser --session bank open https://bank.example.com

# Interact with each independently
agent-browser --session shop snapshot -i
agent-browser --session bank snapshot -i

# List active sessions
agent-browser session list

# Close specific session
agent-browser --session shop close
```

## State Persistence

Save and restore browser state (cookies, localStorage, etc.).

### Manual Save/Load

```bash
# After login, save state
agent-browser open https://app.example.com/login
# ... login flow ...
agent-browser state save ./auth.json

# Later, restore state
agent-browser state load ./auth.json
agent-browser open https://app.example.com/dashboard  # Already logged in
```

### Auto-Save with session-name

```bash
# First session: login and close
agent-browser --session-name myapp open https://app.example.com/login
# ... login ...
agent-browser close  # State auto-saved to ~/.agent-browser/sessions/myapp/

# Second session: state auto-restored
agent-browser --session-name myapp open https://app.example.com/dashboard
```

### Profile Directory

Full browser profile with all data.

```bash
# First run: login
agent-browser --profile ~/.myapp open https://app.example.com/login
# ... login ...

# Future runs: profile persists
agent-browser --profile ~/.myapp open https://app.example.com/dashboard
```

## Auth Vault

Encrypted credential storage for automated login.

### Save Credentials

```bash
# Secure: pipe password via stdin (no shell history)
echo "$PASSWORD" | agent-browser auth save github \
  --url https://github.com/login \
  --username user@example.com \
  --password-stdin

# Or with explicit password (less secure)
agent-browser auth save myapp \
  --url https://app.example.com/login \
  --username user@example.com \
  --password mypassword
```

### Login with Saved Credentials

```bash
agent-browser auth login github
```

The `auth login` command:
1. Navigates to the saved URL
2. Waits for login form selectors
3. Fills credentials
4. Submits form
5. Waits for navigation away from login page

### Manage Auth Profiles

```bash
agent-browser auth list           # List all saved credentials
agent-browser auth show github    # Show details (no password)
agent-browser auth delete github  # Remove saved credentials
```

### Encryption

Set `AGENT_BROWSER_ENCRYPTION_KEY` for encryption at rest:

```bash
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
agent-browser auth save myapp --url https://example.com --username user --password-stdin
```

## State Files

### Manual State Management

```bash
agent-browser state save ./auth.json       # Save current state
agent-browser state load ./auth.json       # Load state
agent-browser state show ./auth.json       # View state metadata
agent-browser state list                   # List saved states
agent-browser state clear mysession        # Clear specific session
agent-browser state clean --older-than 7   # Clean states older than N days
```

### State File Format

State files are JSON containing:
- Cookies
- localStorage
- sessionStorage
- Origin permissions

**Security:** State files contain session tokens in plaintext. Add to `.gitignore` and delete when no longer needed.

## Import from Running Browser

Connect to your existing Chrome session (already logged in).

```bash
# Auto-discover and connect
agent-browser --auto-connect state save ./auth.json

# Or with explicit CDP port
agent-browser --cdp 9222 state save ./auth.json

# Use the imported state
agent-browser --state ./auth.json open https://app.example.com
```

Works with Chrome, Chromium, Edge, Brave, and other Chromium-based browsers.

## Concurrent Automation

Run multiple browsers for parallel tasks.

```bash
# Open different sites in parallel
agent-browser --session task1 open https://site-a.com
agent-browser --session task2 open https://site-b.com
agent-browser --session task3 open https://site-c.com

# Screenshot each
agent-browser --session task1 screenshot ./site-a.png
agent-browser --session task2 screenshot ./site-b.png
agent-browser --session task3 screenshot ./site-c.png

# Cleanup
agent-browser --session task1 close
agent-browser --session task2 close
agent-browser --session task3 close
```

## Cleanup

### Explicit Close

```bash
agent-browser close                    # Default session
agent-browser --session myapp close    # Named session
```

### Auto-Close on Idle

For ephemeral/CI environments:

```bash
AGENT_BROWSER_IDLE_TIMEOUT_MS=60000 agent-browser open example.com
# Browser closes after 60s of inactivity
```

### Cleanup Old States

```bash
# Remove states older than 7 days
agent-browser state clean --older-than 7

# Clear specific session
agent-browser state clear myapp

# Clear all states
rm -rf ~/.agent-browser/sessions/
```

## Best Practices

1. **Always close sessions** when done to avoid leaked processes
2. **Use named sessions** for concurrent automations
3. **Save state** after login to avoid re-authenticating
4. **Encrypt state files** containing sensitive credentials
5. **Add state files to .gitignore** to prevent accidental commits
6. **Use auth vault** for recurring login tasks
7. **Clean old states** periodically to free disk space
