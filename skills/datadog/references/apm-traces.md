# APM Trace Lookup & Slow Spans

**Base URL:** `https://dd-api-proxy.stage.sqprod.co/datadog`

## Search by Speleo Trace ID

Common Block workflow: find a Datadog trace from a Speleo ID, then link to the trace UI.

```bash
BASE_URL=https://dd-api-proxy.stage.sqprod.co/datadog
TRACE_ID="abc123-def456"
ENV="production"

curl -s -X POST "$BASE_URL/api/v2/spans/events/search" \
  -H 'Content-Type: application/json' \
  -d "{\"data\":{\"type\":\"search_request\",\"attributes\":{\"filter\":{\"query\":\"env:$ENV @speleo_trace_id:\\\"$TRACE_ID\\\"\",\"from\":\"now-6h\",\"to\":\"now\"},\"page\":{\"limit\":50}}}}" \
  | jq '{count: (.data | length), spans: [.data[] | {service: .attributes.service, resource: .attributes.resource_name, duration_ms: ((.attributes.custom.duration // 0) / 1000000), status: .attributes.status, trace_id: .attributes.trace_id}]}'
```

Once you have the Datadog `trace_id` from a span result, open the trace in the UI:

```
https://square.datadoghq.com/apm/trace/<dd_trace_id>
```

## Envoy Logs for a Trace

Find Envoy proxy logs associated with a trace. This uses the **logs** search endpoint (not spans), which has a different request envelope (no `data` wrapper):

```bash
BASE_URL=https://dd-api-proxy.stage.sqprod.co/datadog

curl -s -X POST "$BASE_URL/api/v2/logs/events/search" \
  -H 'Content-Type: application/json' \
  -d '{"filter":{"query":"source:envoy @trace_id:<TRACE_ID>","from":"now-1h","to":"now"},"page":{"limit":10}}' \
  | jq '[.data[] | {ts: .attributes.timestamp, msg: .attributes.message, status: .attributes.attributes.http.status_code}]'
```

Replace `<TRACE_ID>` with the Datadog trace ID from the span search results.

## Slow Spans

Find spans exceeding a duration threshold (duration is in nanoseconds):

```bash
BASE_URL=https://dd-api-proxy.stage.sqprod.co/datadog

curl -s -X POST "$BASE_URL/api/v2/spans/events/search" \
  -H 'Content-Type: application/json' \
  -d '{
    "data": {
      "type": "search_request",
      "attributes": {
        "filter": {
          "query": "service:my-service env:production @duration:>5000000000",
          "from": "now-1h",
          "to": "now"
        },
        "page": {"limit": 25}
      }
    }
  }' \
  | jq '{count: (.data | length), spans: [.data[] | {service: .attributes.service, resource: .attributes.resource_name, duration_ms: ((.attributes.custom.duration // 0) / 1000000), trace_id: .attributes.trace_id}]}'
```

## Duration Reference

| Human-readable | Nanoseconds |
|----------------|-------------|
| 100ms | `100000000` |
| 500ms | `500000000` |
| 1 second | `1000000000` |
| 5 seconds | `5000000000` |
| 30 seconds | `30000000000` |

## Request Envelope Comparison

**Spans** (`/api/v2/spans/events/search`) wraps in `data`: `{"data": {"type": "search_request", "attributes": {"filter": {...}, "page": {...}}}}`

**Logs** (`/api/v2/logs/events/search`) uses top-level keys: `{"filter": {...}, "page": {...}}`
