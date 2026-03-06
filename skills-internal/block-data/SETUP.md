# Business Metrics Skill Setup

## Prerequisites

- **VPN connected** (required for Snowflake Okta SSO authentication)
- **`SNOWFLAKE_USER`** set to your corporate email (e.g., `user@example.com`)

Add to your shell profile (`~/.zshrc` or `~/.bashrc`) to persist across sessions:
```bash
export SNOWFLAKE_USER="your_email@example.com"
```

---

## Install the MCP Server

### Option A: Auto-install via CLI

```bash
claude mcp add --scope user -e SNOWFLAKE_USER=your_email@example.com mcp-metrics -- uvx mcp_metrics@latest
```

**Important:** After running, verify `~/.claude.json` has `"command": "uvx"` (not `"--"`). If the CLI mangled the command, edit `~/.claude.json` directly — see Option B below.

### Option B: Manual configuration

Add the following to the `"mcpServers"` section of `~/.claude.json`:

```json
"mcp-metrics": {
  "type": "stdio",
  "command": "uvx",
  "args": ["mcp_metrics@latest"],
  "env": { "SNOWFLAKE_USER": "your_email@example.com" }
}
```

---

## First-Time Authentication

After installing, restart Claude Code:
1. Press Cmd+Q to quit
2. Relaunch Claude Code
3. A browser window will open for Okta SSO login — complete the authentication
4. Run your query (e.g., "What's our GPV?")

Snowflake tokens are cached locally and remain valid for hours/days. If authentication expires, a new browser window will open automatically.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not detected after install | Restart Claude Code (Cmd+Q, relaunch) |
| `"command": "--"` in ~/.claude.json | CLI bug — edit the file manually per Option B above |
| Okta browser doesn't open | Ensure VPN is connected and `SNOWFLAKE_USER` is set |
| Snowflake auth expired | Re-run any query to trigger a new browser auth flow |
| `SNOWFLAKE_USER not set` | Add `export SNOWFLAKE_USER="email@example.com"` to `~/.zshrc` |
