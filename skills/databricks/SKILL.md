---
name: databricks
description: Query Block's Databricks Lakehouse using SQL. Use when user needs to query Databricks, search tables/catalogs, or run SQL against Databricks data.
metadata:
  author: jom
  version: "0.1.0"
  status: experimental
---

# Block Data Skill

Query Block's Databricks Lakehouse using the Databricks CLI.

## Prerequisites

### Install Databricks CLI

```bash
brew tap databricks/tap
brew install databricks
```

### Authenticate (First Time)

```bash
databricks auth login --host https://block-lakehouse-production.cloud.databricks.com
```

This opens a browser for OAuth login. After authenticating, tokens are cached at `~/.databricks/token-cache.json`.

---

## Quick Reference

Set the host in your environment:

```bash
export DATABRICKS_HOST=https://block-lakehouse-production.cloud.databricks.com
```

Or pass it inline with each command.

---

## Running SQL Queries

Use the Statement Execution API to run SQL:

```bash
DATABRICKS_HOST=https://block-lakehouse-production.cloud.databricks.com \
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "a53b3ef899f7696a",
  "statement": "SELECT 1 as test",
  "wait_timeout": "30s"
}'
```

**Available warehouses:**

| ID | Name | Size | State |
|----|------|------|-------|
| `a53b3ef899f7696a` | Serverless Starter Warehouse | Large | RUNNING |
| `75121791727d1544` | LakeView 🏖 | Large | RUNNING |
| `cdd782621e37257a` | Anomalo | Large | RUNNING |

**Note:** `wait_timeout` must be between 5s and 50s. For long queries, use `0s` and poll for results.

---

## Common Queries

### List Catalogs

```bash
DATABRICKS_HOST=https://block-lakehouse-production.cloud.databricks.com \
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "a53b3ef899f7696a",
  "statement": "SHOW CATALOGS",
  "wait_timeout": "30s"
}' | jq -r '.result.data_array[][]'
```

### Search for Tables

```bash
DATABRICKS_HOST=https://block-lakehouse-production.cloud.databricks.com \
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "a53b3ef899f7696a",
  "statement": "SELECT table_catalog, table_schema, table_name FROM system.information_schema.tables WHERE lower(table_name) LIKE '\''%merchant%'\'' LIMIT 20",
  "wait_timeout": "50s"
}' | jq '.result.data_array'
```

### Describe a Table

```bash
DATABRICKS_HOST=https://block-lakehouse-production.cloud.databricks.com \
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "a53b3ef899f7696a",
  "statement": "DESCRIBE catalog.schema.table_name",
  "wait_timeout": "30s"
}' | jq '.result.data_array'
```

### Query with Results

```bash
DATABRICKS_HOST=https://block-lakehouse-production.cloud.databricks.com \
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "a53b3ef899f7696a",
  "statement": "SELECT * FROM catalog.schema.table LIMIT 10",
  "wait_timeout": "50s"
}' | jq '{columns: .manifest.schema.columns[].name, data: .result.data_array}'
```

---

## Other CLI Commands

### List Warehouses

```bash
DATABRICKS_HOST=https://block-lakehouse-production.cloud.databricks.com \
databricks warehouses list
```

### List Running Clusters

```bash
DATABRICKS_HOST=https://block-lakehouse-production.cloud.databricks.com \
databricks clusters list
```

### List Jobs

```bash
DATABRICKS_HOST=https://block-lakehouse-production.cloud.databricks.com \
databricks jobs list --limit 10
```

---

## Handling Long-Running Queries

For queries that take longer than 50 seconds:

1. **Submit without waiting:**

```bash
DATABRICKS_HOST=https://block-lakehouse-production.cloud.databricks.com \
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "a53b3ef899f7696a",
  "statement": "SELECT ... complex query ...",
  "wait_timeout": "0s"
}'
# Returns: {"statement_id": "01f0f2e4-..."}
```

2. **Poll for results:**

```bash
DATABRICKS_HOST=https://block-lakehouse-production.cloud.databricks.com \
databricks api get /api/2.0/sql/statements/STATEMENT_ID
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "no configuration file found" | Token cached but profile not saved - commands still work with `DATABRICKS_HOST` env var |
| OAuth token expired | Run `databricks auth login --host https://block-lakehouse-production.cloud.databricks.com` again |
| Query timeout | Use `wait_timeout: "0s"` and poll for results |
| Permission denied on table | Check catalog access - you may not have permissions to all catalogs |

### Check Auth Status

```bash
ls -la ~/.databricks/token-cache.json
```

### Re-authenticate

```bash
rm ~/.databricks/token-cache.json
databricks auth login --host https://block-lakehouse-production.cloud.databricks.com
```

---

## Known Catalogs (Partial List)

Popular catalogs include:
- `cdp` - Customer data platform
- `financial_data` - Financial/transaction data
- `cash_risk_ml` - Cash App risk ML data
- `app_banking` - Banking app data
- `anomalo` - Data quality monitoring

Use `SHOW CATALOGS` to see all available catalogs you have access to.
