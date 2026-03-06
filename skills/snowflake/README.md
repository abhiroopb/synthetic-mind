# Snowflake

> Query a Snowflake data warehouse using SSO authentication with safety guardrails and cost awareness.

## What it does

The Snowflake skill provides a workflow for querying a Snowflake data warehouse using the `snow` CLI with SSO authentication. It supports multiple warehouse sizes for different query workloads, enforces read-only roles by default to prevent accidental destructive operations, and includes cost-awareness guidance for checking table sizes before running expensive queries. It also includes bundled table documentation for quick reference.

## Usage

Invoke when you need to run SQL queries against Snowflake, explore database schemas, find tables, or analyze data. Authentication happens via SSO — a browser window opens automatically when needed.

**Trigger phrases:**
- "Query Snowflake"
- "Run this SQL"
- "Show me tables in this schema"
- "Explore the Snowflake warehouse"

## Examples

- `"Run this query on Snowflake: SELECT COUNT(*) FROM my_table"`
- `"List all tables in the analytics schema"`
- `"Find tables matching 'payments' across all databases"`

## Why it was created

Snowflake queries through the web UI or raw CLI lack safety guardrails and cost awareness. This skill enforces read-only defaults, provides warehouse sizing guidance, and includes table documentation — reducing the risk of expensive accidental queries and making data exploration faster.
