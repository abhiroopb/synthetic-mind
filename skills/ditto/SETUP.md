# Ditto Setup

## Prerequisites

1. **Square VPN**: Connect to Cloudflare WARP (Square VPN)
2. **sq CLI**: Install and authenticate
   ```bash
   brew install squareup/tap/sq
   sq login
   ```

## Related Skills

- **toolbox** — Required for post-creation steps like card approval/activation, credit decisions, and transaction simulation
- **lending-scenarios** — Orchestrates ditto + toolbox for common lending test account setups
- **launchdarkly-cli** — For managing LaunchDarkly flags/segments via `ldcli`
