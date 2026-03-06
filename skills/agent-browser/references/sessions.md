# Sessions

## Session Persistence

Auto-save/restore cookies and localStorage across browser restarts:

```bash
agent-browser --session-name myapp open https://app.example.com/login
# ... login flow ...
agent-browser close  # State auto-saved to ~/.agent-browser/sessions/

# Next time, state is auto-loaded
agent-browser --session-name myapp open https://app.example.com/dashboard
```

Encrypt state at rest:
```bash
export AGENT_BROWSER_ENCRYPTION_KEY=$(openssl rand -hex 32)
agent-browser --session-name secure open https://app.example.com
```

Manage saved states:
```bash
agent-browser state list
agent-browser state show myapp-default.json
agent-browser state clear myapp
agent-browser state clean --older-than 7
```

## Parallel Sessions

```bash
agent-browser --session site1 open https://site-a.com
agent-browser --session site2 open https://site-b.com
agent-browser session list
```

Always close sessions when done: `agent-browser --session site1 close`

If a previous session was not closed properly, the daemon may still be running. Use `agent-browser close` to clean it up.

## Connect to Existing Chrome

```bash
# Auto-discover running Chrome with remote debugging
agent-browser --auto-connect open https://example.com
agent-browser --auto-connect snapshot

# Explicit CDP port
agent-browser connect 9222
agent-browser --cdp 9222 snapshot
```
