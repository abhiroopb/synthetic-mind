---
name: business-metrics
description: Query business metrics, dashboards, and permissions via the Metric Store. Use when asked about business KPIs, revenue, GPV, active users, transaction volumes, or other company metrics. Also handles Looker and Mode dashboard discovery, execution, and permission checks for underlying data tables.
metadata:
  author: anonymous
  version: "0.1.0"
  status: experimental
---

# Business Metrics Skill

Query trusted business metrics and dashboards through the `mcp_metrics` MCP server.

## Prerequisites

See [SETUP.md](./SETUP.md) for MCP server installation and authentication instructions.

**Quick check** — verify the server is connected by looking for `mcp__mcp-metrics__metric_store_search` in your tool list. If missing, follow the [dependency check protocol](references/dependency-check.md).

---

## Examples

When the user asks about business metrics, use the **Metric Workflow** below:
- "What's our GPV?" → search for GPV metrics, get details, fetch data
- "Show me mobile app active users last quarter" → search with brand=mobile_app, validate dimensions, fetch with date range
- "What metrics are available for revenue?" → use `metric_store_search` with keywords
- "List all metric domains" → call `list_available_domains`

When the user asks about dashboards, use the **Dashboard Workflow** below:
- "Find dashboards about GPV" → search dashboards, present results with URLs
- "Run this Looker dashboard" → get metadata first, ask which elements to execute
- "Summarize dashboard 25648" → run metadata, let user pick elements, execute selected

When the user asks about data access:
- "Check my permissions for this table" → call `check_permissions`, provide access request URLs
- "I can't access this metric" → check permissions, guide to access request

---

## Available Tools

| Tool | Purpose |
|------|---------|
| `mcp__mcp-metrics__metric_store_search` | Search for metrics by keywords, brand, and domain |
| `mcp__mcp-metrics__list_available_domains` | List all metric domains |
| `mcp__mcp-metrics__list_available_metrics` | List metrics, optionally filtered by domain |
| `mcp__mcp-metrics__get_metric_details` | Get metric definition, dimensions, governance level |
| `mcp__mcp-metrics__get_dimension_values` | Get valid values for a metric dimension |
| `mcp__mcp-metrics__fetch_metric_data` | Fetch metric data with filters, date ranges, sorting |
| `mcp__mcp-metrics__dashboard_search` | Search for Looker, Mode, and Tableau dashboards |
| `mcp__mcp-metrics__run_dashboard` | Execute dashboard queries and retrieve data |
| `mcp__mcp-metrics__check_permissions` | Check table access and get access request URLs |
| `mcp__mcp-metrics__submit_feedback` | Submit metric requests, issues, or ratings |

---

## Metric Workflow

High-level flow: **Search → Choose → Details → Validate Dimensions → Fetch**

1. **Search** — Use `metric_store_search` with extracted brand and domain hints
2. **Choose** — If `user_choice_required` is true, present options and **STOP — wait for user**
3. **Details** — Call `get_metric_details` to show governance level and dimensions
4. **Validate** — **ALWAYS** call `get_dimension_values` before applying any filters
5. **Fetch** — Use `fetch_metric_data` with structured filters and date range

### Critical Rules

- **Never guess metric names** — always search first
- **STOP on `user_choice_required: true`** — present numbered options, wait for user to choose
- **STOP when `use_block_metric_store: false`** — go to "No Metrics Found" flow (offer feedback submission or dashboard search)
- **Always validate dimensions** before filtering — dimension values are case-sensitive and metric-specific
- **Connection errors** — STOP immediately, do not fabricate data

**See:** [`references/metric-query-workflow.md`](references/metric-query-workflow.md) for the full 7-step protocol

---

## Dashboard Workflow

High-level flow: **Search → Metadata → Ask User → Execute Selected**

1. **Search** — Use `dashboard_search` to find dashboards; present as numbered list with platform and URL
2. **Metadata** — Call `run_dashboard` without `query_ids` to get dashboard elements and filters
3. **Ask user** — **STOP** and ask which elements to execute (do NOT execute all by default)
4. **Execute** — Call `run_dashboard` again with selected `query_ids` and optional filters

**See:** [`references/dashboard-workflow.md`](references/dashboard-workflow.md) for complete protocol including Looker filter handling

---

## Error Handling

- **Connection errors** (`connection_error: true`) — STOP immediately. Inform user of connectivity issue. Do not retry or fabricate data.
- **Permission / access errors** — Use `check_permissions` with the metric's source tables to get access request URLs.
- **No metrics found** — Offer two options: (1) submit a metric request via `submit_feedback`, or (2) fall back to `dashboard_search`.

---

## Conventions

- **Filter operators**: `=`, `!=`, `>`, `<`, `>=`, `<=`, `IN`, `NOT IN`, `LIKE`, `ILIKE`, `IS NULL`, `IS NOT NULL`
- **Date format**: ISO 8601 (`YYYY-MM-DD`). Defaults: start = 1 month ago, end = yesterday. Both inclusive.
- **Valid brands**: configure based on your organization's product lines
- **Domains parameter**: comma-separated string (e.g., `"domain_1,domain_2"`)
- **Governance levels**: shown in `get_metric_details` — always surface to user so they understand data reliability
- **Search keywords**: use comma-delimited keywords (e.g., `"revenue,monthly,product_name"`)

---

## Reference Files

- [`SETUP.md`](./SETUP.md) — Installation and authentication setup
- [`references/dependency-check.md`](references/dependency-check.md) — Runtime server detection and auto-install protocol
- [`references/metric-query-workflow.md`](references/metric-query-workflow.md) — Full 7-step metric query protocol
- [`references/dashboard-workflow.md`](references/dashboard-workflow.md) — Dashboard search and execution protocol
