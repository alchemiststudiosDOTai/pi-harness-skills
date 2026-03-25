---
title: "agent-browser authentication patterns"
link: "agent-browser-authentication"
type: reference
ontological_relations:
  - relates_to: [[agent-browser]]
tags: [reference, agent-browser, auth, login, oauth, 2fa]
uuid: "auto-generated"
created_at: "2026-03-25T00:00:00Z"
---

# Authentication Patterns

Strategies for automating login and authentication flows.

## Quick Comparison

| Method | Best For | Security | Automation |
|--------|----------|----------|------------|
| Auth Vault | Recurring logins | High (encrypted) | One command |
| State Import | One-off tasks | Medium (plaintext) | Manual save |
| Session Name | Persistent sessions | Medium | Auto-save |
| Profile | Long-term use | High | Permanent |

## Auth Vault (Recommended)

Encrypted credential storage for recurring logins.

### Setup

```bash
# Save credentials (recommended: pipe password via stdin)
echo "$PASSWORD" | agent-browser auth save myapp \
  --url https://app.example.com/login \
  --username user@example.com \
  --password-stdin

# Verify saved
agent-browser auth list
```

### Login

```bash
agent-browser auth login myapp
# Automatically:
# 1. Navigates to login URL
# 2. Waits for form selectors
# 3. Fills credentials
# 4. Submits form
# 5. Waits for post-login navigation
```

### Manage Credentials

```bash
agent-browser auth list           # Show all saved
agent-browser auth show myapp     # View (no password)
agent-browser auth delete myapp   # Remove
```

### Encryption

```bash
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
# Now auth vault encrypts at rest
```

## Cookie-Based Authentication

### Save Cookies After Login

```bash
# Login manually
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "user@example.com"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --load networkidle

# Save session state
agent-browser state save ./auth.json
```

### Reuse Cookies

```bash
agent-browser state load ./auth.json
agent-browser open https://app.example.com/dashboard
# Already authenticated
```

## OAuth Flow

### Automated OAuth

```bash
# Start OAuth
agent-browser open https://oauth.provider.com/authorize?client_id=xxx&redirect_uri=https://app.example.com/callback
agent-browser snapshot -i

# Click "Authorize" button
agent-browser click @e1
agent-browser wait --url "*callback*"
agent-browser wait --load networkidle

# Extract authorization code from URL
agent-browser get url
# Parse code from: https://app.example.com/callback?code=xxx

# Save state after OAuth
agent-browser state save ./oauth-state.json
```

### OAuth with State Persistence

```bash
# After successful OAuth
agent-browser state save ./oauth-state.json

# Later: restore OAuth session
agent-browser state load ./oauth-state.json
agent-browser open https://app.example.com
```

## Two-Factor Authentication (2FA)

### TOTP (Time-based OTP)

```bash
agent-browser open https://app.example.com/login
agent-browser snapshot -i
agent-browser fill @e1 "email@example.com"
agent-browser fill @e2 "password"
agent-browser click @e3
agent-browser wait --text "Enter code"

# Generate TOTP (requires secret key)
TOTP=$(oathtool --totp -b "$SECRET_KEY")
agent-browser fill @e_otp "$TOTP"
agent-browser click @e_submit
```

### SMS OTP

```bash
# Trigger SMS
agent-browser fill @e_phone "+1234567890"
agent-browser click @e_send_code
agent-browser wait --text "Enter code"

# Prompt user for SMS code (manual step)
read -p "Enter SMS code: " SMS_CODE
agent-browser fill @e_otp "$SMS_CODE"
agent-browser click @e_verify
```

## Token Refresh

### Handle Expired Tokens

```bash
agent-browser open https://app.example.com
agent-browser snapshot -i

# Check for token expiration
agent-browser eval --stdin <<'EOF'
const expired = document.body.innerText.includes('Session expired');
const refreshBtn = document.querySelector('[data-action="refresh-token"]');
expired ? 'expired' : 'valid';
EOF

# Refresh if needed
agent-browser click @e_refresh
agent-browser wait --load networkidle
```

## Session Import from Browser

Connect to your existing browser session.

### macOS

```bash
# Chrome with remote debugging
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222

# Then in another terminal:
agent-browser --auto-connect state save ./imported-auth.json
```

### Linux

```bash
google-chrome --remote-debugging-port=9222
agent-browser --auto-connect state save ./imported-auth.json
```

### Windows

```bash
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
agent-browser --auto-connect state save ./imported-auth.json
```

## Persistent Profiles

### Create Profile

```bash
# First login
agent-browser --profile ~/.myapp open https://app.example.com/login
# ... complete login ...

# Profile persists all data
```

### Reuse Profile

```bash
agent-browser --profile ~/.myapp open https://app.example.com
# No login needed - fully authenticated
```

## SAML/SSO

### SAML Flow

```bash
agent-browser open https://app.example.com/login
agent-browser snapshot -i

# Click SSO/SAML button
agent-browser click @e_sso

# Wait for redirect to IdP
agent-browser wait --url "*identity.provider*"
agent-browser wait --load networkidle

# Fill IdP credentials
agent-browser snapshot -i
agent-browser fill @e_username "user@company.com"
agent-browser fill @e_password "password"
agent-browser click @e_login

# Wait for SAML assertion and redirect back
agent-browser wait --url "*app.example.com*"
agent-browser wait --load networkidle

# Save state
agent-browser state save ./saml-auth.json
```

## Security Best Practices

1. **Never hardcode passwords** - use environment variables or auth vault
2. **Pipe passwords via stdin** - avoids shell history:
   ```bash
   echo "$PASSWORD" | agent-browser auth save myapp --password-stdin
   ```
3. **Encrypt state files** - use `AGENT_BROWSER_ENCRYPTION_KEY`
4. **Add auth files to .gitignore** - prevent accidental commits
5. **Use content boundaries** - helps LLM distinguish page content
6. **Rotate credentials** - periodically update stored passwords
7. **Clean up old states** - remove unused session files

## Troubleshooting

### Login Form Not Found

```bash
agent-browser snapshot -i
# Verify selectors match expected form elements
# May need custom wait: agent-browser wait --text "Sign in"
```

### Session Expires Mid-Automation

```bash
# Check session validity
agent-browser get text @e_error  # Look for "expired" or "re-login"

# If expired, re-authenticate
agent-browser state load ./auth.json
```

### Captcha Handling

Captchas cannot be solved programmatically. Options:
1. Use browser fingerprinting to appear human
2. Use service like 2Captcha (external service)
3. Ask user to solve manually (pause automation)
