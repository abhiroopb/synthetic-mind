# Snowflake Access History

Query access history to find which users, services, and queries have accessed specific tables and columns.

## Tables

### SNOWFLAKE_USAGE.ACCOUNT_USAGE.ACCESS_HISTORY

Records every query's data access, including which objects (tables/views) and columns were read. Each row represents a query execution. The `DIRECT_OBJECTS_ACCESSED` and `BASE_OBJECTS_ACCESSED` columns are VARIANT arrays containing the objects and columns touched by the query.

**Key Fields:**
- `QUERY_ID` (TEXT) — Unique query identifier
- `QUERY_START_TIME` (TIMESTAMP_LTZ) — When the query started
- `USER_NAME` (TEXT) — Snowflake user who ran the query (uppercase LDAP for humans, service account names for bots)
- `DIRECT_OBJECTS_ACCESSED` (ARRAY) — Objects directly referenced in the query. Each element contains:
  - `objectName` (TEXT) — Fully qualified object name (e.g., `ONBOARD.RAW_OLTP.ACTIVATION_FLOWS`)
  - `objectDomain` (TEXT) — Object type (e.g., `Table`, `View`)
  - `columns` (ARRAY) — Columns accessed, each with `columnName` and `columnId`
- `BASE_OBJECTS_ACCESSED` (ARRAY) — Underlying base tables accessed (resolves views to their source tables)
- `OBJECTS_MODIFIED` (ARRAY) — Objects modified by the query (for writes/DDL)
- `OBJECT_MODIFIED_BY_DDL` (OBJECT) — DDL changes

**Important:** This view has a ~2 hour latency. Data is retained for 365 days.

### APP_ENGOPS.PUBLIC.ENG_LDAPS

Square/Block employee directory. Used to determine whether a Snowflake user is a human employee or a service account.

**Key Fields:**
- `IC_LDAP` (TEXT) — Employee LDAP username (lowercase)

**Join pattern:** `UPPER(el.IC_LDAP) = h.USER_NAME` — ACCESS_HISTORY stores usernames in uppercase; ENG_LDAPS stores them in lowercase.

## Querying Access History

The `DIRECT_OBJECTS_ACCESSED` column is a nested VARIANT array that must be flattened to extract individual tables and columns.

### Flatten Pattern

```sql
SELECT
    h.USER_NAME,
    f.value:"objectName"::STRING AS object_name,
    col.value:"columnName"::STRING AS column_name
FROM SNOWFLAKE_USAGE.ACCOUNT_USAGE.ACCESS_HISTORY AS h,
     LATERAL FLATTEN(input => h.DIRECT_OBJECTS_ACCESSED) f,
     LATERAL FLATTEN(input => f.value:"columns", outer => true) col
WHERE h.QUERY_START_TIME::DATE >= CURRENT_DATE() - 7
```

- First `LATERAL FLATTEN` expands each accessed object into its own row
- Second `LATERAL FLATTEN` (with `outer => true`) expands each column; `outer => true` keeps rows even when column list is empty
- Use `SPLIT_PART` on `objectName` to extract service, database, and table components

**Important — do not inline LATERAL FLATTEN with explicit JOINs:** Snowflake does not allow `LATERAL FLATTEN` (comma-join syntax) on the left side of an explicit `JOIN` in the same `FROM` clause. Always use a CTE to wrap the `LATERAL FLATTEN` query first, then join the CTE result to other tables like `ENG_LDAPS`.

### Filter Out CDC Metadata Columns

CDC pipeline columns (prefixed with `__`) should typically be excluded:

```sql
AND column_name NOT LIKE '\\_\\_%' ESCAPE '\\'
```

## Common Query Patterns

### Find All Users Accessing a Specific Database (Last 7 Days)

```sql
WITH base_data AS (
    SELECT DISTINCT
        SPLIT_PART(f.value:"objectName"::STRING, '.', 1) AS service,
        SPLIT_PART(f.value:"objectName"::STRING, '.', 2) AS database,
        SPLIT_PART(f.value:"objectName"::STRING, '.', 3) AS table_name,
        col.value:"columnName"::STRING AS column_name,
        h.USER_NAME AS user
    FROM SNOWFLAKE_USAGE.ACCOUNT_USAGE.ACCESS_HISTORY AS h,
         LATERAL FLATTEN(input => h.DIRECT_OBJECTS_ACCESSED) f,
         LATERAL FLATTEN(input => f.value:"columns", outer => true) col
    WHERE h.QUERY_START_TIME::DATE >= CURRENT_DATE() - 7
      AND database != 'INFORMATION_SCHEMA'
      AND column_name NOT LIKE '\\_\\_%' ESCAPE '\\'
      AND UPPER(f.value:"objectName"::STRING) LIKE 'ONBOARD.%'
)
SELECT base_data.*
FROM base_data
ORDER BY service, database, table_name, column_name
```

Change `LIKE 'ONBOARD.%'` to filter by a different database (e.g., `'LEGALENTITIES.%'`, `'MULTIPASS.%'`).

### Filter to Non-Human (Service Account) Users Only

Join against the employee directory to exclude human users — any user NOT found in `ENG_LDAPS` is a service account:

```sql
WITH base_data AS (
    SELECT DISTINCT
        SPLIT_PART(f.value:"objectName"::STRING, '.', 1) AS service,
        SPLIT_PART(f.value:"objectName"::STRING, '.', 2) AS database,
        SPLIT_PART(f.value:"objectName"::STRING, '.', 3) AS table_name,
        col.value:"columnName"::STRING AS column_name,
        h.USER_NAME AS user
    FROM SNOWFLAKE_USAGE.ACCOUNT_USAGE.ACCESS_HISTORY AS h,
         LATERAL FLATTEN(input => h.DIRECT_OBJECTS_ACCESSED) f,
         LATERAL FLATTEN(input => f.value:"columns", outer => true) col
    WHERE h.QUERY_START_TIME::DATE >= CURRENT_DATE() - 7
      AND database != 'INFORMATION_SCHEMA'
      AND column_name NOT LIKE '\\_\\_%' ESCAPE '\\'
      AND UPPER(f.value:"objectName"::STRING) LIKE 'ONBOARD.%'
)
SELECT base_data.*
FROM base_data
LEFT JOIN APP_ENGOPS.PUBLIC.ENG_LDAPS AS el
    ON UPPER(el.IC_LDAP) = user
WHERE el.IC_LDAP IS NULL
ORDER BY service, database, table_name, column_name
```

### Filter to Human Users Only

Inverse of the above — keep only users found in the employee directory:

```sql
WITH base_data AS (
    SELECT DISTINCT
        SPLIT_PART(f.value:"objectName"::STRING, '.', 1) AS service,
        SPLIT_PART(f.value:"objectName"::STRING, '.', 2) AS database,
        SPLIT_PART(f.value:"objectName"::STRING, '.', 3) AS table_name,
        col.value:"columnName"::STRING AS column_name,
        h.USER_NAME AS user
    FROM SNOWFLAKE_USAGE.ACCOUNT_USAGE.ACCESS_HISTORY AS h,
         LATERAL FLATTEN(input => h.DIRECT_OBJECTS_ACCESSED) f,
         LATERAL FLATTEN(input => f.value:"columns", outer => true) col
    WHERE h.QUERY_START_TIME::DATE >= CURRENT_DATE() - 7
      AND database != 'INFORMATION_SCHEMA'
      AND column_name NOT LIKE '\\_\\_%' ESCAPE '\\'
      AND UPPER(f.value:"objectName"::STRING) LIKE 'ONBOARD.%'
)
SELECT base_data.*
FROM base_data
JOIN APP_ENGOPS.PUBLIC.ENG_LDAPS AS el
    ON UPPER(el.IC_LDAP) = user
ORDER BY service, database, table_name, column_name
```

### Find Who Accessed a Specific Table

```sql
SELECT DISTINCT
    h.USER_NAME,
    h.QUERY_START_TIME,
    h.QUERY_ID
FROM SNOWFLAKE_USAGE.ACCOUNT_USAGE.ACCESS_HISTORY AS h,
     LATERAL FLATTEN(input => h.DIRECT_OBJECTS_ACCESSED) f
WHERE h.QUERY_START_TIME::DATE >= CURRENT_DATE() - 7
  AND UPPER(f.value:"objectName"::STRING) = 'ONBOARD.RAW_OLTP.ACTIVATION_FLOWS'
ORDER BY h.QUERY_START_TIME DESC
```

### Find Who Accessed a Specific Column

```sql
SELECT DISTINCT
    h.USER_NAME,
    h.QUERY_START_TIME,
    col.value:"columnName"::STRING AS column_name
FROM SNOWFLAKE_USAGE.ACCOUNT_USAGE.ACCESS_HISTORY AS h,
     LATERAL FLATTEN(input => h.DIRECT_OBJECTS_ACCESSED) f,
     LATERAL FLATTEN(input => f.value:"columns", outer => true) col
WHERE h.QUERY_START_TIME::DATE >= CURRENT_DATE() - 7
  AND UPPER(f.value:"objectName"::STRING) = 'ONBOARD.RAW_OLTP.UNDERWRITING_REQUESTS'
  AND col.value:"columnName"::STRING = 'DECISION'
ORDER BY h.QUERY_START_TIME DESC
```

### Most Accessed Tables by User Count (Last 30 Days)

```sql
SELECT
    UPPER(f.value:"objectName"::STRING) AS object_name,
    COUNT(DISTINCT h.USER_NAME) AS distinct_users,
    COUNT(DISTINCT h.QUERY_ID) AS query_count
FROM SNOWFLAKE_USAGE.ACCOUNT_USAGE.ACCESS_HISTORY AS h,
     LATERAL FLATTEN(input => h.DIRECT_OBJECTS_ACCESSED) f
WHERE h.QUERY_START_TIME::DATE >= CURRENT_DATE() - 30
  AND UPPER(f.value:"objectName"::STRING) LIKE 'ONBOARD.%'
GROUP BY object_name
ORDER BY distinct_users DESC
LIMIT 20
```

## Customization Guide

The base query can be filtered on any combination of:

| Filter | Where Clause |
|--------|-------------|
| Database/Service | `UPPER(f.value:"objectName"::STRING) LIKE 'ONBOARD.%'` |
| Specific table | `UPPER(f.value:"objectName"::STRING) = 'ONBOARD.RAW_OLTP.ACTIVATION_FLOWS'` |
| Column name | `col.value:"columnName"::STRING = 'MERCHANT_TOKEN'` |
| Time range | `h.QUERY_START_TIME::DATE >= CURRENT_DATE() - 7` |
| Human users only | `JOIN APP_ENGOPS.PUBLIC.ENG_LDAPS AS el ON UPPER(el.IC_LDAP) = user` |
| Service accounts only | `LEFT JOIN ... WHERE el.IC_LDAP IS NULL` |
| Exclude CDC columns | `column_name NOT LIKE '\\_\\_%' ESCAPE '\\'` |
| Exclude INFORMATION_SCHEMA | `database != 'INFORMATION_SCHEMA'` |
