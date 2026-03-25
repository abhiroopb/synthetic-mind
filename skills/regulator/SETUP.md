# Regulator Skill Setup

## Prerequisites

- **VPN connected** (required for all queries)
- **Registry group access** — request via your internal registry:
  - `locations--users` — for merchant and location queries
  - `payments--users` — for payment queries

---

## Install the MCP Server

The `mcp_regulator` package is published to your internal package registry. Configure `uv` to use it first:

```bash
mkdir -p ~/.config/uv
cat >> ~/.config/uv/uv.toml << 'EOF'
native-tls = true
index-url = "https://artifacts.internal.example.com/api/pypi/simple"
EOF
```

### Option A: Claude Code (auto-install)

```bash
claude mcp add --scope user mcp-regulator -- uvx mcp_regulator@latest
```

**Important:** After running, verify `~/.claude.json` has `"command": "uvx"` (not `"--"`). If the CLI mangled the command, edit `~/.claude.json` directly — see Option B.

### Option B: Claude Code (manual config)

Add to the `"mcpServers"` section of `~/.claude.json`:

```json
"mcp-regulator": {
  "type": "stdio",
  "command": "uvx",
  "args": ["mcp_regulator@latest"]
}
```

### Option C: Goose

1. Go to **Settings → Extensions → Add**
2. Set **Type** to **StandardIO**
3. Enter command (replace `<your_ldap>`):
   ```
   uv run /Users/<your_ldap>/Development/mcp/mcp_regulator/.venv/bin/mcp_regulator
   ```

---

## Quick Check

After restarting your agent, verify the MCP is connected:

```bash
# Claude Code
claude mcp list
```

You should see `mcp-regulator` listed. In a conversation, look for `mcp__mcp-regulator__query_merchant` in your available tools.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Server not detected after install | Restart Claude Code (Cmd+Q, relaunch) |
| `"command": "--"` in `~/.claude.json` | CLI bug — edit the file manually per Option B |
| Permission denied on queries | Request `locations--users` / `payments--users` via Registry |
| VPN errors / connection refused | Ensure you're connected to VPN |
| Package not found | Ensure package registry `uv` config is set (see above) |
