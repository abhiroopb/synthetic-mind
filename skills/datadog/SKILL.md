---
name: datadog
roles:
  - frontend
description: "Query Datadog for logs, metrics, traces, monitors, RUM, and CI visibility. Use when user needs observability data, investigating production issues, checking service health, analyzing frontend performance, or debugging CI/CD pipelines."
metadata:
  author: anonymous
  version: "0.3.0"
  status: "experimental"
---

# Datadog Skill

Query Datadog observability data via direct API calls. **No API keys, no MCP, no extra dependencies** -- just `curl` and `jq`.

## How It Works

All requests go through an internal API proxy (`dd-api-proxy`), which handles authentication automatically:

```bash
BASE_URL=https://<dd-api-proxy-url>/datadog

curl -s [-X POST] "$BASE_URL/<endpoint>" \
  -H 'Content-Type: application/json' \
  [-d '<request_body>'] | jq '<filter>'
```

## Reference Files

Load the reference for the domain you need:

- `references/endpoints.md` -- full endpoint table and proxy scope
- `references/logs.md` -- when searching logs or events
- `references/metrics.md` -- when querying timeseries metrics or listing available metrics
- `references/monitors.md` -- when searching or inspecting monitors
- `references/dashboards.md` -- when searching or viewing dashboards
- `references/apm.md` -- when searching APM spans by query
- `references/apm-traces.md` -- when looking up a specific trace by trace ID or correlating proxy logs
- `references/rum-search.md` -- when searching individual RUM events
- `references/rum-aggregate.md` -- when aggregating RUM metrics (counts, percentiles, timeseries)
- `references/ci-pipelines.md` -- when searching or aggregating CI pipeline events
- `references/ci-tests.md` -- when searching or aggregating CI test events
- `references/notebooks-downtimes.md` -- when working with notebooks, downtimes, or integrations

## Telemetry Knowledge (Start Here)

Before querying Datadog, search your internal monitoring knowledge base for service-specific insights:

```bash
curl -s -X POST 'https://<telemetry-knowledge-url>/mcp/' \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{
    "jsonrpc": "2.0", "id": "1", "method": "tools/call",
    "params": {
      "name": "search_telemetry_knowledge",
      "arguments": {"query": "<service or topic>", "limit": 5}
    }
  }' | jq '.result.content[0].text' -r
```

The trailing slash on the URL is required.

## Response Size Management

Raw API responses can be large (~4KB per log entry). Always use `jq` to extract only needed fields:

```bash
# Logs/spans: extract core fields (~200 bytes each instead of ~4KB)
| jq '{count: (.data | length), logs: [.data[] | {id: .id, ts: .attributes.timestamp, svc: .attributes.service, msg: .attributes.message}]}'

# Aggregations: responses are already small, pass through
| jq '.data.buckets'
```

Defaults: use `"page":{"limit":10}` unless the user asks for more. Use search endpoints with filters rather than listing all.

## Workflow

- [ ] **Telemetry knowledge** -- query the knowledge base for context (see above)
- [ ] **Query** -- use the appropriate API endpoint (see reference files)
- [ ] **Datadog URL** -- provide a link so the user can explore further: `https://<your-datadog-instance>.datadoghq.com/{logs,rum/explorer,apm/traces,monitors/manage,dashboard/<id>,ci/pipeline-executions}?query=<encoded_query>`
