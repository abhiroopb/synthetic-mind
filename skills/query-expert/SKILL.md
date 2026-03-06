---
name: query-expert
description: Discover tables, search historical queries, and execute SQL on Snowflake using Databricks vector search and Okta SSO authentication.
metadata:
  author: pazar, pweir, jbattles
  version: "0.1.0"
  status: experimental
---

# Query Expert Skill

Discover data tables, find expert query patterns, and execute SQL against Block's Snowflake environment. Powered by Databricks vector search over historical query patterns from Square, Cash App, Afterpay, and other Block organizations.

## Prerequisites

### First-Time Setup

Set your Square email (required for Snowflake). Databricks uses browser SSO or a PAT token:

```bash
export SNOWFLAKE_USER="your_email@squareup.com"
```

Test both connections:

```bash
# Test Snowflake (opens Okta SSO browser)
cd {{SKILL_DIR}}/scripts && uv run query-expert-cli.py execute --sql "SELECT CURRENT_USER() as user, CURRENT_ROLE() as role"

# Test Databricks vector search
cd {{SKILL_DIR}}/scripts && uv run query-expert-cli.py search --text "test query"
```

**Add to your shell profile** (`~/.zshrc` or `~/.bashrc`) to persist across sessions:
```bash
export SNOWFLAKE_USER="your_email@squareup.com"
# Optional: Databricks PAT token (falls back to browser SSO if not set)
# export QUERY_EXPERT_DATABRICKS_TOKEN="dapi..."
```

---

## Quick Reference

All commands output JSON. Run from `{{SKILL_DIR}}/scripts`:

```bash
cd {{SKILL_DIR}}/scripts && uv run query-expert-cli.py <command> [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `search` | Semantic search of historical queries from Block's query store |
| `tables` | Discover table metadata (structure, owners, users, verification) |
| `execute` | Execute SQL query on Snowflake |
| `permissions` | Check table access and get Registry URLs for requesting access |
| `knowledge` | Browse or load brand/domain-specific knowledge files |
| `metrics` | Search the Block Metric Store |

---

## Commands in Detail

### search — Find Similar Queries

Search historical queries semantically to find expert patterns, JOIN logic, and working examples.

```bash
uv run query-expert-cli.py search --text "revenue by merchant last month"
uv run query-expert-cli.py search --text "GPV by seller" --user-name PAZAR --limit 10
uv run query-expert-cli.py search --text "payment volume" --table-names "APP_BI.HEXAGON.VFACT_GPV_PROCESSING,APP_BI.HEXAGON.VDIM_MERCHANT"
uv run query-expert-cli.py search --text "subscription states" --query-source "Looker"
```

| Flag | Description |
|------|-------------|
| `--text` | **(required)** Question or query to search for |
| `--user-name` | Filter by LDAP username (e.g., `PAZAR`) |
| `--table-names` | Comma-delimited table names to validate JOIN patterns |
| `--query-source` | Filter: `Looker`, `Mode`, `Query Expert: Top User`, `Query Expert: Labeled` |
| `--limit` | Max results (default: 5) |

**Results include:** `query_text`, `query_description`, `user_name`, `tables_in_query`, `query_source`, extracted `source_tables` and `join_tables`.

### tables — Discover Table Metadata

Semantic search over Block's table catalog. Returns descriptions, column schemas, owners, verification status, and commonly joined tables.

```bash
uv run query-expert-cli.py tables --text "payment transactions" --brand "Square"
uv run query-expert-cli.py tables --text "timecards" --table-name "APP_PAYROLL.APP_PAYROLL.TIMECARDS"
uv run query-expert-cli.py tables --text "merchant activity" --verification-status "VERIFIED" --table-type "Analytics"
uv run query-expert-cli.py tables --text "employee data" --table-owner PAZAR
```

| Flag | Description |
|------|-------------|
| `--text` | **(required)** Semantic search query |
| `--table-name` | Exact table name (`DATABASE.SCHEMA.TABLE`) |
| `--brand` | `Square`, `Cash App`, `Afterpay`, `Tidal`, `Bitkey`, `Block` |
| `--table-type` | `Analytics`, `Production`, `Event` |
| `--verification-status` | `VERIFIED`, `UNVERIFIED`, or both (default: both) |
| `--table-owner` | Filter by owner LDAP |
| `--domain` | Data domain filter |
| `--sub-domain` | Sub-domain filter |
| `--table-database` | Filter by database name |
| `--table-schema` | Filter by schema (`DATABASE.SCHEMA`) |
| `--limit` | Max results (default: 5) |

**Results include:** `table_name`, `table_description`, `column_schema`, `table_verification_status`, `brand`, `table_type`, `table_owners`, `top_table_users`, `top_tables_joined`, `total_users_recent`.

### execute — Run SQL on Snowflake

Execute SQL queries directly on Snowflake with Okta SSO authentication.

```bash
uv run query-expert-cli.py execute --sql "SELECT CURRENT_USER() as user, CURRENT_ROLE() as role"
uv run query-expert-cli.py execute --sql "SELECT * FROM APP_BI.HEXAGON.VDIM_MERCHANT LIMIT 10"
uv run query-expert-cli.py execute --sql "SELECT COUNT(*) FROM MY_TABLE" --database ANALYTICS --schema PUBLIC --limit 100
uv run query-expert-cli.py execute --sql "SELECT * FROM MY_TABLE" --warehouse ADHOC__LARGE --role ANALYST
```

| Flag | Description |
|------|-------------|
| `--sql` | **(required)** SQL query to execute |
| `--database` | Database override |
| `--schema` | Schema override |
| `--warehouse` | Warehouse override (default: `ADHOC__LARGE`) |
| `--role` | Role override (default: `ANALYST`) |
| `--limit` | Append LIMIT clause if not already present |

**Results include:** `rows`, `row_count`, `snowflake_query_link`.

### permissions — Check Table Access

Check access to tables and get Registry URLs for requesting access to databases you don't have.

```bash
uv run query-expert-cli.py permissions --tables ANALYTICS.PUBLIC.TABLE1 APP_BI.HEXAGON.VDIM_MERCHANT
```

| Flag | Description |
|------|-------------|
| `--tables` | **(required)** One or more tables in `DATABASE.SCHEMA.TABLE` format |
| `--role` | Role override |

**Results include:** `accessible_tables`, `inaccessible_tables` (with `access_url` for Registry).

### knowledge — Browse Brand/Domain Knowledge

Explore or load brand-specific (Square, Cash App, Afterpay) and domain-specific (product, financial) knowledge files including context, glossaries, and demographics.

```bash
# List all available knowledge
uv run query-expert-cli.py knowledge

# Load Square brand context and glossary
uv run query-expert-cli.py knowledge --brand square --files "context.txt,glossary.json"

# Load all Cash App brand files
uv run query-expert-cli.py knowledge --brand cash_app

# Load domain knowledge
uv run query-expert-cli.py knowledge --domain product --subdomain hardware --files "workflow.txt"

# Load scope area files
uv run query-expert-cli.py knowledge --domain product --subdomain services --scope-area staff --files "employees.txt"
```

| Flag | Description |
|------|-------------|
| `--brand` | Brand: `square`, `cash_app`, `afterpay` |
| `--domain` | Domain: `product`, `financial` |
| `--subdomain` | Subdomain within domain |
| `--scope-area` | Scope area within subdomain |
| `--files` | Comma-delimited filenames to load (default: all files) |
| `--knowledge-dir` | Override knowledge directory path |

### metrics — Search Block Metric Store

Search for standardized metrics across Block.

```bash
uv run query-expert-cli.py metrics --text "total GPV" --brand "Square"
uv run query-expert-cli.py metrics --text "active sellers" --domains "payments"
uv run query-expert-cli.py metrics --text "revenue" --metric-name "total_net_revenue"
```

| Flag | Description |
|------|-------------|
| `--text` | **(required)** Search query |
| `--brand` | Brand filter |
| `--domains` | Metric domain filter |
| `--metric-name` | Specific metric name for exact lookup |
| `--cut-off` | Similarity threshold (default: 0.5, lower = broader) |

---

## Recommended Workflow

When helping a user write a SQL query, follow this process:

1. **Understand the question** — identify the brand (Square, Cash App, Afterpay), data needs, and time range
2. **Load knowledge** — run `knowledge` with no args to see what's available, then load relevant brand context/glossary
3. **Find tables** — use `tables` to discover relevant tables, prioritize VERIFIED + Analytics types
4. **Find expert queries** — use `search` with relevant terms and table names to find working examples
5. **Identify experts** — note `user_name` from search results and re-search with `--user-name` to see their patterns
6. **Validate JOINs** — use `search --table-names TABLE1,TABLE2` to find JOIN examples
7. **Check permissions** — use `permissions` before executing to verify access
8. **Execute** — use `execute` to run the final query

---

## Authentication

### Snowflake

Uses Okta SSO via `externalbrowser` authenticator. A browser window opens on first use; tokens are cached in your system keychain.

### Databricks

Uses one of:
- `QUERY_EXPERT_DATABRICKS_TOKEN` environment variable (PAT token)
- Browser SSO fallback (opens browser for authentication)

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SNOWFLAKE_USER` | `$USER@squareup.com` | Snowflake username |
| `SNOWFLAKE_ACCOUNT` | `squareinc-square` | Snowflake account |
| `SNOWFLAKE_WAREHOUSE` | `ADHOC__LARGE` | Default warehouse |
| `SNOWFLAKE_DATABASE` | `ANALYTICS` | Default database |
| `SNOWFLAKE_SCHEMA` | `PUBLIC` | Default schema |
| `SNOWFLAKE_ROLE` | `ANALYST` | Default role |
| `QUERY_EXPERT_DATABRICKS_TOKEN` | *(none)* | Databricks PAT (falls back to browser SSO) |
| `DATABRICKS_HOST` | `https://block-lakehouse-production.cloud.databricks.com` | Databricks workspace URL |
| `QUERY_EXPERT_KNOWLEDGE_DIR` | Auto-detected | Path to knowledge directory |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `SNOWFLAKE_USER not set` | `export SNOWFLAKE_USER="your_email@squareup.com"` |
| Snowflake auth expired | Re-run any `execute` command to trigger new Okta login |
| Databricks auth fails | Set `QUERY_EXPERT_DATABRICKS_TOKEN` or check browser SSO |
| `No matching queries found` | Broaden search terms, increase `--limit`, remove filters |
| `No matching tables found` | Try `--verification-status "VERIFIED, UNVERIFIED"`, broaden search |
| Table access denied | Use `permissions` command to get Registry URL for access request |
| Browser doesn't open | Set `BROWSER` env var to your browser path |
| Dependencies missing | Script uses `uv run` which auto-installs dependencies |

### Force Re-authentication

```bash
# Snowflake: clear token cache
rm -rf ~/.snowflake/token_cache*
rm -rf ~/.cache/snowflake/*

# Then re-run any command to trigger fresh login
cd {{SKILL_DIR}}/scripts && uv run query-expert-cli.py execute --sql "SELECT CURRENT_USER()"
```

---

## Notes

- All commands output JSON for easy parsing
- Snowflake uses Okta SSO via `externalbrowser` (no passwords stored)
- Databricks vector search indexes are hosted on Block's production Databricks workspace
- Knowledge files are bundled with the skill for offline access
- Query results include `snowflake_query_link` for viewing in the Snowflake UI
- Table results are ranked by verification status (VERIFIED first) and recent user activity
