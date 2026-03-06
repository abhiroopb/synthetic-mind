# Setup

## Prerequisites

### gdrive skill
This skill depends on the `gdrive` skill (v0.3.0+) for Google Docs read/write operations.

Install it from the [squareup/agents marketplace](https://github.com/squareup/agents/tree/main/skills/gdrive):
```bash
sq agents skills add gdrive
```

### Authenticate with Google Drive
```bash
cd ~/.claude/skills/gdrive && uv run gdrive-cli.py auth login
```

Credentials are stored at `~/.config/gdrive-skill/credentials.json`.

Check auth status:
```bash
cd ~/.claude/skills/gdrive && uv run gdrive-cli.py auth status
```

### GitHub CLI (optional)
The `gh` CLI is needed if you provide PR links for additional context:
```bash
gh auth status
```

### slack skill (optional)
Required for searching Slack channels for feature discussions (Step 2).
```bash
sq agents skills add slack
```

### linear skill (optional)
Required for creating Linear tickets from bugs logged in the Bugs tab (Step 9).
```bash
sq agents skills add linear
```
