# Registry Info

> Query application metadata from a service registry using a simple CLI for service information, dependencies, and operational details.

## What it does

Registry Info provides quick access to service registry data through a CLI tool. You can describe applications, check deployment status, understand dependency relationships, find contact information for owning teams, get links to operational resources (dashboards, runbooks, on-call schedules), and extract specific metadata fields. It's the simpler, faster alternative to the full `registry-api` skill.

## Usage

Invoke when you need to quickly look up service information, find who owns an app, check deployment endpoints, or get operational links like dashboards and runbooks.

**Trigger phrases:**
- "Describe this service"
- "What are the dependencies of this app?"
- "Find the Slack channel for this service"
- "Who owns this application?"

## Examples

- `"Describe the payments-service in the registry"`
- `"What services depend on the checkout-api?"`
- `"Get the runbook and dashboard links for my-service"`

## Why it was created

Developers frequently need to look up service metadata — ownership, dependencies, deployment info, monitoring links — but switching to the registry UI breaks flow. This skill puts that information one command away, directly in your terminal.
