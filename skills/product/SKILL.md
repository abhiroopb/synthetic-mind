---
name: product
description: Searches and reads from the product documentation repository. Use when searching existing product requirements, end-to-end feature architecture, or browsing product documentation.
---

# Product Repository Search

Search and read product requirements, end-to-end feature architecture, and other documentation from the product documentation repository.

## Prerequisites

- `gh` CLI (GitHub CLI) authenticated with access to the product repo

## CLI Tool

This skill includes a CLI tool at `{{SKILL_DIR}}/scripts/product-search`.

Run it through Python so it works even if executable bits are missing after install:

```bash
python3 {{SKILL_DIR}}/scripts/product-search <command> [options]
```

## Commands

### Search for documents

Search for files matching a query. Defaults to markdown files.

```bash
python3 {{SKILL_DIR}}/scripts/product-search search "payments architecture"
```

Options:
- `--all-files` — search all file types, not just markdown
- `--limit N` — max results to return (default: 10)
- `--json` — output results as JSON

### Read a file

Read a specific file from the repository.

```bash
python3 {{SKILL_DIR}}/scripts/product-search read docs/payments/architecture.md
```

Options:
- `--max-lines N` — truncate output after N lines (default: 200, use 0 for unlimited)
- `--ref REF` — git ref to read from (default: main)

### Browse the directory tree

List the directory structure to discover what documents exist.

```bash
python3 {{SKILL_DIR}}/scripts/product-search tree
python3 {{SKILL_DIR}}/scripts/product-search tree docs/payments
```

Options:
- `--depth N` — max directory depth to show (default: 3)
- `--md-only` — show only markdown files

## Workflow

1. Use `tree` to discover the directory structure
2. Use `search` to find documents matching a topic
3. Use `read` to fetch the full content of a specific document
