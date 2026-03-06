# Codesearch

> Search across all repositories in your organization via Sourcegraph.

## What it does

Searches your organization's entire codebase through a Sourcegraph instance. Supports scoping by repo, file path, language, and symbol definitions. Includes boolean operators, regex patterns, case-sensitive search, branch filtering, and diff/commit search. When run inside a git repo, it auto-scopes to that repo unless you specify an explicit `repo:` filter.

## Usage

Use when you need to find code implementations, locate usages, discover where something is defined, or explore unfamiliar codebases across the organization.

Trigger phrases:
- "Search code for..."
- "Find where this function is defined"
- "Find all usages of this API"
- "Search across all repos for..."

## Examples

- "Find where `processPayment` is defined in Java"
- "Search for all usages of the `/api/v2/payments` endpoint"
- "Find YAML config files containing `database_url` across all repos"

## Why it was created

Finding code across a large multi-repo codebase requires powerful cross-repo search. This skill wraps Sourcegraph's query syntax into an accessible interface for quick lookups without leaving the terminal.
