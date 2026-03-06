# RUM Search Events

Base URL: `https://<dd-api-proxy-url>/datadog`

Requires `rum_apps_read` scope on dd-api-proxy (already enabled).

**Endpoint:** `POST /api/v2/rum/events/search`

Returns individual RUM events matching a query.

## Request Body

```json
{
  "filter": {
    "query": "@type:view",
    "from": "now-1h",
    "to": "now"
  },
  "sort": "-timestamp",
  "page": {"limit": 10}
}
```

- `sort`: `timestamp` (oldest first), `-timestamp` (newest first)
- `page.limit`: max events per page (default 10, max 1000)

## Example: Search Page Views

```bash
curl -s -X POST "https://<dd-api-proxy-url>/datadog/api/v2/rum/events/search" \
  -H 'Content-Type: application/json' \
  -d '{
    "filter": {
      "query": "@type:view @application.name:\"Dashboard Frontend\"",
      "from": "now-1h",
      "to": "now"
    },
    "sort": "-timestamp",
    "page": {"limit": 10}
  }' \
  | jq '{count: (.data | length), events: [.data[] | {id: .id, type: .attributes.attributes.type, app: .attributes.attributes.application.name, view: .attributes.attributes.view.name, ts: .attributes.timestamp}]}'
```

## Example: Search JavaScript Errors

```bash
curl -s -X POST "https://<dd-api-proxy-url>/datadog/api/v2/rum/events/search" \
  -H 'Content-Type: application/json' \
  -d '{
    "filter": {
      "query": "@type:error @error.source:source @application.name:\"Dashboard Frontend\"",
      "from": "now-1h",
      "to": "now"
    },
    "sort": "-timestamp",
    "page": {"limit": 10}
  }' \
  | jq '{count: (.data | length), events: [.data[] | {id: .id, error: .attributes.attributes.error.message, view: .attributes.attributes.view.name, ts: .attributes.timestamp}]}'
```

Other search types follow the same pattern. Change `"query"` filter: `@type:resource @resource.type:xhr` for XHR requests, `@type:action @action.type:click` for click actions.

## Query Syntax

| Query | Description |
|-------|-------------|
| `@type:view` | Page views |
| `@type:error` | Errors |
| `@type:action` | User actions (clicks, taps) |
| `@type:resource` | Network requests (XHR, fetch, images) |
| `@application.name:"Dashboard Frontend"` | Filter by app |
| `@view.name:"/dashboard/items/library"` | Filter by page/route |
| `@type:error @error.source:source` | JavaScript errors |
| `@type:action @action.type:click` | Click actions |
| `@type:resource @resource.type:xhr` | XHR requests |
| `@view.loading_type:initial_load` | Initial page loads only |

Combine filters with spaces (implicit AND): `@type:view @application.name:"My App" @view.name:"/home"`
