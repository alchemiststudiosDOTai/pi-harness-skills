---
title: "agent-browser snapshot and refs"
link: "agent-browser-snapshot-refs"
type: reference
ontological_relations:
  - relates_to: [[agent-browser]]
tags: [reference, agent-browser, snapshot, refs, selectors]
uuid: "auto-generated"
created_at: "2026-03-25T00:00:00Z"
---

# Snapshot and Refs

Understanding element references and the snapshot system.

## What is a Snapshot?

A snapshot is an accessibility tree of the current page. It shows:
- Interactive elements with refs (`@e1`, `@e2`, etc.)
- Element types (button, input, link, etc.)
- Labels and text content
- Visibility and state

## Taking Snapshots

### Basic Snapshot

```bash
agent-browser snapshot
```

Output:
```
@e1 [button] "Submit"
@e2 [textbox] "Email address"
@e3 [link] "Forgot password?"
```

### Interactive Elements Only (-i)

Recommended for automation - shows only clickable/fillable elements.

```bash
agent-browser snapshot -i
```

### Scoped Snapshot

Limit snapshot to a specific element or selector.

```bash
agent-browser snapshot -s "#form"
agent-browser snapshot -s "@e1"  # Scope to element
agent-browser snapshot -s "div.modal"
```

### JSON Output

Machine-readable format for programmatic use.

```bash
agent-browser snapshot --json > snapshot.json
agent-browser snapshot -i --json
```

## Element Refs

Refs are temporary identifiers for elements in the current snapshot.

### Format

```
@e{index}
```

Examples: `@e1`, `@e2`, `@e42`

### Using Refs

```bash
agent-browser click @e1           # Click element 1
agent-browser fill @e2 "text"     # Fill element 2
agent-browser get text @e3        # Get text from element 3
```

## Ref Lifecycle

**Important:** Refs are invalidated when the page changes.

### Refs Become Invalid After:

- Clicking links or buttons that navigate
- Form submissions
- Page navigation (open, back, forward)
- Dynamic content loading (modals, dropdowns, AJAX)
- DOM mutations

### Always Re-Snapshot After Navigation

```bash
# WRONG: Using stale refs
agent-browser open https://example.com
agent-browser snapshot -i
agent-browser click @e1  # Navigates to new page
agent-browser click @e1  # FAIL - @e1 no longer valid!

# CORRECT: Re-snapshot after navigation
agent-browser open https://example.com
agent-browser snapshot -i
agent-browser click @e1  # Navigates to new page
agent-browser snapshot -i  # Get fresh refs!
agent-browser click @e1  # Now @e1 is valid again
```

## Interactive vs Non-Interactive

### Interactive Elements (-i flag)

Only shows:
- Buttons
- Links
- Inputs (text, checkbox, radio, select)
- Textareas
- Contenteditable elements
- Menu items

### All Elements (no flag)

Shows entire accessibility tree including:
- Headings
- Paragraphs
- Images
- Tables
- Divs/spans (if semantic role)

## Troubleshooting

### Element Not Found

1. **Page not loaded**
   ```bash
   agent-browser wait --load networkidle
   agent-browser snapshot -i
   ```

2. **Element in iframe**
   ```bash
   agent-browser frame @e_iframe
   agent-browser snapshot -i
   ```

3. **Element behind overlay**
   ```bash
   agent-browser click @e_close_modal  # Close first
   agent-browser snapshot -i
   ```

4. **Lazy-loaded content**
   ```bash
   agent-browser wait @e_target_element
   agent-browser snapshot -i
   ```

### Wrong Element Clicked

1. **Verify element position**
   ```bash
   agent-browser screenshot --annotate
   # Check element numbers
   ```

2. **Scope to container**
   ```bash
   agent-browser snapshot -s "div.specific-container"
   ```

### Element Hidden/Disabled

```bash
agent-browser wait @e1 --state visible
# Or force click (not recommended - may indicate wrong element)
agent-browser click @e1 --force
```

## Semantic Locators (Alternative to Refs)

When refs aren't available or reliable.

### `find` Command

```bash
agent-browser find text "Sign In" click
agent-browser find label "Email" fill "user@test.com"
agent-browser find role button click --name "Submit"
agent-browser find placeholder "Search" type "query"
agent-browser find testid "submit-btn" click
```

### CSS Selectors

```bash
agent-browser click "button.primary"
agent-browser fill "input[name='email']" "test@example.com"
agent-browser screenshot --selector "#main-content"
```

### XPath

```bash
agent-browser click "//button[contains(text(), 'Submit')]"
```

## Iframes

Iframe content is automatically inlined in snapshots.

```bash
agent-browser snapshot -i
# @e1 [Iframe] "payment-frame"
#   @e2 [input] "Card number"
#   @e3 [input] "Expiry"

# Interact directly - no frame switch needed!
agent-browser fill @e2 "4111111111111111"
agent-browser fill @e3 "12/28"

# Scope to iframe explicitly
agent-browser frame @e1
agent-browser snapshot -i  # Only iframe content

# Return to main frame
agent-browser frame main
```

## Annotated Screenshots

Combine snapshot with visual reference.

```bash
agent-browser screenshot --annotate
```

Output:
```
@e1 [button] "Submit"
@e2 [link] "Home"
@e3 [textbox] "Email"

Screenshot saved to: /tmp/screenshot-xxx.png
```

Numbers on screenshot match refs - use to verify correct element.

## Best Practices

1. **Always snapshot before interacting** - never assume element positions
2. **Re-snapshot after any navigation** - refs are invalidated
3. **Use `-i` flag** - interactive elements only is clearer
4. **Use JSON for programmatic access** - easier to parse
5. **Combine with waits** - wait for elements before snapshotting
6. **Check annotated screenshots** - verify correct elements
