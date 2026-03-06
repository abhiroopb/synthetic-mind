---
Skill name: internal-docs
Skill description: Searches and retrieves developer documentation from an internal documentation site. Use to search for documentation or fetch readable markdown content from internal documentation URLs.
roles: [admins, infra, dx, mobile, backend, frontend]
---

# Internal Documentation Reader

When you encounter a URL hosted on your internal documentation site, you can retrieve the markdown content of that page for easier reading and context.

## Usage

### Search for documentation

```bash
docs-cli search <query>
```

Options:
- `-l, --limit <n>` - Limit number of results (default 10)
- `-i, --index <name>` - Search only in a specific index
- `-j, --json` - Output results as JSON

### Fetch a specific page

To retrieve the markdown content of an internal docs URL, append `.md` to the path and fetch it:

```bash
curl -fsSL "https://<internal-docs-url>/docs/path/to/page.md"
```

### Example search

```bash
docs-cli search "acceptance tests"
```

This returns matching documentation with URLs that can be fetched directly.

### Other commands

- `docs-cli sync` - Update indexes from the manifest
- `docs-cli list` - List all documents in the indexes
- `docs-cli info` - Show configuration and index information
- `docs-cli stats` - Show index statistics
