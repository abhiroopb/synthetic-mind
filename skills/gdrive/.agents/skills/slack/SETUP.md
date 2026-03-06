# Slack skill setup

One-time setup steps for the Slack skill.

## Install uv (if needed)

```bash
which uv || brew install uv
```

## Configure uv for Block PyPI (if needed)

```bash
mkdir -p ~/.config/uv
cat > ~/.config/uv/uv.toml << 'EOL'
native-tls = true
index-url = "https://artifactory.global.square/artifactory/api/pypi/block-pypi/simple"
EOL
```

## Authenticate

**IMPORTANT: You must be connected to WARP VPN throughout this process.**

```bash
scripts/slack-cli auth login
```

This will:
1. Open the Slack OAuth page in your browser
2. After clicking "Allow", you'll see your token displayed
3. Copy and paste the token when prompted
4. Select your default workspace

Credentials are stored at `~/.config/slack-skill/credentials.json`.

Check status: `scripts/slack-cli auth status`
