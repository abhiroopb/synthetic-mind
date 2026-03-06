---
name: launchdarkly-cli
description: "Manages LaunchDarkly feature flags, experiments, environments, and local dev-server using the ldcli CLI. Use when asked to create, list, toggle, or manage feature flags, run the LaunchDarkly dev-server, or interact with LaunchDarkly resources."
---

# LaunchDarkly CLI

Interact with LaunchDarkly feature flags, experiments, environments, and other resources using the `ldcli` command line tool.

## Prerequisites

- `ldcli` must be installed (`brew install ldcli` or `npm install -g @launchdarkly/ldcli`)
- Authentication must be configured (run `ldcli login` or set `LD_ACCESS_TOKEN` env var)

## Configuration

ldcli stores config at `$XDG_CONFIG_HOME/ldcli/config.yml`. Set defaults to avoid passing flags repeatedly:

```bash
ldcli config --set access-token <token>
ldcli config --set project <project-key>
ldcli config --set environment <environment-key>
ldcli config --set output json  # or plaintext
ldcli config --list
```

Environment variables use `LD_` prefix (e.g., `LD_ACCESS_TOKEN`, `LD_PROJECT`).

## Common Workflows

### Feature Flags

```bash
# List flags
ldcli flags list --project <project>

# Create a flag
ldcli flags create --project <project> -d '{"name": "My Flag", "key": "my-flag"}'

# Get flag details
ldcli flags get --project <project> --flag <flag-key>

# Update a flag
ldcli flags update --project <project> --flag <flag-key> -d '{"name": "Updated Name"}'

# Delete a flag
ldcli flags delete --project <project> --flag <flag-key>
```

### Experiments

```bash
# List experiments
ldcli experiments list --project <project> --environment <env>

# Create an experiment
ldcli experiments create --project <project> --environment <env> -d '{
  "name": "Checkout flow test",
  "key": "checkout-flow-test",
  "description": "Experiment comparing new and old checkout flow"
}'
```

### Environments

```bash
# Get environment details and SDK credentials
ldcli environments get --project <project> --environment <env>

# Get SDK key (server-side)
ldcli environments get --project <project> --environment <env> | jq '.apiKey'

# Get mobile key
ldcli environments get --project <project> --environment <env> | jq '.mobileKey'

# Get client-side ID
ldcli environments get --project <project> --environment <env> | jq '.id'
```

### Dev Server (Local Testing)

The dev-server lets you test flag values locally without connecting to LaunchDarkly.

```bash
# Start the dev-server (runs on http://localhost:8765)
ldcli dev-server start

# Add a project/environment to the dev-server
ldcli dev-server add-project --project <project> --source <environment>

# Sync flags from source environment
ldcli dev-server sync-project --project <project>

# Override a flag value locally
ldcli dev-server add-override --project <project> --flag <flag-key> --data <value-json>

# Remove a flag override
ldcli dev-server remove-override --project <project> --flag <flag-key>

# Start with sync, context, and overrides
ldcli dev-server start --project <project> --source <env> \
  --context '{"kind": "user", "key": "test-key"}' \
  --override '{"my-flag": true}'
```

Dev-server UI is available at `http://localhost:8765/ui/`.

### Sourcemaps

```bash
# Upload JavaScript sourcemaps for error monitoring
ldcli sourcemaps upload \
  --app-version <version> \
  --path <sourcemap-dir> \
  --base-path <deploy-dir> \
  --project <project>
```

## Output Format

- Default output is plaintext (human-readable)
- Use `--output json` for machine-readable JSON output
- Pipe through `jq` for formatted JSON: `ldcli <cmd> --output json | jq`

## Resource Commands

ldcli supports all LaunchDarkly API resources. Discover available resources and their commands:

```bash
ldcli --help                    # List all resources
ldcli <resource> --help         # List commands for a resource
ldcli <resource> <cmd> --help   # Detailed help for a command
```

Data can be provided inline with `-d '{...}'` or from a file with `-d "$(cat data.json)"`.

## Tips

- Always use `--output json` when you need to parse or process the response
- Set default project/environment with `ldcli config` to reduce repetitive flags
- The dev-server does NOT evaluate targeting rules — it returns the same value for all contexts
- Use `ldcli dev-server --help` for full dev-server command reference
