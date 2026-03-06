# Monitors

Reference for querying Datadog Monitors via the API proxy.

```
BASE_URL=https://dd-api-proxy.stage.sqprod.co/datadog
```

## Search Monitors

The search endpoint supports a query syntax for filtering by status, tags, and title.

```bash
curl -s "$BASE_URL/api/v1/monitor/search?query=status:alert&per_page=10" \
  | jq '{count: .metadata.total_count, monitors: [.monitors[] | {id: .id, name: .name, status: .status, type: .type, tags: .tags}]}'
```

Query syntax examples:

| Query | Description |
|-------|-------------|
| `status:alert` | Monitors currently alerting |
| `status:ok` | Monitors in OK state |
| `status:warn` | Monitors in warning state |
| `tag:service:payments` | Monitors tagged with `service:payments` |
| `title:*cpu*` | Monitors with "cpu" in the title |
| `status:alert tag:team:platform` | Combine filters with spaces (AND) |

Paginate with `page` (0-indexed):

```bash
curl -s "$BASE_URL/api/v1/monitor/search?query=status:alert&per_page=50&page=0" \
  | jq '.metadata.total_count'
```

## Get Monitor by ID

```bash
curl -s "$BASE_URL/api/v1/monitor/12345678" \
  | jq '{id: .id, name: .name, status: .overall_state, type: .type, query: .query, thresholds: .options.thresholds, created_by: .creator.email, tags: .tags}'
```

## List Monitors (filtered)

Filter by name:

```bash
curl -s "$BASE_URL/api/v1/monitor?name=my-monitor&page=0&page_size=10" \
  | jq '[.[] | {id: .id, name: .name, status: .overall_state}]'
```

Filter by tags:

```bash
curl -s "$BASE_URL/api/v1/monitor?monitor_tags=service:payments&page=0&page_size=10" \
  | jq '[.[] | {id: .id, name: .name, status: .overall_state}]'
```

Multiple tags (comma-separated, AND logic):

```bash
curl -s "$BASE_URL/api/v1/monitor?monitor_tags=service:payments,env:production&page=0&page_size=10" \
  | jq '[.[] | {id: .id, name: .name, status: .overall_state, tags: .tags}]'
```

## Monitor Group States

Check per-group status for multi-alert monitors:

```bash
curl -s "$BASE_URL/api/v1/monitor/12345678?group_states=all" \
  | jq '{name: .name, groups: .state.groups | to_entries | map({group: .key, status: .value.status, last_triggered: .value.last_triggered_ts})}'
```

## Datadog URL

```
https://square.datadoghq.com/monitors/manage?q=<encoded_query>
https://square.datadoghq.com/monitors/<monitor_id>
```
