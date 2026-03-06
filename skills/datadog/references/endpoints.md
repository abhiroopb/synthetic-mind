# Datadog API Endpoints

Base URL: `https://<dd-api-proxy-url>/datadog`

## Endpoint Reference

| Domain | Method | Endpoint | Reference |
|--------|--------|----------|-----------|
| Logs | POST | `/api/v2/logs/events/search` | `logs.md` |
| Events | POST | `/api/v2/events/search` | `logs.md` |
| Metrics Query | GET | `/api/v1/query?from=&to=&query=` | `metrics.md` |
| Metrics List | GET | `/api/v2/metrics` | `metrics.md` |
| Metric Tags | GET | `/api/v2/metrics/{name}/all-tags` | `metrics.md` |
| Monitors | GET | `/api/v1/monitor/search?query=` | `monitors.md` |
| Dashboards | GET | `/api/v1/dashboard` | `dashboards.md` |
| APM Spans | POST | `/api/v2/spans/events/search` | `apm.md` |
| APM Traces | POST | `/api/v2/spans/events/search` | `apm-traces.md` |
| RUM Search | POST | `/api/v2/rum/events/search` | `rum-search.md` |
| RUM Aggregate | POST | `/api/v2/rum/analytics/aggregate` | `rum-aggregate.md` |
| CI Pipelines | POST | `/api/v2/ci/pipelines/events/search` | `ci-pipelines.md` |
| CI Pipe Agg | POST | `/api/v2/ci/pipelines/analytics/aggregate` | `ci-pipelines.md` |
| CI Tests | POST | `/api/v2/ci/tests/events/search` | `ci-tests.md` |
| CI Tests Agg | POST | `/api/v2/ci/tests/analytics/aggregate` | `ci-tests.md` |
| Notebooks | GET | `/api/v1/notebooks` | `notebooks-downtimes.md` |
| Downtimes | GET/POST/DELETE | `/api/v2/downtime` | `notebooks-downtimes.md` |
| Integrations | GET | `/api/v1/integration/{type}` | `notebooks-downtimes.md` |

## Proxy Scope

The dd-api-proxy handles auth automatically. If a call returns 403, the proxy lacks that scope.

Enabled: logs, metrics, monitors, dashboards, spans (APM), RUM, CI visibility, events, notebooks, integrations (aws, gcp, azure).
Not enabled: hosts (returns 403).
