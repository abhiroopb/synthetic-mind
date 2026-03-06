---
Skill name: query-expert
Skill description: Discover tables, search historical queries, and execute SQL on Snowflake using vector search and SSO authentication.
---

# Query Expert Skill

Discover data tables, find expert query patterns, and execute SQL against your company's Snowflake environment. Powered by vector search over historical query patterns from your company's brands and business units.

## Prerequisites

### First-Time Setup

Set your corporate email (required for Snowflake). The vector search engine uses browser SSO or a PAT token:

```bash
export SNOWFLAKE_USER="your_email@yourcompany.com"
```

Test both connections:

```bash
# Test Snowflake (opens SSO browser)
cd {{SKILL_DIR}}/scripts && uv run query-expert-cli.py execute --sql "SELECT CURRENT_USER() as user, CURRENT_ROLE() as role"

# Test vector search
cd {{SKILL_DIR}}/scripts && uv run query-expert-cli.py search --text "test query"
```

**Add to your shell profile** (`~/.zshrc` or `~/.bashrc`) to persist across sessions:
```bash
export SNOWFLAKE_USER="your_email@yourcompany.com"
# Optional: Vector search PAT token (falls back to browser SSO if not set)
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
| `search` | Semantic search of historical queries from your company's query store |
| `tables` | Discover table metadata (structure, owners, users, verification) |
| `execute` | Execute SQL query on Snowflake |
| `permissions` | Check table access and get URLs for requesting access |
| `knowledge` | Browse or load brand/domain-specific knowledge files |
| `metrics` | Search the company metric store |

---

## Commands in Detail

### search — Find Similar Queries

Search historical queries semantically to find expert patterns, JOIN logic, and working examples.

```bash
uv run query-expert-cli.py search --text "revenue by customer last month"
uv run query-expert-cli.py search --text "volume by customer" --user-name JDOE --limit 10
uv run query-expert-cli.py search --text "payment volume" --table-names "YOUR_SCHEMA.FACT_VOLUME,YOUR_SCHEMA.DIM_CUSTOMER"
uv run query-expert-cli.py search --text "subscription states" --query-source "Looker"
```

| Flag | Description |
|------|-------------|
| `--text` | **(required)** Question or query to search for |
| `--user-name` | Filter by username (e.g., `JDOE`) |
| `--table-names` | Comma-delimited table names to validate JOIN patterns |
| `--query-source` | Filter: `Looker`, `Mode`, `Query Expert: Top User`, `Query Expert: Labeled` |
| `--limit` | Max results (default: 5) |

**Results include:** `query_text`, `query_description`, `user_name`, `tables_in_query`, `query_source`, extracted `source_tables` and `join_tables`.

### tables — Discover Table Metadata

Semantic search over your company's table catalog. Returns descriptions, column schemas, owners, verification status, and commonly joined tables.

```bash
uv run query-expert-cli.py tables --text "payment transactions" --brand "brand_a"
uv run query-expert-cli.py tables --text "timecards" --table-name "YOUR_DB.YOUR_SCHEMA.TIMECARDS"
uv run query-expert-cli.py tables --text "customer activity" --verification-status "VERIFIED" --table-type "Analytics"
uv run query-expert-cli.py tables --text "employee data" --table-owner JDOE
```

| Flag | Description |
|------|-------------|
| `--text` | **(required)** Semantic search query |
| `--table-name` | Exact table name (`DATABASE.SCHEMA.TABLE`) |
| `--brand` | Brand filter (e.g., `brand_a`, `brand_b`, `brand_c`) |
| `--table-type` | `Analytics`, `Production`, `Event` |
| `--verification-status` | `VERIFIED`, `UNVERIFIED`, or both (default: both) |
| `--table-owner` | Filter by owner username |
| `--domain` | Data domain filter |
| `--sub-domain` | Sub-domain filter |
| `--table-database` | Filter by database name |
| `--table-schema` | Filter by schema (`DATABASE.SCHEMA`) |
| `--limit` | Max results (default: 5) |

**Results include:** `table_name`, `table_description`, `column_schema`, `table_verification_status`, `brand`, `table_type`, `table_owners`, `top_table_users`, `top_tables_joined`, `total_users_recent`.

### execute — Run SQL on Snowflake

Execute SQL queries directly on Snowflake with SSO authentication.

```bash
uv run query-expert-cli.py execute --sql "SELECT CURRENT_USER() as user, CURRENT_ROLE() as role"
uv run query-expert-cli.py execute --sql "SELECT * FROM YOUR_SCHEMA.DIM_CUSTOMER LIMIT 10"
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

Check access to tables and get URLs for requesting access to databases you don't have.

```bash
uv run query-expert-cli.py permissions --tables ANALYTICS.PUBLIC.TABLE1 YOUR_SCHEMA.DIM_CUSTOMER
```

| Flag | Description |
|------|-------------|
| `--tables` | **(required)** One or more tables in `DATABASE.SCHEMA.TABLE` format |
| `--role` | Role override |

**Results include:** `accessible_tables`, `inaccessible_tables` (with `access_url` for your access management system).

### knowledge — Browse Brand/Domain Knowledge

Explore or load brand-specific and domain-specific knowledge files including context, glossaries, and demographics.

```bash
# List all available knowledge
uv run query-expert-cli.py knowledge

# Load brand_a context and glossary
uv run query-expert-cli.py knowledge --brand brand_a --files "context.txt,glossary.json"

# Load all brand_b files
uv run query-expert-cli.py knowledge --brand brand_b

# Load domain knowledge
uv run query-expert-cli.py knowledge --domain product --subdomain hardware --files "workflow.txt"

# Load scope area files
uv run query-expert-cli.py knowledge --domain product --subdomain services --scope-area staff --files "employees.txt"
```

| Flag | Description |
|------|-------------|
| `--brand` | Brand: `brand_a`, `brand_b`, `brand_c` |
| `--domain` | Domain: `product`, `financial` |
| `--subdomain` | Subdomain within domain |
| `--scope-area` | Scope area within subdomain |
| `--files` | Comma-delimited filenames to load (default: all files) |
| `--knowledge-dir` | Override knowledge directory path |

### metrics — Search Company Metric Store

Search for standardized metrics across your company.

```bash
uv run query-expert-cli.py metrics --text "total volume" --brand "brand_a"
uv run query-expert-cli.py metrics --text "active customers" --domains "payments"
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

1. **Understand the question** — identify the brand/business unit, data needs, and time range
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

Uses SSO via `externalbrowser` authenticator. A browser window opens on first use; tokens are cached in your system keychain.

### Vector Search Engine

Uses one of:
- `QUERY_EXPERT_DATABRICKS_TOKEN` environment variable (PAT token)
- Browser SSO fallback (opens browser for authentication)

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SNOWFLAKE_USER` | `$USER@yourcompany.com` | Snowflake username |
| `SNOWFLAKE_ACCOUNT` | `YOUR_SNOWFLAKE_ACCOUNT` | Snowflake account |
| `SNOWFLAKE_WAREHOUSE` | `ADHOC__LARGE` | Default warehouse |
| `SNOWFLAKE_DATABASE` | `ANALYTICS` | Default database |
| `SNOWFLAKE_SCHEMA` | `PUBLIC` | Default schema |
| `SNOWFLAKE_ROLE` | `ANALYST` | Default role |
| `QUERY_EXPERT_DATABRICKS_TOKEN` | *(none)* | Vector search PAT (falls back to browser SSO) |
| `DATABRICKS_HOST` | `https://your-lakehouse.cloud.databricks.com` | Vector search workspace URL |
| `QUERY_EXPERT_KNOWLEDGE_DIR` | Auto-detected | Path to knowledge directory |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `SNOWFLAKE_USER not set` | `export SNOWFLAKE_USER="your_email@yourcompany.com"` |
| Snowflake auth expired | Re-run any `execute` command to trigger new SSO login |
| Vector search auth fails | Set `QUERY_EXPERT_DATABRICKS_TOKEN` or check browser SSO |
| `No matching queries found` | Broaden search terms, increase `--limit`, remove filters |
| `No matching tables found` | Try `--verification-status "VERIFIED, UNVERIFIED"`, broaden search |
| Table access denied | Use `permissions` command to get URL for access request |
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
- Snowflake uses SSO via `externalbrowser` (no passwords stored)
- Vector search indexes are hosted on your company's production workspace
- Knowledge files are bundled with the skill for offline access
- Query results include `snowflake_query_link` for viewing in the Snowflake UI
- Table results are ranked by verification status (VERIFIED first) and recent user activity
