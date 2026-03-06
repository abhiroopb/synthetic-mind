# Dashboard Workflow

Complete protocol for searching and executing Looker and Mode dashboards.

---

## Step 1: Search Dashboards

Call `mcp__mcp-metrics__dashboard_search` with:
- `search_text`: user's search query
- `cut_off`: `"0.5"` baseline (adjust as needed)
- `source`: optional filter (`"looker"`, `"mode"`, or `"tableau"`)

### Present results as a numbered list:
```
1. [Dashboard Name] — [Platform] — [URL]
   Description: ...
2. [Dashboard Name] — [Platform] — [URL]
   Description: ...
```

If no results found, suggest broadening the search with a lower `cut_off` value (`"0.3"`).

---

## Step 2: Get Dashboard Metadata

When the user selects a dashboard, call `mcp__mcp-metrics__run_dashboard` with:
- `dashboard_id`: the selected dashboard's ID
- `platform`: `"looker"` or `"mode"`
- **Do NOT include `query_ids`** — this returns metadata only

This returns:
- Dashboard name
- Available filters (with defaults and format hints for Looker)
- Dashboard elements (tiles/queries) with their titles and query IDs

### Present the elements to the user:
```
Dashboard: [Name]

Available elements:
1. [Element Title] (query_id: abc123)
2. [Element Title] (query_id: def456)
3. [Element Title] (query_id: ghi789)

Which elements would you like me to execute? (or "all")
```

---

## Step 3: Ask User Which Elements to Execute

**STOP and wait for user response.** Do NOT execute all elements by default.

- Query execution can produce very large results or be long-running
- Let the user choose specific elements they need
- If the user says "all", proceed with all query IDs

---

## Step 4: Execute Selected Queries

Call `mcp__mcp-metrics__run_dashboard` again with:
- `dashboard_id`: same dashboard
- `platform`: same platform
- `query_ids`: list of selected query IDs
- `filters`: optional filter overrides (Looker only)

### Present results:
- Show data from each executed element
- If results are very large, summarize and recommend the user view the dashboard directly in their browser

---

## Looker Filter Handling

Looker dashboards may have default filter values. When filters are returned in metadata:

1. **Show the user the default filter values** and their formats
2. **Ask if they want to override any filters** before executing queries
3. To clear a default filter and show all values, set it to empty string (`""`)
4. Apply filter overrides in the `filters` parameter of the execution call

### Filter format example:
```json
{
  "Date Range": "last 30 days",
  "AE Manager": "Allan Manuel"
}
```

---

## Mode Dashboard Notes

- Mode dashboards use report tokens as dashboard IDs
- Filters work differently from Looker — follow the format returned in metadata
- Some Mode dashboards may have long-running queries — warn the user if execution takes too long
