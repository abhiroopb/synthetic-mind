# Datadog Logs & Events

Base URL: `https://<dd-api-proxy-url>/datadog`

## Search Logs

**Endpoint:** `POST /api/v2/logs/events/search`

```bash
curl -s -X POST "https://<dd-api-proxy-url>/datadog/api/v2/logs/events/search" \
  -H 'Content-Type: application/json' \
  -d '{"filter":{"query":"service:my-service status:error","from":"now-1h","to":"now"},"sort":"-timestamp","page":{"limit":10}}' \
  | jq '{count: (.data | length), logs: [.data[] | {id: .id, ts: .attributes.timestamp, svc: .attributes.service, msg: .attributes.message, level: .attributes.attributes.level, trace: .attributes.attributes.trace_id}]}'
```

Query syntax: `service:X status:error`, `@http.status_code:500`, `env:production service:payments`, `@error.kind:TimeoutError`. Combine with spaces (AND).

## Pagination

Responses include a cursor for fetching more results:

```bash
# First page
| jq '{status: .meta.status, cursor: .meta.page.after, count: (.data | length)}'

# Next page: pass cursor back as page.cursor
-d '{"filter":{...},"page":{"limit":10,"cursor":"eyJhZnRlci..."}}'
```

Stop when `.meta.page.after` is `null` or `.data` is empty. Status `.meta.status` is `"done"` when complete.

## Discover Log Schema

Fetch one log and inspect all available field paths, then add them to the jq projection:

```bash
# Top-level keys
| jq '.data[0].attributes | keys'
# Nested attribute keys (where most service-specific fields live)
| jq '.data[0].attributes.attributes | keys'
# Full recursive path listing (all dot-paths, no values)
| jq '[.data[0].attributes | [paths(scalars)] | .[] | join(".")]'
# Then use discovered paths in your jq filter:
| jq '[.data[] | {id: .id, ts: .attributes.timestamp, msg: .attributes.message, path: .attributes.attributes.request.path}]'
```

## Search Events

**Endpoint:** `POST /api/v2/events/search` (same request body shape as logs)

```bash
curl -s -X POST "https://<dd-api-proxy-url>/datadog/api/v2/events/search" \
  -H 'Content-Type: application/json' \
  -d '{"filter":{"query":"source:jenkins","from":"now-24h","to":"now"},"page":{"limit":10}}' \
  | jq '[.data[] | {id: .id, title: .attributes.attributes.title, ts: .attributes.timestamp, source: .attributes.attributes.service}]'
```

### Event Query Syntax

| Query | Description |
|-------|-------------|
| `source:jenkins` | Events from Jenkins |
| `source:github` | Events from GitHub |
| `priority:normal` | Normal priority events |
| `@evt.name:deployment` | Events with specific name |
| `host:prod-server-*` | Events from hosts matching pattern |
| `tags:deployment env:production` | Tagged events |
| `"error occurred"` | Text search in event title/text |

Combine filters with spaces (AND). Supports wildcards: `source:*jenkins*`, `@evt.name:deploy*`.
