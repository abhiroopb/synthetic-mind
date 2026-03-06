# Playpen

> Deploy and debug applications using ephemeral staging environments in Kubernetes.

## What it does

Playpen creates ephemeral development pods in a Kubernetes staging environment for testing code changes. You can sync local code to a staging pod, stream logs, execute commands, take heap and stack dumps, run CPU profilers, and route RPC calls to your specific pod. It also supports feature flag overrides per-request, making it easy to test flagged features in isolation.

## Usage

Use this skill when you need to deploy, test, or debug code in a staging environment. Requires VPN and the staging CLI tool.

**Trigger phrases:**
- "Sync my code to a staging pod"
- "Show me the staging logs"
- "Deploy this to a playpen"
- "Profile the service in staging"
- "Route RPC calls to my staging pod"
- "Spin down my staging pods"

## Examples

- `"Sync my changes and show logs"` — Syncs local code to a staging pod, restarts the service, and streams logs.
- `"Take a heap dump of the dashboard service"` — Connects to the staging pod and downloads a heap dump for analysis.
- `"Test with my-feature-flag set to true"` — Makes an RPC call to the staging pod with a feature flag override.

## Why it was created

Testing code changes in a realistic staging environment requires multiple manual steps — deploying, tailing logs, debugging, and cleaning up. Playpen wraps the entire workflow into simple commands, making it fast to iterate on changes in a production-like environment.
