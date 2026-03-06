---
Skill name: databricks
Skill description: Query the Databricks Lakehouse using SQL. Use when user needs to query Databricks, search tables/catalogs, or run SQL against Databricks data.
---

# Databricks Skill

Query the Databricks Lakehouse using the Databricks CLI.

## Prerequisites

### Install Databricks CLI

```bash
brew tap databricks/tap
brew install databricks
```

### Authenticate (First Time)

```bash
databricks auth login --host https://<your-databricks-host>.cloud.databricks.com
```

This opens a browser for OAuth login. After authenticating, tokens are cached at `~/.databricks/token-cache.json`.

---

## Quick Reference

Set the host in your environment:

```bash
export DATABRICKS_HOST=https://<your-databricks-host>.cloud.databricks.com
```

Or pass it inline with each command.

---

## Running SQL Queries

Use the Statement Execution API to run SQL:

```bash
DATABRICKS_HOST=https://<your-databricks-host>.cloud.databricks.com \
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "<your-warehouse-id>",
  "statement": "SELECT 1 as test",
  "wait_timeout": "30s"
}'
```

**Available warehouses:**

Configure your warehouse IDs based on your Databricks workspace. Use `databricks warehouses list` to discover available warehouses.

**Note:** `wait_timeout` must be between 5s and 50s. For long queries, use `0s` and poll for results.

---

## Common Queries

### List Catalogs

```bash
DATABRICKS_HOST=https://<your-databricks-host>.cloud.databricks.com \
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "<your-warehouse-id>",
  "statement": "SHOW CATALOGS",
  "wait_timeout": "30s"
}' | jq -r '.result.data_array[][]'
```

### Search for Tables

```bash
DATABRICKS_HOST=https://<your-databricks-host>.cloud.databricks.com \
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "<your-warehouse-id>",
  "statement": "SELECT table_catalog, table_schema, table_name FROM system.information_schema.tables WHERE lower(table_name) LIKE '\''%search_term%'\'' LIMIT 20",
  "wait_timeout": "50s"
}' | jq '.result.data_array'
```

### Describe a Table

```bash
DATABRICKS_HOST=https://<your-databricks-host>.cloud.databricks.com \
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "<your-warehouse-id>",
  "statement": "DESCRIBE catalog.schema.table_name",
  "wait_timeout": "30s"
}' | jq '.result.data_array'
```

### Query with Results

```bash
DATABRICKS_HOST=https://<your-databricks-host>.cloud.databricks.com \
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "<your-warehouse-id>",
  "statement": "SELECT * FROM catalog.schema.table LIMIT 10",
  "wait_timeout": "50s"
}' | jq '{columns: .manifest.schema.columns[].name, data: .result.data_array}'
```

---

## Other CLI Commands

### List Warehouses

```bash
DATABRICKS_HOST=https://<your-databricks-host>.cloud.databricks.com \
databricks warehouses list
```

### List Running Clusters

```bash
DATABRICKS_HOST=https://<your-databricks-host>.cloud.databricks.com \
databricks clusters list
```

### List Jobs

```bash
DATABRICKS_HOST=https://<your-databricks-host>.cloud.databricks.com \
databricks jobs list --limit 10
```

---

## Handling Long-Running Queries

For queries that take longer than 50 seconds:

1. **Submit without waiting:**

```bash
DATABRICKS_HOST=https://<your-databricks-host>.cloud.databricks.com \
databricks api post /api/2.0/sql/statements --json '{
  "warehouse_id": "<your-warehouse-id>",
  "statement": "SELECT ... complex query ...",
  "wait_timeout": "0s"
}'
# Returns: {"statement_id": "01f0f2e4-..."}
```

2. **Poll for results:**

```bash
DATABRICKS_HOST=https://<your-databricks-host>.cloud.databricks.com \
databricks api get /api/2.0/sql/statements/STATEMENT_ID
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "no configuration file found" | Token cached but profile not saved - commands still work with `DATABRICKS_HOST` env var |
| OAuth token expired | Run `databricks auth login --host https://<your-databricks-host>.cloud.databricks.com` again |
| Query timeout | Use `wait_timeout: "0s"` and poll for results |
| Permission denied on table | Check catalog access - you may not have permissions to all catalogs |

### Check Auth Status

```bash
ls -la ~/.databricks/token-cache.json
```

### Re-authenticate

```bash
rm ~/.databricks/token-cache.json
databricks auth login --host https://<your-databricks-host>.cloud.databricks.com
```

---

## Known Catalogs

Use `SHOW CATALOGS` to see all available catalogs you have access to. Catalogs are organization-specific and will vary by workspace.
