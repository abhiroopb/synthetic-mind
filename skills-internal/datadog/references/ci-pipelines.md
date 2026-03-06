# CI Pipeline Visibility

Query Datadog CI Pipeline Visibility via direct curl to the API proxy.

```bash
BASE_URL="https://<dd-api-proxy-url>/datadog"
```

## Search CI Pipeline Events

```bash
curl -s -X POST "$BASE_URL/api/v2/ci/pipelines/events/search" \
  -H 'Content-Type: application/json' \
  -d '{
    "filter": {
      "query": "@ci.pipeline.name:my-pipeline",
      "from": "now-1d",
      "to": "now"
    },
    "page": {"limit": 10},
    "sort": "-timestamp"
  }' | jq '{count: (.data | length), pipelines: [.data[] | {id: .id, pipeline: .attributes.attributes.ci.pipeline.name, status: .attributes.attributes.ci.status, branch: .attributes.attributes.git.branch, duration_s: ((.attributes.attributes.duration // 0) / 1000000000), level: .attributes.ci_level}]}'
```

### Pipeline Query Syntax

| Filter | Example |
|--------|---------|
| Pipeline name | `@ci.pipeline.name:my-pipeline` |
| Status | `@ci.status:error` (values: `success`, `error`, `canceled`) |
| CI provider | `@ci.provider.name:github` |
| Branch | `@git.branch:main` |
| Event level | `@ci.level:pipeline` (vs `stage` or `job`) |

Combine filters with spaces (AND) or `OR`:
`@ci.pipeline.name:my-pipeline @ci.status:error @git.branch:main`

## Aggregate CI Pipeline Metrics

Endpoint: `POST /api/v2/ci/pipelines/analytics/aggregate`

### Count pipeline runs by status (last 7 days)

```bash
curl -s -X POST "$BASE_URL/api/v2/ci/pipelines/analytics/aggregate" \
  -H 'Content-Type: application/json' \
  -d '{
    "compute": [{"aggregation": "count", "type": "total"}],
    "filter": {"query": "*", "from": "now-7d", "to": "now"},
    "group_by": [{"facet": "@ci.status", "limit": 10, "sort": {"type": "measure", "aggregation": "count", "order": "desc"}}]
  }' | jq '.data.buckets[] | {status: .by["@ci.status"], count: .computes.c0}'
```

### Average pipeline duration by pipeline name

```bash
curl -s -X POST "$BASE_URL/api/v2/ci/pipelines/analytics/aggregate" \
  -H 'Content-Type: application/json' \
  -d '{
    "compute": [{"aggregation": "avg", "metric": "@ci.queue_time", "type": "total"}],
    "filter": {"query": "@ci.level:pipeline", "from": "now-7d", "to": "now"},
    "group_by": [{"facet": "@ci.pipeline.name", "limit": 10, "sort": {"type": "measure", "aggregation": "avg", "order": "desc"}}]
  }' | jq '.data.buckets[] | {pipeline: .by["@ci.pipeline.name"], avg_duration_ns: .computes.c0}'
```

### Timeseries: daily failure trend (last 14 days)

Use `"type": "timeseries"` with `"interval": "1d"` in compute. Filter: `@ci.status:error`, range: `now-14d` to `now`.

## Aggregation Functions

`count`, `avg`, `sum`, `min`, `max`, `median`, `pc75`, `pc90`, `pc95`, `pc99`, `cardinality`. Percentiles use `pc` prefix (e.g., `pc95`, not `p95`).

**Migration note:** The previous MCP tool (`mcp_datadog`) accepted `p95` as the aggregation parameter and translated internally. The raw Datadog API requires `pc95`. If porting queries from MCP, replace `p` with `pc`.

## Pagination

Cursor-based: next cursor is in `.meta.page.after`. Pass as `page.cursor`. Stop when `null` or no data.

## Scope

Requires `ci_visibility_read` scope on dd-api-proxy (already enabled).
