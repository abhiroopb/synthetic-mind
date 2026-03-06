---
name: playpen
description: "Deploy and debug applications using an ephemeral staging environment service. Use when user needs to sync code to a staging pod, view logs, debug running services, manage instances, make RPC calls, or test with feature flag overrides."
metadata:
  version: "0.2.0"
  status: experimental
---

# Staging Environment Deployer

Deploy and debug applications using CLI commands that create ephemeral development environments in Kubernetes for testing code changes.

## Prerequisites

- VPN connected
- CLI tool installed
- Application must be registered in the staging service (check with `cli staging list -a <app>`)

**Note**: Staging pods run in the staging environment and can modify staging data. Use with caution.

---

## Commands Overview

| Command | Description |
|---------|-------------|
| `cli staging sync` | Sync local changes to a staging pod and restart the service |
| `cli staging attach` | Attach to an existing staging pod without re-syncing |
| `cli staging exec` | Execute a command in a staging pod |
| `cli staging logs` | Stream logs from a staging pod |
| `cli staging list` | List any staging pod instances for an application |
| `cli staging down` | Spin down all staging pods owned by user |
| `cli staging heap-dump` | Dump heap and transfer to local machine |
| `cli staging stack-dump` | Dump stack and display in terminal |
| `cli staging profile` | Run async-profiler and download flamegraph |

---

## Specifying an Application

Most commands auto-detect the app from your current directory. If detection fails, use `-a <app>`:

```bash
cli staging list -a dashboard
cli staging sync -a my-service
cli staging logs -a my-service
```

---

## List Staging Pods

```bash
cli staging list
cli staging list -a dashboard
```

---

## Sync Command

Sync local changes to a staging pod and restart the service:

```bash
cli staging sync
cli staging sync -a my-service
cli staging sync -a my-service --deployment my-service-jobs
cli staging sync --no-attach
```

---

## Attach Command

```bash
cli staging attach
cli staging attach -a my-service
```

---

## Logs

```bash
cli staging logs
cli staging logs -a my-service
```

---

## Execute Commands

```bash
cli staging exec <command>
cli staging exec -a my-service <command>
```

---

## Spin Down

```bash
cli staging down
```

---

## Debugging Commands

### Heap Dump

```bash
cli staging heap-dump
cli staging heap-dump -a my-service
```

### Stack Dump

```bash
cli staging stack-dump
cli staging stack-dump -a my-service
```

### Profiling

```bash
cli staging profile
cli staging profile -a my-service
```

---

## Common Workflows

### Deploy and Test Changes

```bash
cli staging sync
cli staging logs
# Test your changes
cli staging down
```

### Debug Performance Issues

```bash
cli staging attach
cli staging profile
```

### Investigate Memory Issues

```bash
cli staging sync
cli staging heap-dump
```

---

## Routing RPC Calls to Staging Pods

Route requests to your staging pod instead of production pods.

### Using --staging-pod Flag (Recommended)

```bash
curl --staging-pod <app> -L --post302 'https://<app>.staging.example.com/_admin/rpc/call' \
  -H 'content-type: application/json' \
  --data-raw '{"service_name": "...", "method_name": "...", "json_body": "..."}'
```

### Using Baggage Header

```bash
curl -H "Baggage: envoy-route--<app>=staging-pod-$(echo $USER)" \
  -L --post302 'https://<app>.staging.example.com/_admin/rpc/call' ...
```

---

## Testing with Feature Flag Overrides

Some services support `testing_only_flag_overrides` to override LaunchDarkly flags per-request:

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

**Alternative**: Use the `launchdarkly` skill to add a testing account to the flag, then use that account as the session context.

---

## Checking Staging Pod Logs

```bash
cli logs query --staging --from=-5m --size=50 \
  -- "application:<app> hostname:*staging-pod-<username>*"
```

---

## Enabling Async Tasks

```bash
cli staging sync --allow-async-tasks
```

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| `no app specified` | Run from app directory or use `-a <app>` |
| `Application 'X' not found in registry` | App not configured for staging pods — check config docs |
| `VPN not connected` | Connect to VPN first |
| `No instances found` | No active pods — run `cli staging sync` to create one |
| Feature flag not working | Verify field is `testing_only_flag_overrides` at request level, resync |
| Instance has old code | Run `cli staging sync` after making changes |

---

## Documentation

- Slack: #staging-environments or #dx-backend-build
