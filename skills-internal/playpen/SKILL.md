---
name: playpen
description: "Deploy and debug applications using Square's Playpen service. Use when user needs to sync code to a playpen, view logs, debug running services, manage playpen instances, make RPC calls to playpens, or test with feature flag overrides."
metadata:
  author: jom
  version: "0.2.0"
  status: experimental
---

# Playpen

Deploy and debug applications using `sq playpen` commands. Playpen creates ephemeral development environments in Kubernetes for testing code changes.

## Prerequisites

- VPN connected
- `sq` CLI installed
- Application must be registered in Playpen (check with `sq playpen list -a <app>`)

**Note**: Playpens run in the staging environment and can modify staging data. Use with caution.

---

## Commands Overview

| Command | Description |
|---------|-------------|
| `sq playpen sync` | Sync local changes to a playpen and restart the service |
| `sq playpen attach` | Attach to an existing playpen without re-syncing |
| `sq playpen exec` | Execute a command in a playpen |
| `sq playpen logs` | Stream logs from a playpen |
| `sq playpen list` | List any playpen instances for an application |
| `sq playpen down` | Spin down all playpens owned by user |
| `sq playpen heap-dump` | Dump heap and transfer to local machine |
| `sq playpen stack-dump` | Dump stack and display in terminal |
| `sq playpen profile` | Run async-profiler and download flamegraph |

---

## Specifying an Application

Most commands auto-detect the app from your current directory. If detection fails, use `-a <app>`:

```bash
sq playpen list -a dashboard
sq playpen sync -a my-service
sq playpen logs -a my-service
```

---

## List Playpens

List all playpen instances for an application:

```bash
# Auto-detect app from current directory
sq playpen list

# Specify app explicitly
sq playpen list -a dashboard
```

---

## Sync Command

Sync local changes to a playpen and restart the service:

```bash
# From app directory (auto-detect)
sq playpen sync

# Specify app
sq playpen sync -a my-service

# Specify deployment type (e.g., RPC pods vs jobs pods)
sq playpen sync -a my-service --deployment my-service-jobs

# Run in background (useful for AI agents or scripts)
sq playpen sync --no-attach
```

This is the primary command for deploying code changes to a playpen environment.

---

## Attach Command

Attach to an existing playpen without re-syncing:

```bash
sq playpen attach
sq playpen attach -a my-service
```

Use when you want to reconnect to a running playpen without pushing new changes.

---

## Logs

Stream logs from a running playpen:

```bash
sq playpen logs
sq playpen logs -a my-service
```

Useful for debugging application behavior in real-time.

---

## Execute Commands

Run arbitrary commands inside the playpen:

```bash
sq playpen exec <command>
sq playpen exec -a my-service <command>
```

### Examples

```bash
# Run a shell command
sq playpen exec ls -la

# Check environment
sq playpen exec env | grep NODE

# Run a script
sq playpen exec ./run-test.sh
```

---

## Spin Down

Spin down all playpens owned by the current user:

```bash
sq playpen down
```

Use to clean up resources when done with debugging.

---

## Debugging Commands

### Heap Dump

Dump the heap and transfer to local machine for analysis:

```bash
sq playpen heap-dump
sq playpen heap-dump -a my-service
```

Useful for investigating memory issues or leaks.

### Stack Dump

Dump the stack and display in terminal:

```bash
sq playpen stack-dump
sq playpen stack-dump -a my-service
```

Useful for diagnosing deadlocks or seeing what threads are doing.

### Profiling

Run async-profiler and download a flamegraph:

```bash
sq playpen profile
sq playpen profile -a my-service
```

Generates a flamegraph for performance analysis.

---

## Common Workflows

### Deploy and Test Changes

```bash
# 1. Make local code changes
# 2. Sync to playpen
sq playpen sync

# 3. Watch logs (in another terminal)
sq playpen logs

# 4. Test your changes
# 5. Clean up when done
sq playpen down
```

### Debug Performance Issues

```bash
# 1. Attach to existing playpen
sq playpen attach

# 2. Generate flamegraph
sq playpen profile

# 3. Analyze the flamegraph for hotspots
```

### Investigate Memory Issues

```bash
# 1. Sync or attach to playpen
sq playpen sync

# 2. Reproduce the issue
# 3. Capture heap dump
sq playpen heap-dump

# 4. Analyze with a memory profiler (e.g., VisualVM, MAT)
```

### Diagnose Thread Issues

```bash
# 1. Attach to playpen
sq playpen attach

# 2. Capture stack dump
sq playpen stack-dump

# 3. Review thread states for deadlocks or blocking
```

---

## Routing RPC Calls to Playpens

Route requests to your playpen instead of production pods. For RPC call syntax, see the `rpc-admin-console` skill.

### Using --playpen Flag (Recommended)

```bash
sq curl --playpen <app> -L --post302 'https://<app>.stage.sqprod.co/_admin/rpc/call' \
  -H 'content-type: application/json' \
  --data-raw '{"service_name": "...", "method_name": "...", "json_body": "..."}'
```

### Using Baggage Header

Determine the current LDAP username with `echo $USER`, then use it in the Baggage header:

```bash
sq curl -H "Baggage: envoy-route--<app>=playpen-$(echo $USER)" \
  -L --post302 'https://<app>.stage.sqprod.co/_admin/rpc/call' ...
```

### Direct Playpen URL

Use the URL shown after `sq playpen sync`:

```bash
sq curl 'https://<app>-<deployment>-playpen-<ldap>--<app>.stage.sqprod.co/_admin/rpc/call' ...
```

---

## Testing with Feature Flag Overrides

Some Java gRPC services support `testing_only_flag_overrides` to override LaunchDarkly flags per-request. This is a per-service pattern — to enable it in a Java gRPC service:

1. Define a `FlagOverride` proto message with `name` (string) and `value` (string) fields
2. Add `repeated FlagOverride testing_only_flag_overrides` to your RPC request messages
3. In your feature flag evaluation logic, check for overrides before calling LaunchDarkly

See the `abacus` service for a working example (`flag_overrides.proto`, `AbacusFeatureFlags.java`).

```json
{
  "service_name": "...",
  "method_name": "...",
  "json_body": "...",
  "testing_only_flag_overrides": [
    {"name": "my-feature-flag", "value": "true"}
  ]
}
```

**IMPORTANT**: Field must be at request level, NOT inside `json_body`.

**Alternative**: Use the `launchdarkly` skill to add a testing merchant to the flag, then use that merchant as the session context. This avoids needing `testing_only_flag_overrides` entirely.

### Workflow

1. Add flag to code, sync playpen: `sq playpen sync`
2. Make RPC call with `testing_only_flag_overrides` (or use the LaunchDarkly alternative above)
3. Check logs, iterate

---

## Checking Playpen Logs

Query playpen logs by filtering on the hostname. Use `--staging` since playpens run in staging:

```bash
sq presidio query --staging --from=-5m --size=50 \
  -- "application:<app> hostname:*playpen-<ldap>*"
```

For full Presidio query syntax, see the `presidio-logs` skill.

---

## Enabling Async Tasks

By default, async tasks (cron jobs, background jobs) are disabled on playpen pods. To enable them:

```bash
sq playpen sync --allow-async-tasks
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `no playpen app specified` | Run from app directory or use `-a <app>` |
| `Application 'X' not found in registry` | App not configured for playpen - see [config docs](https://dev-guides.sqprod.co/docs/tools/playpen/reference/configuration) |
| `VPN not connected` | Connect to VPN first |
| `No playpens found` | No active playpens - run `sq playpen sync` to create one |
| Feature flag not working | Verify field is `testing_only_flag_overrides` at request level, resync playpen |
| Playpen has old code | Run `sq playpen sync` after making changes |
| UNAUTHENTICATED errors | Downstream service requires auth - test with different API or enable flag in LaunchDarkly |

---

## Documentation

- [Playpen docs](https://go/playpen)
- [Configuration reference](https://dev-guides.sqprod.co/docs/tools/playpen/reference/configuration)
- Slack: #playpen or #dx-backend-build
