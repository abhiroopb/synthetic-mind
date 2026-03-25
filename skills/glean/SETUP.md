# Glean skill setup

## Prerequisites

- **VPN**: Must be connected to corporate VPN
- **SSO**: Access to your company's SSO portal
- **uv**: Python package runner (`brew install uv`)

## First run

The CLI auto-authenticates on first use. It will open a browser for SSO login.
Tokens are cached at `~/.config/block-glean/tokens.json`.

To authenticate manually:

```bash
scripts/block-glean-cli auth login
```

## Troubleshooting

If authentication fails, ensure VPN is connected and try:

```bash
scripts/block-glean-cli auth login --reauth
```

If port 8030 is in use (from a previous interrupted auth flow):

```bash
lsof -ti :8030 | xargs kill
```
