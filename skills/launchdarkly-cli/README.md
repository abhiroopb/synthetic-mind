# LaunchDarkly CLI

> Manage feature flags, experiments, environments, and local dev-server using the `ldcli` command line tool.

## What it does

This skill wraps the LaunchDarkly CLI (`ldcli`) to manage feature flags end-to-end. You can create, list, update, and delete flags, run experiments, retrieve SDK credentials for different environments, and spin up a local dev-server for testing flag values without connecting to LaunchDarkly. It supports all LaunchDarkly API resources.

## Usage

Use this skill whenever you need to interact with LaunchDarkly resources from the command line. Requires `ldcli` to be installed and authenticated.

**Trigger phrases:**
- "Create a feature flag called my-new-flag"
- "List all flags in the project"
- "Toggle flag X in production"
- "Start the LaunchDarkly dev-server"
- "Get the SDK key for the staging environment"

## Examples

- `"List all feature flags in my project"` — Runs `ldcli flags list` to show all flags.
- `"Start the dev-server with my-flag set to true"` — Starts a local dev-server with flag overrides for testing.
- `"Create an experiment for the checkout flow"` — Creates a new experiment in the specified environment with the given parameters.

## Why it was created

Managing feature flags through a web UI is slow when you're iterating quickly. This skill brings full LaunchDarkly management to the command line, enabling fast flag operations, local testing, and scripted workflows.
