# Datadog

> Query Datadog for logs, metrics, traces, monitors, RUM, and CI visibility directly from your agent.

## What it does

This skill lets you query Datadog observability data via direct API calls — no API keys, no MCP, no extra dependencies. It covers logs, metrics, APM traces, monitors, dashboards, RUM events, and CI pipeline visibility. Before querying, it consults an internal telemetry knowledge base for service-specific context.

## Usage

Invoke when you need observability data, are investigating production issues, checking service health, analyzing frontend performance, or debugging CI/CD pipelines. The skill provides domain-specific reference files for each Datadog capability (logs, metrics, monitors, APM, RUM, CI, etc.).

## Examples

- "Search Datadog logs for errors in the checkout service over the last hour"
- "Show me RUM page load percentiles for the dashboard app this week"
- "Check if there are any triggered monitors for the payments service"

## Why it was created

Querying Datadog typically requires navigating a complex UI or managing API keys. This skill eliminates that friction by routing through an authenticated proxy, letting you investigate production issues and analyze telemetry without leaving your terminal.
