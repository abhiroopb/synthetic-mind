---
name: codesearch
description: Use when searching, finding, locating, discovering, querying, looking up, or browsing code patterns, files, or implementations across all company repositories via internal code search.
roles: [frontend, cash-ios, backend]
---

# Codesearch

Search code across all company repos using `sq codesearch`.

**STOP** — Before proceeding, verify `sq codesearch` is available by running `sq codesearch --help`. If not found, stop and tell the user to install the `sq` CLI.

## Usage

```bash
sq codesearch <query>
```

## Options

| Flag | Description |
|------|-------------|
| `-o, --output` | Output format: `id` (default), `url`, `repo`, `json` |
| `--sourcegraph` | Use Sourcegraph instead of internal code search. **Do not use unless the user explicitly asks for it.** |

## Query Syntax

Standard code search patterns work:

- `file:<pattern>` - Filter by filename (e.g., `file:.ruby-version`)
- Plain text searches across all file contents

## Examples

**Find files containing "nexus3":**
```bash
sq codesearch nexus3
```

**Find projects on a specific Ruby version:**
```bash
sq codesearch file:.ruby-version 2.7
```

**Get GitHub URLs for results:**
```bash
sq codesearch file:.ruby-version 2.7 -ourl
```

**Get list of repos only:**
```bash
sq codesearch file:.ruby-version 2.7 -orepo
```

**Get raw JSON response:**
```bash
sq codesearch file:.ruby-version 2.7 -ojson
```

**Use Sourcegraph backend:**
```bash
sq codesearch --sourcegraph "some query"
```

## Output Formats

- `id` (default): `repo:filepath` format
- `url`: Full GitHub blob URL
- `repo`: Just the repository name (deduplicated)
- `json`: Raw JSON from codesearch API

## Support

Ask in the developer experience channel
