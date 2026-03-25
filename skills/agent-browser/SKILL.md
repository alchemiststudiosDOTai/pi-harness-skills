---
name: agent-browser
description: Browser automation for AI agents (Linux/macOS/Windows). Use when the user needs to interact with websites, navigate pages, fill forms, click buttons, take screenshots, extract data, test web apps, or automate browser tasks. Triggers include "open a website", "fill out a form", "click a button", "take a screenshot", "scrape data", "test this web app", "login to a site", or any task requiring programmatic web interaction.
allowed-tools:
  - Bash
writes-to: .artifacts/browser/
hard-guards:
  - Always re-snapshot after navigation or DOM changes
  - Close browser session when done
  - Use content boundaries for untrusted pages
---

# Browser Automation with agent-browser

The agent-browser CLI automates Chrome/Chromium via CDP (Chrome DevTools Protocol). Install via `npm i -g agent-browser`, `brew install agent-browser`, or `cargo install agent-browser`.

## Installation

### Linux (most common)

```bash
# Option 1: npm (recommended)
npm install -g agent-browser

# Option 2: cargo (if you have Rust)
cargo install agent-browser

# Then install Chromium
agent-browser install
```

### macOS

```bash
# npm
npm install -g agent-browser

# or Homebrew
brew install agent-browser

# Install Chromium
agent-browser install
```

### Windows (WSL2 or native)

```bash
# npm (WSL2 recommended for best experience)
npm install -g agent-browser
agent-browser install
```

### Verify Installation

```bash
agent-browser --version
agent-browser install  # Downloads Chromium if not present
```

### Dependencies (Linux)

If Chromium fails to launch, you may need system libraries:

```bash
# Debian/Ubuntu
sudo apt install libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 libasound2

# Fedora/RHEL
sudo dnf install nss nspr cups-libs libXcomposite libXdamage libXrandr libXScrnSaver alsa-lib
```

## Quick Start

```bash
# Navigate to a URL
agent-browser open https://example.com

# Get interactive elements
agent-browser snapshot -i

# Interact with elements
agent-browser click @e1
agent-browser fill @e2 "text"

# Take screenshot
agent-browser screenshot output.png

# Close when done
agent-browser close
```

## Core Workflow

Every browser automation follows this pattern:

1. **Navigate**: `agent-browser open <url>`
2. **Snapshot**: `agent-browser snapshot -i` (get element refs like `@e1`, `@e2`)
3. **Interact**: Use refs to click, fill, select
4. **Re-snapshot**: After navigation or DOM changes, get fresh refs

```bash
agent-browser open https://example.com/form
agent-browser snapshot -i
# Output: @e1 [input type="email"], @e2 [input type="password"], @e3 [button] "Submit"

agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password123"
agent-browser click @e3
agent-browser wait --load networkidle
agent-browser snapshot -i  # Check result
```

## Command Chaining

Chain commands with `&&` for efficiency when you don't need intermediate output:

```bash
# Chain navigation + wait + screenshot in one call
agent-browser open https://example.com && agent-browser wait --load networkidle && agent-browser screenshot page.png

# Chain multiple interactions
agent-browser fill @e1 "text" && agent-browser click @e2
```

## Essential Commands

### Navigation
```bash
agent-browser open <url>              # Navigate (aliases: goto, navigate)
agent-browser close                   # Close browser
agent-browser back                    # Go back
agent-browser forward                 # Go forward
```

### Snapshot
```bash
agent-browser snapshot -i             # Interactive elements with refs (recommended)
agent-browser snapshot -s "#selector"  # Scope to CSS selector
agent-browser snapshot --json          # JSON output for parsing
agent-browser snapshot --json > out.json
```

### Interaction
```bash
agent-browser click @e1               # Click element
agent-browser click @e1 --new-tab     # Click and open in new tab
agent-browser fill @e2 "text"         # Clear and type text
agent-browser type @e2 "text"         # Type without clearing
agent-browser select @e3 "option"     # Select dropdown option
agent-browser check @e4               # Check checkbox
agent-browser press Enter             # Press key
agent-browser keyboard type "text"    # Type at current focus
agent-browser scroll down 500         # Scroll page
```

### Get Information
```bash
agent-browser get text @e1           # Get element text
agent-browser get url                 # Get current URL
agent-browser get title               # Get page title
agent-browser get text body > page.txt  # Get all page text
```

### Wait
```bash
agent-browser wait @e1                # Wait for element
agent-browser wait --load networkidle # Wait for network idle
agent-browser wait --url "**/page"    # Wait for URL pattern
agent-browser wait 2000               # Wait milliseconds
agent-browser wait --text "Welcome"   # Wait for text to appear
```

### Capture
```bash
agent-browser screenshot              # Screenshot to temp dir
agent-browser screenshot page.png     # Screenshot to file
agent-browser screenshot --full       # Full page screenshot
agent-browser screenshot --annotate   # Annotated with element labels
agent-browser pdf output.pdf          # Save as PDF
```

### Network
```bash
agent-browser network requests                 # Inspect tracked requests
agent-browser network requests --type xhr,fetch  # Filter by type
agent-browser network route "**/api/*" --abort  # Block matching requests
agent-browser network har start                # Start HAR recording
agent-browser network har stop ./capture.har   # Stop and save
```

### Device & Viewport
```bash
agent-browser set viewport 1920 1080    # Set viewport size
agent-browser set viewport 1920 1080 2 # With 2x retina scale
agent-browser set device "iPhone 14"    # Emulate device
agent-browser set media dark            # Dark mode
```

### State Persistence
```bash
agent-browser state save ./auth.json    # Save session state
agent-browser state load ./auth.json    # Load session state
agent-browser --session myapp open ...  # Named session (auto-save)
```

## Authentication Patterns

### Option 1: Import from Running Browser
```bash
agent-browser --auto-connect state save ./auth.json
agent-browser --state ./auth.json open https://app.example.com
```

### Option 2: Auth Vault (Recommended)
```bash
# Save credentials (encrypted)
echo "$PASSWORD" | agent-browser auth save myapp --url https://app.example.com --username user --password-stdin

# Login later
agent-browser auth login myapp
agent-browser auth list
```

### Option 3: Session Persistence
```bash
agent-browser --session-name myapp open https://app.example.com/login
# ... login flow ...
agent-browser close  # State auto-saved

# Next time: auto-restored
agent-browser --session-name myapp open https://app.example.com/dashboard
```

## Common Patterns

### Form Submission
```bash
agent-browser open https://example.com/signup
agent-browser snapshot -i
agent-browser fill @e1 "Jane Doe"
agent-browser fill @e2 "jane@example.com"
agent-browser select @e3 "California"
agent-browser check @e4
agent-browser click @e5
agent-browser wait --load networkidle
```

### Data Extraction
```bash
agent-browser open https://example.com/products
agent-browser snapshot -i
agent-browser get text @e5           # Get specific element
agent-browser get text body > page.txt  # Get all text
agent-browser snapshot --json > data.json  # Structured data
```

### Visual Verification (Diff)
```bash
agent-browser snapshot -i          # Take baseline
agent-browser click @e2             # Perform action
agent-browser diff snapshot         # Compare current vs last

# Compare two pages
agent-browser diff url https://staging.example.com https://prod.example.com --screenshot
```

### Parallel Sessions
```bash
agent-browser --session site1 open https://site-a.com
agent-browser --session site2 open https://site-b.com
agent-browser --session site1 snapshot -i
agent-browser --session site2 snapshot -i
```

### Connect to Existing Chrome
```bash
agent-browser --auto-connect open https://example.com
agent-browser --cdp 9222 snapshot
```

## Security

### Content Boundaries (Recommended)
Wrap page output in markers to distinguish from tool output:
```bash
export AGENT_BROWSER_CONTENT_BOUNDARIES=1
agent-browser snapshot
```

### Domain Allowlist
```bash
export AGENT_BROWSER_ALLOWED_DOMAINS="example.com,*.example.com"
```

### Output Limits
```bash
export AGENT_BROWSER_MAX_OUTPUT=50000
```

## Batch Execution

Run multiple commands efficiently:
```bash
echo '[
  ["open", "https://example.com"],
  ["snapshot", "-i"],
  ["click", "@e1"],
  ["screenshot", "result.png"]
]' | agent-browser batch --json
```

## Advanced: JavaScript Evaluation

```bash
# Simple expressions
agent-browser eval 'document.title'
agent-browser eval 'document.querySelectorAll("img").length'

# Complex JS: use --stdin
agent-browser eval --stdin <<'EVALEOF'
JSON.stringify(Array.from(document.querySelectorAll("a")).map(a => a.href))
EVALEOF
```

## iOS Simulator (macOS)

```bash
agent-browser device list
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1
agent-browser -p ios screenshot mobile.png
```

Requirements: macOS with Xcode and Appium (`npm install -g appium && appium driver install xcuitest`)

## Important: Ref Lifecycle

Refs (`@e1`, `@e2`) are invalidated when the page changes. **Always re-snapshot after:**
- Clicking links or buttons that navigate
- Form submissions
- Dynamic content loading

```bash
agent-browser click @e5              # Navigates to new page
agent-browser snapshot -i            # MUST re-snapshot
agent-browser click @e1              # Use new refs
```

## Session Cleanup

Always close when done:
```bash
agent-browser close
```

For ephemeral environments, auto-shutdown after inactivity:
```bash
AGENT_BROWSER_IDLE_TIMEOUT_MS=60000 agent-browser open example.com
```

## Reference Commands

```bash
# Check console errors
agent-browser console
agent-browser errors

# Open DevTools
agent-browser inspect

# Record session
agent-browser record start demo.webm
agent-browser record stop
```

## Output Artifacts

Save screenshots and snapshots to `.artifacts/browser/` for organized output:
```bash
mkdir -p .artifacts/browser/screenshots
agent-browser screenshot .artifacts/browser/screenshots/page.png
agent-browser snapshot --json > .artifacts/browser/snapshot.json
```
