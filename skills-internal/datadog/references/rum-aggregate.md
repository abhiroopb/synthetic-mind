# RUM Aggregate Events

Base URL: `https://<dd-api-proxy-url>/datadog`

**Endpoint:** `POST /api/v2/rum/analytics/aggregate`

Returns aggregated metrics (counts, averages, percentiles) with optional grouping.

## Count Aggregation with Grouping

```bash
curl -s -X POST "https://<dd-api-proxy-url>/datadog/api/v2/rum/analytics/aggregate" \
  -H 'Content-Type: application/json' \
  -d '{
    "compute": [{"aggregation": "count", "type": "total"}],
    "filter": {"query": "@type:view", "from": "now-1h", "to": "now"},
    "group_by": [{"facet": "@application.name", "limit": 10, "sort": {"type": "measure", "aggregation": "count", "order": "desc"}}]
  }' \
  | jq '.data.buckets[] | {app: .by["@application.name"], views: .computes.c0}'
```

## Metric Aggregation (avg, p95, etc.)

Non-count aggregations require a `metric` field:

```bash
curl -s -X POST "https://<dd-api-proxy-url>/datadog/api/v2/rum/analytics/aggregate" \
  -H 'Content-Type: application/json' \
  -d '{
    "compute": [{"aggregation": "pc95", "metric": "@view.loading_time", "type": "total"}],
    "filter": {"query": "@type:view @view.loading_type:initial_load", "from": "now-24h", "to": "now"},
    "group_by": [{"facet": "@view.name", "limit": 10, "sort": {"type": "measure", "aggregation": "pc95", "order": "desc"}}]
  }' \
  | jq '.data.buckets[] | {page: .by["@view.name"], p95_loading_time_ns: .computes.c0}'
```

Replace `pc95` with `avg`, `sum`, `min`, `max`, `median`, or other functions as needed.

## Timeseries & Multi-Dimensional Grouping

For timeseries, change `"type": "total"` to `"type": "timeseries"` and add `"interval": "1d"` (or `1h`, `5m`, etc.).

For multi-dimensional grouping, add multiple entries to `group_by` array (e.g., group by both `@view.name` and `@browser.name`).

## Aggregation Functions

| Function | Description |
|----------|-------------|
| `count` | Event count (no `metric` needed) |
| `avg` | Average |
| `sum` / `min` / `max` | Sum, minimum, maximum |
| `median` | Median (50th percentile) |
| `pc75` / `pc90` / `pc95` / `pc99` | Percentiles |
| `cardinality` | Unique count |

**Note:** The API uses `pc` prefix for percentiles (not `p`): `pc75`, `pc90`, `pc95`, `pc99`.

## Common Facets

| Facet | Description |
|-------|-------------|
| `@view.name` | Page/route name |
| `@application.name` | RUM application |
| `@browser.name` | Browser (Chrome, Firefox, etc.) |
| `@geo.country` | User country |
| `@os.name` | Operating system |
| `@view.url_path` | URL path |
| `@view.loading_type` | `initial_load` or `route_change` |

## Common Metrics

| Metric | Description |
|--------|-------------|
| `@view.loading_time` | Total page load time (ns) |
| `@view.largest_contentful_paint` | LCP (ns) |
| `@view.first_contentful_paint` | FCP (ns) |
| `@view.cumulative_layout_shift` | CLS |
| `@view.interaction_to_next_paint` | INP (ns) |
