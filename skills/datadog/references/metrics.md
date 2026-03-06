# Datadog Metrics

Base URL: `https://<dd-api-proxy-url>/datadog`

## Query Timeseries

**Endpoint:** `GET /api/v1/query` with `from` (POSIX), `to` (POSIX), `query` params.

```bash
FROM=$(date -v-1H +%s); TO=$(date +%s)
curl -s -G "https://<dd-api-proxy-url>/datadog/api/v1/query" \
  --data-urlencode "from=$FROM" --data-urlencode "to=$TO" --data-urlencode "query=avg:system.cpu.user{*}" \
  | jq '{status: .status, series: [.series[] | {metric: .metric, scope: .scope, points: (.pointlist | length)}]}'
```

Time helpers:
- macOS: `date -v-1H +%s` (1h ago), `date -v-24H +%s` (24h ago), `date -v-7d +%s` (7d ago)
- Linux: `date -d '1 hour ago' +%s`, `date -d '24 hours ago' +%s`, `date -d '7 days ago' +%s`

Recommended max 1 day per query for performance. For longer ranges, split into multiple calls.

### top() Function

When grouping by a tag, use `top()` to limit series: `top(<query> by {tag}, <limit>, '<agg>', '<dir>')`.
- Limit: 5, 10, 25, 50, or 100
- Agg: `max`, `mean`, `min`, `sum`, `last`
- Dir: `asc` or `desc`

```bash
FROM=$(date -v-1H +%s); TO=$(date +%s)
QUERY="top(sum:trace.servlet.request.errors{env:production} by {service}, 10, 'sum', 'desc')"
curl -s -G "https://<dd-api-proxy-url>/datadog/api/v1/query" \
  --data-urlencode "from=$FROM" --data-urlencode "to=$TO" --data-urlencode "query=$QUERY" \
  | jq '{series: [.series[] | {scope: .scope, avg: (.pointlist | map(.[1] // 0) | add / length)}]}'
```

### Multiple Queries

Run multiple metric queries by iterating (the API accepts one query per call):

```bash
FROM=$(date -v-1H +%s); TO=$(date +%s)
for Q in "avg:system.cpu.user{*}" "avg:system.mem.used{*}"; do
  curl -s -G "https://<dd-api-proxy-url>/datadog/api/v1/query" \
    --data-urlencode "from=$FROM" --data-urlencode "to=$TO" --data-urlencode "query=$Q" \
    | jq "{query: \"$Q\", series: [.series[] | {scope: .scope, points: (.pointlist | length)}]}"
done
```

### Metric Explorer URL

After querying, construct a link to explore further in the UI:

```
https://<your-datadog-instance>.datadoghq.com/metric/explorer?fromUser=true&start=<FROM_MS>&end=<TO_MS>&paused=true#<URL_ENCODED_QUERY>
```

Timestamps are in milliseconds (POSIX seconds * 1000).

## List Metrics

**Endpoint:** `GET /api/v2/metrics`

```bash
# By service
curl -s "https://<dd-api-proxy-url>/datadog/api/v2/metrics?filter[configured]=true&filter[tags_configured]=service:my-service&window[seconds]=3600" \
  | jq '[.data[] | .id]'
```

To list trace metrics for a service (error, latency, throughput), filter by both service and span.kind:

```bash
curl -s "https://<dd-api-proxy-url>/datadog/api/v2/metrics?filter[configured]=true&filter[tags_configured]=service:my-service,span.kind:*&window[seconds]=3600" \
  | jq '[.data[] | .id]'
```

## Get Metric Tags

**Endpoint:** `GET /api/v2/metrics/{metric_name}/all-tags`

```bash
curl -s "https://<dd-api-proxy-url>/datadog/api/v2/metrics/system.cpu.user/all-tags" \
  | jq '.data.attributes.tags'
```

## Common Metrics

Service: `trace.servlet.request.hits{service:X}` (count), `trace.servlet.request.errors{service:X}` (errors), `trace.servlet.request.duration{service:X}` (latency).
System: `system.cpu.user{*}`, `system.mem.used{*}`, `system.disk.used{*}`.
