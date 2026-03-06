# CI Test Visibility

Query Datadog CI Test Visibility via direct curl to the API proxy.

```bash
BASE_URL="https://dd-api-proxy.stage.sqprod.co/datadog"
```

## Search CI Test Events

```bash
curl -s -X POST "$BASE_URL/api/v2/ci/tests/events/search" \
  -H 'Content-Type: application/json' \
  -d '{
    "filter": {
      "query": "@test.service:my-service @test.status:fail",
      "from": "now-1d",
      "to": "now"
    },
    "page": {"limit": 10},
    "sort": "-timestamp"
  }' | jq '{count: (.data | length), tests: [.data[] | {id: .id, test: .attributes.attributes.test.name, suite: .attributes.attributes.test.suite, status: .attributes.attributes.test.status, duration_s: ((.attributes.attributes.duration // 0) / 1000000000)}]}'
```

### Test Query Syntax

| Filter | Example |
|--------|---------|
| Test service | `@test.service:my-service` |
| Test name | `@test.name:"test_login_flow"` |
| Status | `@test.status:fail` (values: `pass`, `fail`, `skip`) |
| Test suite | `@test.suite:unit_tests` |
| Language | `@language:python` |
| Branch | `@git.branch:main` |

Combine filters with spaces (AND) or `OR`:
`@test.service:my-service @test.status:fail @git.branch:main`

## Aggregate CI Test Metrics

Endpoint: `POST /api/v2/ci/tests/analytics/aggregate`

Same request body shape as pipeline aggregation. Aggregation functions: `count`, `avg`, `sum`, `min`, `max`, `median`, `pc75`, `pc90`, `pc95`, `pc99`, `cardinality`. Percentiles use `pc` prefix (e.g., `pc95`, not `p95`). See `ci-pipelines.md` for migration note.

### Flaky test detection: tests with highest failure counts

```bash
curl -s -X POST "$BASE_URL/api/v2/ci/tests/analytics/aggregate" \
  -H 'Content-Type: application/json' \
  -d '{
    "compute": [{"aggregation": "count", "type": "total"}],
    "filter": {"query": "@test.status:fail", "from": "now-7d", "to": "now"},
    "group_by": [{"facet": "@test.name", "limit": 20, "sort": {"type": "measure", "aggregation": "count", "order": "desc"}}]
  }' | jq '.data.buckets[] | {test: .by["@test.name"], failures: .computes.c0}'
```

### Test pass rate by suite

```bash
curl -s -X POST "$BASE_URL/api/v2/ci/tests/analytics/aggregate" \
  -H 'Content-Type: application/json' \
  -d '{
    "compute": [{"aggregation": "count", "type": "total"}],
    "filter": {"query": "@test.status:pass OR @test.status:fail", "from": "now-7d", "to": "now"},
    "group_by": [
      {"facet": "@test.suite", "limit": 20, "sort": {"type": "measure", "aggregation": "count", "order": "desc"}},
      {"facet": "@test.status", "limit": 5}
    ]
  }' | jq '.data.buckets[] | {suite: .by["@test.suite"], status: .by["@test.status"], count: .computes.c0}'
```

## Scope

Requires `ci_visibility_read` scope on dd-api-proxy (already enabled).
