# Looker Skill Setup

## Option 1: Browser Login (OAuth PKCE, recommended, macOS only)

No setup required. Run the login command and authenticate in your browser. Tokens are stored in the macOS Keychain:

```bash
uvx --with looker-sdk --with requests python {{SKILL_DIR}}/scripts/looker_cli.py login
```

This opens Looker in your browser, authenticates via OAuth PKCE, and saves the token to your macOS Keychain. Tokens auto-refresh on subsequent uses.

## Option 2: API3 Credentials

Generate API3 keys from the Looker UI and set them as environment variables:

1. Go to https://square.cloud.looker.com
2. Navigate to **Admin > Users > your user > API Keys**
3. Click **New API Key** to generate a client ID and secret
4. Set environment variables:

```bash
export LOOKERSDK_CLIENT_ID="your_client_id"
export LOOKERSDK_CLIENT_SECRET="your_client_secret"
```

API3 credentials auto-refresh per request via the SDK (no manual renewal needed). Works on all platforms.

## Prerequisites

- **WARP VPN** must be connected for all Looker API access
- **uv** must be installed: `brew install uv`
- **Looker access**: You need an active Looker account at square.cloud.looker.com

## Verify

```bash
uvx --with looker-sdk --with requests python {{SKILL_DIR}}/scripts/looker_cli.py me
```
