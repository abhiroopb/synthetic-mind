# Registry API

> Query a service registry API using a Python client library for full access to applications, users, groups, roles, and infrastructure.

## What it does

Registry API provides direct access to all v2 endpoints of a service registry through a Python client library. You can look up applications by name or ID, search users, list group memberships, inspect roles, query infrastructure (AWS accounts, zones, ports), and trace dependency relationships between services. Scripts run via `uv run` with automatic dependency management.

## Usage

Invoke when you need detailed service registry data — application metadata, ownership, user lookups, group memberships, dependency graphs, or infrastructure information. This skill provides more endpoints and flexibility than the simpler CLI-based `registry-info` skill.

**Trigger phrases:**
- "Look up this application in the registry"
- "Who owns this service?"
- "Find all dependencies of this app"
- "Search for a user by email"

## Examples

- `"Find all applications owned by the checkout team"`
- `"List the dependencies of the payments service"`
- `"Look up user groups for jdoe"`

## Why it was created

The service registry holds critical metadata about applications, ownership, and infrastructure, but navigating it manually is tedious. This skill provides programmatic access to the full API surface, enabling quick lookups and cross-referencing that would take many clicks in the UI.
