# Google Calendar Skill — Setup

One-time setup for the gcal skill.

## Prerequisites

### Install uv (if needed)

```bash
which uv || curl -LsSf https://astral.sh/uv/0.10.0/install.sh | sh
```

> **Tip:** You can also install via Homebrew: `brew install uv`

### Authenticate

```bash
cd {{SKILL_DIR}} && uv run gcal-cli.py auth login
```

This opens a browser for Google OAuth. Credentials are stored at `~/.config/gcal-skill/credentials.json`.

### Verify

```bash
cd {{SKILL_DIR}} && uv run gcal-cli.py auth status
```

Should show `"authenticated": true`.

## Troubleshooting

| Error | Solution |
|-------|----------|
| "Not authenticated" | Run `uv run gcal-cli.py auth login` |
| "Insufficient permissions" | Run `uv run gcal-cli.py auth login --force` |
| "Calendar not found" | Check calendar ID with `uv run gcal-cli.py calendars list` |
| "orderBy requires singleEvents" | Use `--single-events` (default) with `--order-by startTime` |

## Logout

```bash
cd {{SKILL_DIR}} && uv run gcal-cli.py auth logout
```
