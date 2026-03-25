---
title: "agent-browser commands reference"
link: "agent-browser-commands"
type: reference
ontological_relations:
  - relates_to: [[agent-browser]]
tags: [reference, agent-browser, browser, automation]
uuid: "auto-generated"
created_at: "2026-03-25T00:00:00Z"
---

# Command Reference

Complete reference for all agent-browser CLI commands.

## Navigation

### `open`
Navigate to a URL.
```bash
agent-browser open <url>
agent-browser goto <url>
agent-browser navigate <url>
```

Options:
- `--new-window` - Open in new window
- `--background` - Open in background tab

### `close`
Close the browser.
```bash
agent-browser close
```

### `back` / `forward`
Navigate browser history.
```bash
agent-browser back
agent-browser forward
```

---

## Snapshot

### `snapshot`
Get accessibility tree of current page.

```bash
agent-browser snapshot
agent-browser snapshot -i              # Interactive elements only
agent-browser snapshot -s "#selector" # Scope to selector
agent-browser snapshot --json         # JSON output
agent-browser snapshot --json > out.json
agent-browser snapshot -c             # Compact output
```

---

## Interaction

### `click`
Click an element by ref.
```bash
agent-browser click @e1
agent-browser click @e1 --new-tab    # Click and open in new tab
agent-browser click @e1 --force       # Force click (bypass visibility)
```

### `fill`
Clear and fill an input field.
```bash
agent-browser fill @e1 "text to fill"
```

### `type`
Type text without clearing (appends).
```bash
agent-browser type @e1 "additional text"
```

### `select`
Select a dropdown option.
```bash
agent-browser select @e1 "Option Text"
agent-browser select @e1 "value" --by value  # Select by option value
```

### `check` / `uncheck`
Toggle checkboxes.
```bash
agent-browser check @e1
agent-browser uncheck @e1
```

### `press`
Press a keyboard key.
```bash
agent-browser press Enter
agent-browser press Escape
agent-browser press Tab
agent-browser press "Control+a"
```

### `keyboard`
Type at current focus without selector.
```bash
agent-browser keyboard type "hello"
agent-browser keyboard inserttext "hello"  # Without key events
agent-browser keyboard press Enter
```

### `scroll`
Scroll the page or element.
```bash
agent-browser scroll down 500
agent-browser scroll up 300
agent-browser scroll down 500 --selector "div.content"  # Within element
```

---

## Get Information

### `get`
Get page or element information.
```bash
agent-browser get url              # Current URL
agent-browser get title             # Page title
agent-browser get text @e1         # Element text
agent-browser get text body        # All body text
agent-browser get text @e1 > out.txt
agent-browser get cdp-url          # CDP WebSocket URL
agent-browser get text @e1 --json  # JSON output
```

---

## Wait

### `wait`
Wait for conditions.
```bash
agent-browser wait @e1              # Wait for element
agent-browser wait --load networkidle  # Network idle
agent-browser wait --load domcontentloaded
agent-browser wait --url "**/page"  # URL pattern
agent-browser wait 2000             # Milliseconds
agent-browser wait --text "Welcome" # Text appears
agent-browser wait --fn "condition" # JavaScript condition
agent-browser wait @e1 --state hidden  # Element hidden
```

---

## Capture

### `screenshot`
Take a screenshot.
```bash
agent-browser screenshot                    # To temp dir
agent-browser screenshot output.png          # To file
agent-browser screenshot --full              # Full page
agent-browser screenshot --annotate          # With element labels
agent-browser screenshot --screenshot-dir ./shots
agent-browser screenshot --screenshot-format jpeg
agent-browser screenshot --screenshot-quality 80
agent-browser screenshot --json              # JSON with path
```

### `pdf`
Save page as PDF.
```bash
agent-browser pdf output.pdf
agent-browser pdf output.pdf --format A4
```

### `record`
Record session as video.
```bash
agent-browser record start demo.webm
agent-browser record stop
```

---

## Network

### `network`
Network inspection and manipulation.
```bash
agent-browser network requests                    # List requests
agent-browser network requests --type xhr,fetch    # Filter by type
agent-browser network requests --method POST       # Filter by method
agent-browser network requests --status 2xx       # Filter by status
agent-browser network request <requestId>          # Request details
agent-browser network route "**/api/*" --abort     # Block requests
agent-browser network har start                    # Start recording
agent-browser network har stop ./capture.har       # Stop and save
```

---

## State

### `state`
Manage browser state.
```bash
agent-browser state save ./auth.json
agent-browser state load ./auth.json
agent-browser state list
agent-browser state show ./auth.json
agent-browser state clear mysession
agent-browser state clean --older-than 7
```

### Auth Vault
```bash
agent-browser auth save <name> --url <url> --username <user> --password-stdin
agent-browser auth login <name>
agent-browser auth list
agent-browser auth show <name>
agent-browser auth delete <name>
```

---

## Device & Viewport

### `set`
Configure browser settings.
```bash
agent-browser set viewport 1920 1080
agent-browser set viewport 1920 1080 2        # With scale (retina)
agent-browser set device "iPhone 14"
agent-browser set device "iPad Pro"
agent-browser set media dark
agent-browser set media light
```

### `device`
iOS device management.
```bash
agent-browser device list
agent-browser -p ios --device "iPhone 16 Pro" open <url>
```

---

## Clipboard

### `clipboard`
Clipboard operations.
```bash
agent-browser clipboard read
agent-browser clipboard write "text"
agent-browser clipboard copy
agent-browser clipboard paste
```

---

## Dialogs

### `dialog`
Handle JavaScript dialogs.
```bash
agent-browser dialog accept
agent-browser dialog accept "input text"
agent-browser dialog dismiss
agent-browser dialog status
```

---

## Tabs

### `tab`
Manage browser tabs.
```bash
agent-browser tab              # List tabs
agent-browser tab 2            # Switch to tab 2
agent-browser tab --url "*settings*"  # Switch by URL
agent-browser tab new          # Open new tab
agent-browser tab close       # Close current tab
```

---

## Sessions

### `--session`
Named sessions for isolation.
```bash
agent-browser --session myapp open <url>
agent-browser --session myapp snapshot -i
agent-browser --session-name myapp state save ./auth.json
agent-browser session list
```

---

## Diff

### `diff`
Compare page states.
```bash
agent-browser diff snapshot                    # Compare to last snapshot
agent-browser diff snapshot --baseline before.txt
agent-browser diff screenshot --baseline before.png
agent-browser diff url <url1> <url2>
agent-browser diff url <url1> <url2> --screenshot
agent-browser diff url <url1> <url2> --wait-until networkidle
agent-browser diff url <url1> <url2> --selector "#main"
```

---

## Developer Tools

### `inspect`
Open Chrome DevTools.
```bash
agent-browser inspect
```

### `profiler`
Chrome DevTools profiling.
```bash
agent-browser profiler start
agent-browser profiler stop trace.json
```

### `console`
Console output.
```bash
agent-browser console
agent-browser errors
```

### `highlight`
Highlight element in browser.
```bash
agent-browser highlight @e1
```

---

## Batch

### `batch`
Execute multiple commands.
```bash
echo '[["open", "https://example.com"], ["snapshot", "-i"]]' | agent-browser batch --json
agent-browser batch --bail commands.json  # Stop on first error
```

---

## Configuration

### Global Options
```bash
agent-browser --config ./config.json      # Config file
agent-browser --profile ./data             # Browser profile dir
agent-browser --state ./auth.json          # State file
agent-browser --session myapp              # Named session
agent-browser --session-name myapp         # Session name
agent-browser --cdp 9222                   # CDP port
agent-browser --auto-connect               # Auto-connect to Chrome
agent-browser --headed                     # Visible browser
agent-browser --color-scheme dark          # Color scheme
agent-browser --download-path ./downloads  # Download directory
agent-browser --allow-file-access          # Allow file:// URLs
agent-browser --engine chrome              # Browser engine
agent-browser --executable-path /path      # Custom browser path
agent-browser --content-boundaries         # Enable content markers
agent-browser --proxy http://localhost:8080  # Proxy server
```

### Environment Variables
```bash
AGENT_BROWSER_CONTENT_BOUNDARIES=1
AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"
AGENT_BROWSER_ACTION_POLICY=./policy.json
AGENT_BROWSER_MAX_OUTPUT=50000
AGENT_BROWSER_DEFAULT_TIMEOUT=25000
AGENT_BROWSER_IDLE_TIMEOUT_MS=60000
AGENT_BROWSER_HEADED=1
AGENT_BROWSER_COLOR_SCHEME=dark
AGENT_BROWSER_ENGINE=lightpanda
AGENT_BROWSER_CONFIG=./config.json
```
