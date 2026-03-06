---
name: flag-simulator
description: "Evaluate LaunchDarkly feature flags via an evaluation relay API. CLI replacement for a web-based flag simulator UI. Use when user asks to evaluate a flag, check flag value, simulate flag evaluation, test flag targeting, look up flag result, query flag state, resolve flag variation, inspect flag output, or mentions flag-simulator."
roles: [frontend, backend, mobile]
allowed-tools: [Bash(scripts/evaluate.sh:*), Bash(jq:*), Read]
metadata:
  version: "0.1.0"
  status: experimental
---

# Flag Simulator

Evaluate LaunchDarkly feature flags via an evaluation relay API. This is a CLI replacement for a web-based flag simulator UI.

**STOP** and ask the user if: the flag key is unknown or ambiguous, the token (account/unit/person) is missing, or the platform (Server, Mobile, Dashboard Web) is not specified.

## Default Assumptions

When the user doesn't specify, use these defaults:

| Parameter | Default |
|-----------|---------|
| Project | `DEFAULT` |
| Environment | `production` |
| Flag type | `BOOLEAN` |

## Script Usage

Run `scripts/evaluate.sh` with these parameters:

```bash
scripts/evaluate.sh \
  --flag-key <flag_key> \
  --token <token_value> \
  [--token-type <MERCHANT|UNIT|PERSON|DEVICE>] \
  [--project <DEFAULT|CAPITAL|CONSOLE|MUSIC|SHOP>] \
  [--env <production|staging|sandbox>] \
  [--flag-type <BOOLEAN|STRING|INTEGER|DOUBLE|JSON>] \
  [--platform <Server|Mobile|"Dashboard Web">] \
  [--app-vertical <POS|Invoices|Appointments|Restaurants|Retail|Dashboard|...>] \
  [--app-version <version>] \
  [--mobile-os <iOS|Android>] \
  [--device <X2A|X2B|X2C|T2A|T2B|T3A|COTS>] \
  [--attribute <key=value>] \
  [--attribute-int <key=value>] \
  [--attribute-bool <key=value>] \
  [--attribute-double <key=value>] \
  [--context <type:token>] \
  [--default-context-type <MERCHANT|UNIT|PERSON|DEVICE>]
```

## Mapping User Requests to Parameters

### Simple evaluation

> "What's the value of `waiter-orders-mode` for account MLN7XZDSEWET1?"

```bash
scripts/evaluate.sh --flag-key waiter-orders-mode --token MLN7XZDSEWET1
```

Defaults apply: project=DEFAULT, env=production, type=BOOLEAN, token-type=MERCHANT. Platform must be specified.

### Specifying project and environment

> "Check `capital-feature` for account ABC123 in staging on the CAPITAL project"

```bash
scripts/evaluate.sh --flag-key capital-feature --token ABC123 \
  --project CAPITAL --env staging
```

### String flag type

> "What string value does `menu-layout` return for unit UNIT456?"

```bash
scripts/evaluate.sh --flag-key menu-layout --token UNIT456 \
  --token-type UNIT --flag-type STRING
```

### Mobile platform (iOS)

> "Check `ios-feature` for account M123 on iOS POS version 6.95"

```bash
scripts/evaluate.sh --flag-key ios-feature --token M123 \
  --platform Mobile --mobile-os iOS --app-vertical POS --app-version 6.95
```

### Mobile platform (Android)

> "Evaluate `android-feature` on an X2C device running Restaurants 6.90"

```bash
scripts/evaluate.sh --flag-key android-feature --token M123 \
  --platform Mobile --mobile-os Android --device X2C \
  --app-vertical Restaurants --app-version 6.90
```

### Dashboard Web platform

> "Check `dashboard-feature` for account M123 from Dashboard Web"

```bash
scripts/evaluate.sh --flag-key dashboard-feature --token M123 \
  --platform "Dashboard Web"
```

### Custom attributes

> "Evaluate `ab-test` for account M123 with attribute country=US and tier (int) = 3"

```bash
scripts/evaluate.sh --flag-key ab-test --token M123 \
  --attribute country=US --attribute-int tier=3
```

### Multi-context evaluation

> "Check `cross-context-flag` for account M123 and person P456"

```bash
scripts/evaluate.sh --flag-key cross-context-flag \
  --context MERCHANT:M123 --context PERSON:P456 \
  --default-context-type MERCHANT
```

## Interpreting Output

The script outputs a formatted JSON response with:

- **status** — `SUCCESS`, `SDK_ERROR`, `INVALID_REQUEST`, `NOT_FOUND`, `WRONG_TYPE`, `SERVICE_NOT_READY`, `MISSING_USER_TOKEN`
- **value** — The flag's evaluated value (type depends on flag_type)
- **evaluation_reason** — Human-readable explanation of why the flag returned this value (HTML stripped)
- **launchdarkly_link** — Direct link to the flag in LaunchDarkly (extracted from HTML response)
- **user_attributes** — Attributes that were sent to the evaluation
- **user_context_attributes** — Per-context attribute breakdown

### Error Messages

See `references/error-messages.md` for the full error table. On `WRONG_TYPE`, load the `launchdarkly` skill to look up the correct flag type and retry.

## Notes

- For non-Mobile platforms, a fake DEVICE context is auto-added to carry user_attributes (this matches the web UI behavior)
- Dashboard Web platform auto-injects `product=dashboard`, `platform=web`, `server.application=experiment-relay` attributes (flags are evaluated server-side via Dynamic Config)
