# Dashboards

Reference for querying Datadog Dashboards via the API proxy.

```
BASE_URL=https://<dd-api-proxy-url>/datadog
```

## List Dashboards

Returns dashboards sorted by most recently modified:

```bash
curl -s "$BASE_URL/api/v1/dashboard?count=10" \
  | jq '[.dashboards[] | {id: .id, title: .title, url: .url}]'
```

## Search Dashboards by Keyword

The list endpoint does not support server-side search or fuzzy matching. List a larger batch and filter client-side with jq regex. For more sophisticated matching, refine in the Datadog UI.

```bash
curl -s "$BASE_URL/api/v1/dashboard?count=100" \
  | jq '[.dashboards[] | select(.title | test("payment"; "i")) | {id: .id, title: .title}]'
```

Case-insensitive search across title and description:

```bash
curl -s "$BASE_URL/api/v1/dashboard?count=200" \
  | jq '[.dashboards[] | select((.title // "") + " " + (.description // "") | test("latency"; "i")) | {id: .id, title: .title}]'
```

## Get Dashboard by ID

Summary view:

```bash
curl -s "$BASE_URL/api/v1/dashboard/32e-yrv-dm4" \
  | jq '{id: .id, title: .title, description: .description, widgets: (.widgets | length), url: .url}'
```

Widget inventory (types and titles):

```bash
curl -s "$BASE_URL/api/v1/dashboard/32e-yrv-dm4" \
  | jq '{title: .title, widgets: [.widgets[] | {id: .id, title: .definition.title, type: .definition.type}]}'
```

Extract metric queries from all widgets:

```bash
curl -s "$BASE_URL/api/v1/dashboard/32e-yrv-dm4" \
  | jq '[.widgets[].definition | select(.requests) | .requests[]? | .q // .queries[]?.query] | map(select(. != null)) | unique'
```

URL: `https://<your-datadog-instance>.datadoghq.com/dashboard/<dashboard_id>`

## Common Patterns

### Combining Monitor Search with Dashboard Lookup

```bash
curl -s "$BASE_URL/api/v1/monitor/search?query=status:alert+tag:service:payments&per_page=5" \
  | jq '[.monitors[] | {id: .id, name: .name}]'
curl -s "$BASE_URL/api/v1/dashboard?count=100" \
  | jq '[.dashboards[] | select(.title | test("payment"; "i")) | {id: .id, title: .title}]'
```

## Proxy Permissions

| Scope | Status |
|-------|--------|
| monitors_read | ✅ |
| dashboards_read | ✅ |
| notebooks_read | ✅ |
| events_read | ✅ |

Write operations (creating downtimes) may require additional proxy scopes. If a call returns 403, the proxy lacks permission.
