# CI Observability Tables (Buildkite / CI System / ETL)

CI build and pipeline data synced into Snowflake via Fivetran.

## CI Observability Databases

| Platform | Database/Schema |
|----------|-----------------|
| Runway | `YOUR_DB.YOUR_SCHEMA.YOUR_TABLE` |
| Cashkite | `YOUR_DB.YOUR_SCHEMA.YOUR_TABLE` |
| your company-kite | `YOUR_DB.YOUR_SCHEMA.YOUR_TABLE` |
| Your CI System | `YOUR_CI.RAW_OLTP` |

## Recent Builds Summary

```bash
snow sql --format JSON -q "
SELECT
    DATE_TRUNC('day', CREATED_AT) as build_date,
    PIPELINE_SLUG,
    COUNT(*) as total_builds,
    SUM(CASE WHEN STATE = 'passed' THEN 1 ELSE 0 END) as passed,
    SUM(CASE WHEN STATE = 'failed' THEN 1 ELSE 0 END) as failed
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE CREATED_AT > DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY 1, 2
ORDER BY 1 DESC, 3 DESC
LIMIT 20
"
```

## Build Duration Stats

```bash
snow sql --format JSON -q "
SELECT
    PIPELINE_SLUG,
    COUNT(*) as build_count,
    AVG(DATEDIFF(second, STARTED_AT, FINISHED_AT)) as avg_duration_sec,
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY DATEDIFF(second, STARTED_AT, FINISHED_AT)) as median_duration_sec,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY DATEDIFF(second, STARTED_AT, FINISHED_AT)) as p95_duration_sec
FROM YOUR_DB.YOUR_SCHEMA.YOUR_TABLE
WHERE STATE = 'passed'
  AND CREATED_AT > DATEADD(day, -7, CURRENT_TIMESTAMP())
GROUP BY 1
ORDER BY build_count DESC
LIMIT 20
"
```
