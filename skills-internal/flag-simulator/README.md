# Flag Simulator Skill

CLI replacement for [go/flag-simulator](https://go.internal.example.com/flag-simulator) ([console.internal.example.com/flag-simulator](https://console.internal.example.com/flag-simulator)).

Evaluate LaunchDarkly feature flags against specific merchant/unit/person/device contexts using the Experiment Relay API — without leaving the terminal.

## Prerequisites

- **VPN** — Must be connected to Square VPN (Cloudflare WARP)
- **jq** — For JSON formatting. Install with `brew install jq`.

## Parameters

| Parameter | Flag | Default | Description |
|-----------|------|---------|-------------|
| Flag key | `--flag-key` | (required) | The LaunchDarkly flag key to evaluate |
| Token | `--token` | (required*) | Context token value (e.g., merchant token) |
| Token type | `--token-type` | `MERCHANT` | `MERCHANT`, `UNIT`, `PERSON`, `SQUARE_MOBILE_DEVICE` |
| Project | `--project` | `PIE` | `PIE`, `CAPITAL`, `SQUARE_CONSOLE`, `TIDAL`, `SHOP` |
| Environment | `--env` | `production` | `production`, `staging`, `sandbox` |
| Flag type | `--flag-type` | `BOOLEAN` | `BOOLEAN`, `STRING`, `INTEGER`, `DOUBLE`, `JSON` |
| Platform | `--platform` | `Server` | `Server`, `Mobile`, `Dashboard Web` |
| App vertical | `--app-vertical` | `SPOS` | See supported verticals below |
| App version | `--app-version` | `6.95` | App version string |
| Mobile OS | `--mobile-os` | `iOS` | `iOS` or `Android` |
| Device | `--device` | `COTS` | Android device: `X2A`, `X2B`, `X2C`, `T2A`, `T2B`, `T3A`, `COTS` |
| String attribute | `--attribute` | — | `key=value` (repeatable) |
| Int attribute | `--attribute-int` | — | `key=value` (repeatable) |
| Bool attribute | `--attribute-bool` | — | `key=value` (repeatable) |
| Double attribute | `--attribute-double` | — | `key=value` (repeatable) |
| Multi-context | `--context` | — | `TYPE:TOKEN` (repeatable, triggers multi-context mode) |
| Default context | `--default-context-type` | `MERCHANT` | Default context type for multi-context mode |

\* `--token` is required for single-context mode. Use `--context` for multi-context mode.

## Examples

### Simple boolean flag evaluation

```bash
scripts/evaluate.sh --flag-key waiter-orders-mode --token MLN7XZDSEWET1
```

### String flag on staging

```bash
scripts/evaluate.sh --flag-key menu-layout --token UNIT456 \
  --token-type UNIT --flag-type STRING --env staging
```

### iOS Mobile evaluation

```bash
scripts/evaluate.sh --flag-key ios-feature --token M123 \
  --platform Mobile --mobile-os iOS --app-vertical SPOS --app-version 6.95
```

### Android/Squid evaluation on X2C

```bash
scripts/evaluate.sh --flag-key squid-feature --token M123 \
  --platform Mobile --mobile-os Android --device X2C \
  --app-vertical Restaurants --app-version 6.90
```

### Dashboard Web

```bash
scripts/evaluate.sh --flag-key dashboard-feature --token M123 \
  --platform "Dashboard Web"
```

### Custom attributes

```bash
scripts/evaluate.sh --flag-key ab-test --token M123 \
  --attribute country=US --attribute-int tier=3 --attribute-bool premium=true
```

### Multi-context evaluation

```bash
scripts/evaluate.sh --flag-key cross-context-flag \
  --context MERCHANT:M123 --context PERSON:P456 \
  --default-context-type MERCHANT
```

## How It Works

1. The script constructs a JSON payload with the flag key, project, context(s), flag type, and optional user attributes
2. It POSTs to the **Experiment Relay API** at `https://{domain}/1.0/features/flag-evaluation-details`
3. An `Origin` header matching the domain is included to bypass the Trogdor CSRF check (safe because authentication is via Cloudflare Access/VPN, not browser cookies)
4. The response is formatted with jq, HTML tags are stripped from the evaluation reason, and the LaunchDarkly link is extracted
5. On `WRONG_TYPE` errors, the agent loads the `launchdarkly` skill to look up the correct flag type and retries

## Limitations vs Console UI

- **No saved contexts** — Console UI lets you save and reuse evaluation contexts; the CLI requires specifying them each time
- **No visual targeting rule breakdown** — Console shows a graphical breakdown of which rule matched; the CLI shows the text reason only
- **No bulk evaluation** — Console can evaluate multiple flags at once; the CLI evaluates one at a time (but the agent can run it multiple times)
- **No flag search/browse** — Use the [launchdarkly skill](../launchdarkly/SKILL.md) for searching and browsing flags
