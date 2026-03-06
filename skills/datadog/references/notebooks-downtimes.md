# Notebooks, Downtimes & Integrations

Reference for querying Datadog Notebooks, Downtimes, and Integrations via the API proxy.

```
BASE_URL=https://<dd-api-proxy-url>/datadog
```

## Notebooks

### List Notebooks

```bash
curl -s "$BASE_URL/api/v1/notebooks?count=10" \
  | jq '[.data[] | {id: .id, name: .attributes.name, author: .attributes.author.handle, modified: .attributes.modified}]'
```

Search by keyword, filter by type, and control cell inclusion:

```bash
# Search by keyword (paginate with start offset)
curl -s "$BASE_URL/api/v1/notebooks?count=10&query=incident" \
  | jq '[.data[] | {id: .id, name: .attributes.name}]'

# Filter by type (e.g., investigation, postmortem)
curl -s "$BASE_URL/api/v1/notebooks?count=10&type=investigation" \
  | jq '[.data[] | {id: .id, name: .attributes.name}]'

# Include cell content in listing (default excludes cells for smaller responses)
curl -s "$BASE_URL/api/v1/notebooks?count=5&include_cells=true" \
  | jq '[.data[] | {id: .id, name: .attributes.name, cells: (.attributes.cells | length)}]'
```

### Get Notebook by ID

```bash
curl -s "$BASE_URL/api/v1/notebooks/123456" \
  | jq '{id: .data.id, name: .data.attributes.name, cells: [.data.attributes.cells[] | {type: .attributes.definition.type, text: .attributes.definition.text}]}'
```

URL: `https://<your-datadog-instance>.datadoghq.com/notebook/<notebook_id>`

## Downtimes

### List Active Downtimes

```bash
curl -s "$BASE_URL/api/v2/downtime" \
  | jq '[.data[] | {id: .id, scope: .attributes.scope, status: .attributes.status, start: .attributes.schedule.start, end: .attributes.schedule.end}]'
```

### List Downtimes for a Monitor

```bash
curl -s "$BASE_URL/api/v2/downtime?filter%5Bmonitor_id%5D=12345678" \
  | jq '[.data[] | {id: .id, scope: .attributes.scope, status: .attributes.status}]'
```

### Get / Cancel Downtime

```bash
curl -s "$BASE_URL/api/v2/downtime/abc-123" | jq '.data.attributes'
curl -s -X DELETE "$BASE_URL/api/v2/downtime/abc-123"  # 204 on success
```

## Integrations

Supported types: `aws`, `gcp`, `azure` (proxy-enabled). Other types (`pagerduty`, `slack`) may work if proxy scope allows.

### List AWS Integrations

```bash
curl -s "$BASE_URL/api/v1/integration/aws" \
  | jq '[.accounts[] | {account_id: .account_id, role_name: .role_name, host_tags: .host_tags, filter_tags: .filter_tags}]'
```

### List GCP Integrations

```bash
curl -s "$BASE_URL/api/v1/integration/gcp" \
  | jq '[.[] | {project_id: .project_id, host_filters: .host_filters}]'
```

### List Azure Integrations

```bash
curl -s "$BASE_URL/api/v1/integration/azure" \
  | jq '[.[] | {tenant_name: .tenant_name, client_id: .client_id, host_filters: .host_filters}]'
```
