# APM Span Search

**Base URL:** `https://dd-api-proxy.stage.sqprod.co/datadog`

## Search Spans

**Endpoint:** `POST /api/v2/spans/events/search`

> **Important:** This API uses a nested `data` envelope — different from the logs search endpoint which accepts `filter` at the top level.

### Request Structure

```json
{
  "data": {
    "type": "search_request",
    "attributes": {
      "filter": {
        "query": "service:my-service @error:true",
        "from": "now-1h",
        "to": "now"
      },
      "page": {"limit": 10}
    }
  }
}
```

### Example with jq

```bash
BASE_URL=https://dd-api-proxy.stage.sqprod.co/datadog

curl -s -X POST "$BASE_URL/api/v2/spans/events/search" \
  -H 'Content-Type: application/json' \
  -d '{
    "data": {
      "type": "search_request",
      "attributes": {
        "filter": {
          "query": "service:my-service env:production @error:true",
          "from": "now-1h",
          "to": "now"
        },
        "page": {"limit": 25}
      }
    }
  }' \
  | jq '{count: (.data | length), spans: [.data[] | {id: .id, service: .attributes.service, resource: .attributes.resource_name, duration_ms: ((.attributes.custom.duration // 0) / 1000000), status: .attributes.status, trace_id: .attributes.trace_id, status_code: .attributes.custom.http.status_code}]}'
```

## Query Syntax

| Filter | Example | Notes |
|--------|---------|-------|
| Service | `service:my-service` | Filter by service name |
| Error spans | `@error:true` | Only spans that errored |
| Environment | `env:production` | Environment filter |
| HTTP status | `@http.status_code:500` | HTTP status code |
| Duration | `@duration:>5000000000` | Duration in **nanoseconds** (5s = 5,000,000,000) |
| Resource | `resource_name:"GET /api/v2/users"` | Specific resource/endpoint |
| Speleo trace ID | `@speleo_trace_id:"abc123-def456"` | Block's internal trace ID format |

Combine filters with spaces (implicit AND):
```
service:my-service env:production @error:true @duration:>5000000000
```
