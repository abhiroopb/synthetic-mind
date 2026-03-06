---
name: snowflake
description: Query Snowflake data warehouse using SSO authentication. Run SQL queries, explore schemas, and analyze data.
metadata:
  author: anonymous
  version: "0.3.0"
  status: experimental
---

# Snowflake Skill

Query your company's Snowflake data warehouse with SSO authentication.

## Prerequisites

Requires the Snowflake CLI (`snow`). If a `snow` command fails because the CLI is not installed, read 
[SETUP.md](./SETUP.md) and walk the user through installation and configuration.

---

## Safety guardrails

Your SSO identity may have admin-level access to databases you own, so destructive
operations (DROP, TRUNCATE, DELETE, etc.) can succeed.

**Use a read-only role by default.** Derive the role name from the database:

```bash
snow sql --role {DATABASE}__SNOWFLAKE__READ_ONLY -q "SELECT ..."
```

For example:
```bash
snow sql --role YOUR_DB__SNOWFLAKE__READ_ONLY --format JSON -q "SELECT * FROM your_db.raw.my_table LIMIT 10"
```

Exceptions:
- Only omit `--role` when the query JOINs across multiple databases (to use the default role with broader access).
- Use ADMIN or READ_WRITE roles only when the user explicitly asks for write/DDL operations.

---

## Quick Reference

Generally prefer the `--format JSON` for agent-parseable output. 

```bash
snow sql --format JSON -q "SELECT ..."
```

### Choosing a connection

By default, commands connect to **production** with `ADHOC__MEDIUM`.
Use the `-c` flag to change the warehouse size or target **staging**:

| Flag | Environment | Warehouse | Use for |
|------|-------------|-----------|---------|
| `-c small` | Production | ADHOC__SMALL | Metadata queries, row counts, simple lookups |
| (default) | Production | ADHOC__MEDIUM | General use |
| `-c large` | Production | ADHOC__LARGE | Larger scans, joins across big tables |
| `-c xlarge` | Production | ADHOC__XLARGE | Heavy or long-running queries |
| `-c staging-medium` | Staging | ADHOC__MEDIUM | General staging queries |
| `-c staging-small` | Staging | ADHOC__SMALL | Light staging queries |
| `-c staging-large` | Staging | ADHOC__LARGE | Larger staging scans |
| `-c staging-xlarge` | Staging | ADHOC__XLARGE | Heavy staging queries |

```bash
# Query staging
snow sql -c staging-medium --format JSON -q "SELECT ..."
```

### Finding Tables

When a user provides a name but you don't know whether it's a database, schema, or table,
search across all three object types. Each command only searches its own type, so run all three:

```bash
snow sql -c small --format JSON -q "SHOW TERSE DATABASES LIKE '%NAME%' IN ACCOUNT"
snow sql -c small --format JSON -q "SHOW TERSE SCHEMAS LIKE '%NAME%' IN ACCOUNT"
snow sql -c small --format JSON -q "SHOW TERSE TABLES LIKE '%NAME%' IN ACCOUNT"
```

This returns matches across all databases visible to your role, avoiding the need to
iterate through each database's `INFORMATION_SCHEMA`.

### Common Operations

| Operation | Command |
|-----------|---------|
| Check context | `snow sql -q "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()"` |
| List databases | `snow sql -q "SHOW DATABASES"` |
| List schemas | `snow sql -q "SHOW SCHEMAS IN DATABASE <db>"` |
| List tables | `snow sql -q "SHOW TABLES IN SCHEMA <db>.<schema>"` |
| Describe table | `snow sql -q "DESCRIBE TABLE <db>.<schema>.<table>"` |

### Examples

```bash
# Check current context
snow sql -q "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()"

# List all databases
snow sql -q "SHOW DATABASES"
```

### Output Formatting

| Format | Flag | Best for |
|--------|------|----------|
| JSON | `--format JSON` | Default for agent use; structured/nested data |
| Table | (default) | User-facing results with few columns |
| CSV | `--format CSV` | Exporting data; piping to other tools |

Additional strategies:
- Select only the columns you need rather than `SELECT *`
- For exploration, start with `LIMIT 5` to check column names and data shape
- To discover columns: `snow sql -q "SELECT COLUMN_NAME FROM <db>.INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = '<schema>' AND TABLE_NAME = '<table>'"`
- Query results may be large; use `LIMIT` clauses and pipe large exports to a file: `snow sql --format CSV -q "SELECT ..." > /tmp/results.csv`

### Query Cost Awareness

Snowflake queries can scan very large datasets and produce enormous result sets. Before running
a query on an unfamiliar table, check its size and preview the shape of the data:

```bash
# Step 1: Check row count
snow sql -c small --format JSON -q "SELECT COUNT(*) as total FROM DATABASE_NAME.SCHEMA_NAME.TABLE_NAME WHERE <filters>"

# Step 2: Preview a few rows with specific columns
snow sql -c small --format JSON -q "SELECT col1, col2, col3 FROM DATABASE_NAME.SCHEMA_NAME.TABLE_NAME WHERE <filters> LIMIT 5"
```

For complex queries (multi-table joins, large scans), use `EXPLAIN` to check the execution plan
before running:

```bash
snow sql -c small --format JSON -q "EXPLAIN SELECT ... FROM ..."
```

Look at `partitionsAssigned` vs `partitionsTotal` in the EXPLAIN output to gauge how much data will be
scanned. If nearly all partitions are assigned, add filters to narrow the scan.

## Authentication

Authentication uses SSO via `externalbrowser`. A browser window opens automatically when authentication is
needed (first use or token expiry). If an active SSO session exists, it completes silently. Requires VPN.

Tokens are cached locally and remain valid for hours/days.

### Force Re-authentication

```bash
rm -rf ~/.snowflake/token_cache*
rm -rf ~/.cache/snowflake/*
```

## Common SQL Operations

### Explore Schema

```bash
# Show all tables in a schema
snow sql -q "SHOW TABLES IN SCHEMA DATABASE_NAME.SCHEMA_NAME"

# Show all views
snow sql -q "SHOW VIEWS IN SCHEMA DATABASE_NAME.SCHEMA_NAME"

# Get table row count
snow sql --format JSON -q "SELECT COUNT(*) as total FROM DATABASE_NAME.SCHEMA_NAME.TABLE_NAME"
```

## Table Docs

Reference documentation for specific Snowflake tables lives in `{{SKILL_DIR}}/table-docs/`.
Each file documents a table or group of related tables, including schema and column
references, business intent, enum values, and example queries.

Table docs are not listed here — the directory will grow to contain many detailed references
and loading them all would overwhelm the context window. Search for only the tables you need:

```bash
# List available table docs
ls {{SKILL_DIR}}/table-docs/

# Search for a table by name
grep -rl "TABLE_NAME" {{SKILL_DIR}}/table-docs/
```

## Troubleshooting

| Issue | Solution                                                                                              |
|-------|-------------------------------------------------------------------------------------------------------|
| `snow` not found | See [SETUP.md](./SETUP.md)                                                                            |
| `externalbrowser auth fails` | Ensure VPN is connected; try clearing browser cache                                                   |
| `Account not found` | Verify account in `~/.snowflake/config.toml` matches your Snowflake account identifier |
| `Warehouse does not exist` | Check warehouse name and role permissions                                                             |
| Browser doesn't open | Set `BROWSER` env var: `export BROWSER="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"` |
