---
name: dev-guides
description: Searches and retrieves developer documentation from dev-guides.sqprod.co. Use to search for documentation or fetch readable markdown content from URLs on the https://dev-guides.sqprod.co/ domain.
roles: [admins, ecom-infra, dse-dx, mlt-team, fs-dev-tools, observability-eng, mobile, backend-build, cash-ios, frontend, blox]
---

# Dev-Guides Documentation Reader

When you encounter a URL hosted on `https://dev-guides.sqprod.co/`, you can retrieve the markdown content of that page for easier reading and context.

## Usage

### Search for documentation

```bash
sq guide search <query>
```

Options:
- `-l, --limit <n>` - Limit number of results (default 10)
- `-i, --index <name>` - Search only in a specific index
- `-j, --json` - Output results as JSON

### Fetch a specific page

To retrieve the markdown content of a dev-guides URL, append `.md` to the path and fetch it:

```bash
curl -fsSL "https://dev-guides.sqprod.co/square/docs/develop/web/square-web-monorepo/guides/end-to-end-testing/set-up-acceptance-tests.md"
```

### Example search

```bash
sq guide search "acceptance tests"
```

This returns matching documentation with URLs that can be fetched directly.

### Other commands

- `sq guide sync` - Update indexes from the manifest
- `sq guide list` - List all documents in the indexes
- `sq guide info` - Show configuration and index information
- `sq guide stats` - Show index statistics
