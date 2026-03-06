---
Skill name: codesearch
Skill description: Searches your organization's Sourcegraph code search instance across all repositories. Use when asked to search code, find implementations, locate usages, or explore codebases across the organization.
---

# Codesearch

Search your organization's codebase via Sourcegraph at your internal Sourcegraph instance.

## Available Tool

- **search_code(query, n=10, json_output=False, output_to_disk=False)** — Run a Sourcegraph code search.
  - `query`: Sourcegraph search query string (see syntax below)
  - `n`: Max results to return (default 10, max 20000)
  - `json_output`: Return structured JSON instead of text
  - `output_to_disk`: Write results to a temp file (use with `get_json_schema` for large result sets)

> **Note:** When run inside a git repo, the tool auto-prefixes queries with `repo:<current_repo>`. To search across all repos, use an explicit `repo:` filter or run outside a git directory.

## Query Syntax

### Scope Filters

| Filter | Example | Description |
|--------|---------|-------------|
| `repo:` | `repo:myorg/web` | Scope to a specific repo |
| `file:` | `file:\.py$` | Filter by file path (regex) |
| `lang:` | `lang:java` | Filter by language |
| `sym:` | `sym:MyClassName` | Search symbol definitions |

### Boolean & Pattern Operators

| Operator | Example | Description |
|----------|---------|-------------|
| (default) | `foo bar` | AND — both terms must match |
| `or` | `foo or bar` | OR — either term matches |
| `-` | `-test` | Negation — exclude matches |
| `/regex/` | `/func\s+\w+/` | Regex pattern search |
| `case:yes` | `case:yes MyFunc` | Case-sensitive search |

### Additional Filters

| Filter | Example | Description |
|--------|---------|-------------|
| `branch:` | `branch:main` | Search a specific branch |
| `type:` | `type:diff` | Search diffs, commits, symbols, etc. |
| `select:` | `select:repo` | Return only repo names matching |
| `count:` | `count:all` | Return all results |

## Workflows

### Find where a function is defined
```
sym:processPayment lang:java
```

### Find all usages of an API endpoint
```
/\/api\/v2\/payments/ lang:go
```

### Search across specific repos
```
repo:myorg/web repo:myorg/api someFunction
```

### Find config files with a specific key
```
file:\.yaml$ database_url
```

### Find implementations excluding tests
```
implements PaymentProcessor -file:test -file:spec lang:java
```

### Large-scale search
For queries returning many results, use `n=` to increase the limit and `output_to_disk=True` to write results to a file:
```
search_code(query="repo:myorg/web TODO", n=500, output_to_disk=True)
```

## Tips

- Combine multiple `repo:` filters to search across a set of repos
- Use `file:` with regex to target specific directories: `file:^src/main/`
- Use `select:repo` to discover which repos contain matches without seeing code
- Use `-file:vendor -file:node_modules` to exclude vendored code
- Wrap multi-word literal strings in quotes within the query
