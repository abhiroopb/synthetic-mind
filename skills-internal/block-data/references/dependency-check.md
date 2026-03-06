# Dependency Check (Phase 0)

## How to Check for the Required Server

**DO NOT** run MCP tool names as Bash commands — they are tools, not shell commands.

**DO** check your available tool list for:
- `mcp__mcp-metrics__metric_store_search` → mcp_metrics server

### Check logic:
```
Look at your tool list.
If mcp__mcp-metrics__metric_store_search is present → Server is available ✅
If it is NOT present → Server is missing ❌
```

---

## Handle Startup Race Condition

**If the server appears missing on first check:**

**DO NOT immediately ask the user to install!** The server may still be initializing.

1. **Display to user:**
   ```
   ⏳ The mcp_metrics server appears to be initializing, waiting 10 seconds...
   ```

2. **Wait 10 seconds** (don't do anything, just pause)

3. **Check again** — look at your tool list again

4. **If still missing:**
   - Display: "⏳ Still waiting for server (10 more seconds)..."
   - Wait 10 more seconds
   - Check one final time

5. **After 20 seconds total:**
   - If server now available → Proceed with the user's request
   - If server still missing → Show interactive installation menu

---

## Interactive Installation Menu

**Only show this if the server is STILL missing after the 20 second wait:**

```markdown
⚠️ **Missing Required MCP Server**

After waiting, the `mcp_metrics` server is still unavailable.

**What would you like to do?**

**A. Auto-install the server**
   • Runs a single command to register the MCP server
   • Requires Claude Code restart afterward

**B. Show manual installation steps**
   • I'll display the exact command to run
   • You install at your own pace

**C. Cancel**
   • Exit and install later

**Type:** A, B, or C
```

**Wait for user response before proceeding.**

---

## Installation

### Prerequisites

The server connects to Snowflake using Okta SSO browser authentication, which requires:
- **VPN connected**
- **`SNOWFLAKE_USER` set** to the user's corporate email (e.g., `user@example.com`)

Ask the user for their corporate email before running the install command.

### If user selects Option A (Auto-install):

Ask for their corporate email, then run:
```bash
claude mcp add --scope user -e SNOWFLAKE_USER=USER_EMAIL@example.com mcp-metrics -- uvx mcp_metrics@latest
```

**Important:** After running, verify the config in `~/.claude.json` has `"command": "uvx"` (not `"--"`). If the CLI mangled the command, edit `~/.claude.json` directly to set:
```json
{
  "type": "stdio",
  "command": "uvx",
  "args": ["mcp_metrics@latest"],
  "env": { "SNOWFLAKE_USER": "USER_EMAIL@example.com" }
}
```

Then display:
```
✅ MCP server registered. Please restart Claude Code to complete installation:
  • Press Cmd+Q to quit
  • Relaunch Claude Code
  • A browser window will open for Okta SSO login on first use — complete the authentication
  • Run your query again
```

### If user selects Option B (Manual installation):

Ask for their corporate email, then display:
```
Add the following to the "mcpServers" section of ~/.claude.json:

"mcp-metrics": {
  "type": "stdio",
  "command": "uvx",
  "args": ["mcp_metrics@latest"],
  "env": { "SNOWFLAKE_USER": "YOUR_EMAIL@example.com" }
}
```

Then display:
```
After saving the file, restart Claude Code:
  • Press Cmd+Q to quit
  • Relaunch Claude Code
  • A browser window will open for Okta SSO login on first use — complete the authentication
  • Run your query again
```
