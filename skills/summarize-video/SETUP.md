# Summarize Video Skill Setup

## Prerequisites

- **Chrome open** with a profile logged into Okta (for video.square.com SSO)

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

## 2. Install Blockcell MCP

Add to the `"mcpServers"` section of `~/.claude.json`:

```json
"blockcell": {
  "type": "stdio",
  "command": "uvx",
  "args": ["mcp_blockcell@latest"],
  "env": {}
}
```

---

## 3. Install Python dependency

```bash
pip3 install markdown==3.7 --break-system-packages -q
```

---

## Verify Setup

After installing, restart Claude Code (Cmd+Q, relaunch), then check MCP servers are connected:

```
/mcp
```

You should see both `chrome-devtools` and `blockcell` listed with a green status.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Video page requires login | Complete Okta SSO in Chrome before running the skill — the MCP will wait for the page to load |
| `markdown` module not found | `pip3 install markdown==3.7 --break-system-packages` |
| Blockcell upload fails | Check that the Blockcell MCP is connected via `/mcp` |
| MCP servers not showing | Restart Claude Code after adding to `~/.claude.json` |
