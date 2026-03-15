# Summarize Video Skill Setup

## Prerequisites

- **Chrome open** with a profile logged into your SSO provider (for video platform access)

---

## 1. Install Chrome DevTools MCP

Add to the `"mcpServers"` section of `~/.claude.json`:

```json
"chrome-devtools": {
  "type": "stdio",
  "command": "npx",
  "args": ["chrome-devtools-mcp@latest"],
  "env": {}
}
```

---

## 2. Install Python dependency

```bash
pip3 install markdown==3.7 --break-system-packages -q
```

---

## Verify Setup

After installing, restart Claude Code (Cmd+Q, relaunch), then check MCP servers are connected:

```
/mcp
```

You should see `chrome-devtools` listed with a green status.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Video page requires login | Complete SSO login in Chrome before running the skill — the MCP will wait for the page to load |
| `markdown` module not found | `pip3 install markdown==3.7 --break-system-packages` |
| MCP servers not showing | Restart Claude Code after adding to `~/.claude.json` |
