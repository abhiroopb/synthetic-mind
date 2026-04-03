---
name: dev-guides
description: Use when looking up, searching, finding, reading, browsing, retrieving, querying, or checking internal developer documentation. Load this skill when someone wants to search for docs, look up a guide, find a tutorial, read a page, browse documentation, or retrieve markdown content from a documentation URL.
---

# Developer Documentation Reader

## Prerequisites

Before running any commands, verify the documentation CLI is available:

```bash
docs-cli --help
```

**STOP** if the CLI is not installed or not recognized. Direct the user to `SETUP.md` for installation instructions.

When you encounter a URL hosted on your internal developer documentation site, you can retrieve the markdown content of that page for easier reading and context.

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

```bash
docs-cli fetch https://your-docs-site.example.com/docs/path/to/page.md
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
