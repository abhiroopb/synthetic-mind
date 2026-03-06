---
name: looker
description: "Interact with Looker dashboards, tiles, queries, looks, explores, folders, and models via the Looker Python SDK. Use when given a Looker URL (square.cloud.looker.com), dashboard/look ID, explore qid, or asked to search, run, or update Looker content."
metadata:
  author: ccroom
  version: "0.0.1"
  status: experimental
---

# Looker

Query and manage Looker content via a Python CLI wrapping the Looker SDK.

## Prerequisites

- **WARP VPN** must be connected
- **Auth** (checked in order):
  1. `LOOKERSDK_CLIENT_ID` + `LOOKERSDK_CLIENT_SECRET` env vars
  2. OAuth token in macOS Keychain (run `login` to authenticate)
- If neither is configured, read [SETUP.md](./SETUP.md) and walk the user through setup.

## Invocation

All commands use this prefix (shown as `$LC` in examples):

```bash
LC="uvx --with looker-sdk --with requests python {{SKILL_DIR}}/scripts/looker_cli.py"
$LC <command> [options]
```

## Conventions

- **`--full`**: Read/list commands default to compact output. Pass `--full` for complete API objects. Supported by: `get`, `list-elements`, `list-models`, `list-filters`, `list-layouts`, `describe-explore`.
- **`--limit N`**: Max rows returned (default 50 for queries, 20 for searches).
- **`--format`**: `json` (default), `csv`, or `txt`. Supported by: `run-query`, `run-query-id`, `run-explore`.
- **IDs and URLs**: Commands accept numeric IDs. `get-folder` also accepts full Looker URLs.
- **Output**: JSON to stdout. Pipe to `jq` for extraction (e.g., `$LC list-elements 123 | jq '.[].title'`).
- **URL patterns**: Dashboard `.../dashboards/<id>` | Explore `.../explore/<model>/<view>?qid=<slug>` | Folder `.../folders/<id>`

## Safety

- **Destructive operations**: Always ask the user for explicit confirmation before running `delete-element`, `delete-look`, or any delete that affects multiple items. Be especially cautious with actions that could delete an entire dashboard or folder.
- **Prefer copy-then-replace**: When modifying dashboards or looks, prefer creating a copy first (e.g., clone tiles to a new dashboard) and letting the user verify before replacing the original. This avoids irreversible changes to shared content.
- **Updates**: Confirm intent before `update-*` commands on content the user did not create.

## Commands

### Auth

```bash
$LC login     # Authenticate via browser (OAuth PKCE)
$LC me        # Verify authentication
```

### Discovery

```bash
$LC list-models
$LC describe-explore --model Square --view fact_pull_requests
$LC describe-explore --model Square --view fact_pull_requests --filter author
$LC describe-explore --model Square --view fact_pull_requests --names-only
```

Auto-summarizes explores with >100 fields unless `--filter` or `--full` is used. Add `--include-joins` for join metadata.

### Search

```bash
$LC search-content "quarterly revenue"             # cross-type: dashboards + looks + folders
$LC search --title "My Dashboard" --limit 50       # dashboards only
$LC search-looks --title "Monthly Active Users"    # looks only
```

### Folders

```bash
$LC get-folder 123
$LC get-folder "https://square.cloud.looker.com/folders/123"
```

### Dashboards

```bash
$LC get <dashboard_id>
$LC update <dashboard_id> --title "New Title" --description "Updated"
```

### Running Queries

```bash
# Run all tiles in a dashboard concurrently (default 50 rows/tile)
$LC run-dashboard <dashboard_id>
$LC run-dashboard <dashboard_id> --tile "Revenue by Region"   # filter by title substring or element ID

# By slug (the qid from Explore URLs)
$LC run-query <slug> --limit 50

# By query ID
$LC run-query-id <query_id>

# Run a look
$LC run-look <look_id>

# Ad-hoc explore query
$LC run-explore --model Square --view fact_pull_requests \
  --fields "fact_pull_requests.total_prs,people_hierarchy.manager" \
  --filters "fact_pull_requests.created_at_date=this year to second" \
  --sorts "fact_pull_requests.total_prs desc" --limit 50

# Pivot query (crosstab)
$LC run-explore --model Square --view fact_pull_requests \
  --fields "fact_pull_requests.total_prs,people_hierarchy.manager,fact_pull_requests.created_month" \
  --pivots "fact_pull_requests.created_month" --limit 50
```

`--filters` uses `key=value` format with Looker filter expression syntax for values.

### Tiles (Elements)

```bash
$LC list-elements <dashboard_id>
$LC get-element <element_id>
$LC get-query <element_id>                  # inspect the query behind a tile
$LC update-element <element_id> --title "New Tile Title"
$LC delete-element <element_id>
$LC create-element <dashboard_id> --type vis --title "My Tile" --query-id <query_id>
```

### Clone & Modify Tiles

Clone a tile, optionally modifying its `filter_expression`. Uses `|||` (triple pipe) as the find/replace delimiter.

```bash
$LC clone-element <source_element_id> --title "H1 OKR %" \
  --filter-replace '`1 quarter`|||`2026/01/01 to 2026/07/01`'
$LC clone-element <source_id> --title "Copied Tile" --dashboard-id <target_id>
```

### Looks

```bash
$LC get-look <look_id>
$LC run-look <look_id> --limit 50
$LC create-look --title "Weekly Active Users" --query-id <query_id>
$LC update-look <look_id> --title "Updated Title"
$LC delete-look <look_id>
```

### Queries

```bash
$LC query-by-slug <slug>                     # inspect query definition from explore qid
$LC create-query --file query_spec.json      # create from JSON spec
$LC create-query --file query_spec.json --run  # create and execute (prints results only)
```

### Filters & Layouts

```bash
$LC list-filters <dashboard_id>
$LC update-filter <filter_id> --default-value "last 30 days"
$LC list-layouts <dashboard_id>
```

## Workflows

### Discover Available Data (Explore-First Pattern)

**Always use `describe-explore` before constructing `run-explore` queries.** Field names must be fully qualified (e.g., `fact_pull_requests.total_prs`, not `total_prs`).

1. `list-models` to find available LookML models
2. `describe-explore --model X --view Y --filter keyword` to find exact field names
3. `run-explore --model X --view Y --fields "view.field_name,..." --limit 50`

### Clone a Tile with Modified Query

1. `list-elements <dashboard_id>` to find the source element ID
2. `get-query <element_id>` to inspect the filter_expression
3. `clone-element <element_id> --title "New Title" --filter-replace 'old|||new'`

### Run a Query from an Explore URL

Extract the `qid` parameter from the URL, then: `run-query <qid> --limit 50`

### Permissions

```bash
# Check why you can't access a Looker URL (uses Bellhop)
$LC security-lookup "https://square.cloud.looker.com/dashboards/12345"
```

Returns `permissions_granted`, `missing_permissions`, and `recommendations`. Use this when any command returns a 403/404 that might be a permissions issue.

## Troubleshooting

| Issue | Solution |
|-------|---------|
| Auth failure / 401 | Run `$LC login` to re-authenticate |
| Connection timeout | Check WARP VPN is connected |
| Permission denied | Run `$LC security-lookup <url>` to check access |
| `uvx` not found | `brew install uv` |
