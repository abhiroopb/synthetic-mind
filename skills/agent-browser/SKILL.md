---
name: agent-browser
description: Debug visual bugs and interact with web apps using agent-browser CLI. Use when debugging, inspecting, navigating, filling forms, clicking buttons, taking screenshots, scraping data, testing web apps, or automating browser tasks. Supports desktop browsers and iOS Simulator (Mobile Safari). 93% less context than Playwright MCP.
roles: [frontend]
allowed-tools: Bash(npx agent-browser:*), Bash(agent-browser:*)
metadata:
  author: jom
  version: "0.3.0"
  status: experimental
---

# Agent Browser Skill

Fast, token-efficient browser automation for debugging and interaction.

**STOP** if `agent-browser` is not installed. See [SETUP.md](SETUP.md) for installation.

## Core Workflow

1. **Open**: `agent-browser open <url>`
2. **Snapshot**: `agent-browser snapshot -i --json` — returns interactive elements with refs (`@e1`, `@e2`)
3. **Interact**: Use refs to click, fill, etc.
4. **Re-snapshot**: After navigation or DOM changes, snapshot again (refs reset)

Commands can be chained with `&&` when you don't need intermediate output: `agent-browser open <url> && agent-browser wait --load networkidle && agent-browser snapshot -i`

Run commands separately when you need to parse output first (e.g., snapshot to discover refs, then interact).

## Commands

```bash
# Navigation
agent-browser open <url>              # Navigate (aliases: goto, navigate)
agent-browser back / forward / reload
agent-browser close

# Snapshot
agent-browser snapshot -i             # Interactive elements only (recommended)
agent-browser snapshot -i -C          # Include cursor-interactive elements
agent-browser snapshot -i --json      # Structured output (best for agents)
agent-browser snapshot -c -d 3        # Compact, depth-limited
agent-browser snapshot -s "#main"     # Scope to CSS selector

# Interact (use @refs from snapshot)
agent-browser click @e1               # Click (--new-tab to open in new tab)
agent-browser fill @e2 "text"         # Clear and type
agent-browser type @e2 "text"         # Type without clearing
agent-browser press Enter             # Press key (Enter, Tab, Control+a)
agent-browser hover / check / uncheck / select @e1 "value"
agent-browser scroll down 500
agent-browser upload @e1 file.png     # Upload files

# Get information
agent-browser get text @e1 / get value @e1
agent-browser get title / get url

# Screenshots
agent-browser screenshot              # Base64 PNG to stdout
agent-browser screenshot path.png     # Save to file
agent-browser screenshot --full       # Full page
agent-browser screenshot --annotate   # Numbered labels on elements (vision mode)
agent-browser pdf output.pdf

# Wait
agent-browser wait @e1                # Wait for element
agent-browser wait 2000               # Wait milliseconds
agent-browser wait --text "Success"   # Wait for text
agent-browser wait --load networkidle # Wait for network idle
agent-browser wait --url "**/dash"    # Wait for URL pattern
agent-browser wait --fn "expr"        # Wait for JS condition
```

## Ref Lifecycle

Refs (`@e1`, `@e2`) are invalidated when the page changes. Always re-snapshot after clicking links, form submissions, or dynamic content loading.

```bash
agent-browser click @e5              # Navigates to new page
agent-browser snapshot -i            # MUST re-snapshot — old refs are gone
agent-browser click @e1              # Now use new refs
```

## Examples

**Investigate visual bug:**
```bash
agent-browser open http://localhost:3000
agent-browser snapshot -i --json
agent-browser screenshot bug.png
agent-browser close
```

**Form submission:**
```bash
agent-browser open https://example.com/form
agent-browser snapshot -i --json
# e1=Email, e2=Password, e3=Submit
agent-browser fill @e1 "user@example.com" && agent-browser fill @e2 "secret123"
agent-browser click @e3
agent-browser wait --load networkidle && agent-browser snapshot -i --json
```

**Save and restore auth state:**
```bash
agent-browser open https://app.example.com/login && agent-browser snapshot -i --json
agent-browser fill @e1 "username" && agent-browser fill @e2 "secret" && agent-browser click @e3
agent-browser wait --url "**/dashboard"
agent-browser state save auth.json
# Later: agent-browser state load auth.json
```

**iOS Simulator (Mobile Safari):**
```bash
agent-browser -p ios --device "iPhone 16 Pro" open https://example.com
agent-browser -p ios snapshot -i
agent-browser -p ios tap @e1          # Tap (alias for click)
agent-browser -p ios swipe up         # Mobile gesture
agent-browser -p ios close
```

## Reference Files

| File | Load when |
|------|-----------|
| [SETUP.md](SETUP.md) | First-time install, iOS Simulator setup |
| [references/annotated-screenshots.md](references/annotated-screenshots.md) | Visual debugging, unlabeled buttons, canvas/chart elements |
| [references/advanced-interactions.md](references/advanced-interactions.md) | Tabs, frames, semantic locators, dialogs, network mocking, browser settings |
| [references/javascript-eval.md](references/javascript-eval.md) | Running JS in the browser, extracting data via scripts |
| [references/sessions.md](references/sessions.md) | Persisting auth, parallel sessions, connecting to existing Chrome |
| [references/advanced-features.md](references/advanced-features.md) | Local files, slow pages, profiling, configuration |

## Related Skills

- `playwright` — Use when running Playwright e2e test suites, not ad-hoc browser interaction
