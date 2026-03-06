# Metric Query Workflow

Complete 7-step protocol for querying metrics from the Metric Store.

---

## Step 1: Parse User Question

Extract context from the user's question before searching:

- **Brand hints** — Look for mentions of specific product lines. If found, include in the `brand` parameter. Configure valid brands based on your organization's product lines.
- **Domain hints** — If the user mentions a specific business domain, note it for the `domains` parameter.
- **Keywords** — Break the question into comma-delimited search keywords (e.g., "What is mobile app revenue?" → `"revenue,mobile_app"`).

---

## Step 2: List Domains (if requested)

If the user asks to list available domains:

1. Call `mcp__mcp-metrics__list_available_domains`
2. Present domains to the user
3. Ask: "Would you like to see the available metrics for any of these domains?"
4. If yes → proceed to Step 3 with the specified domain(s)

---

## Step 3: List Metrics (if requested)

If the user asks to list available metrics:

1. First call `list_available_domains` to get all domains
2. Ask: "Before I show you all metrics, would you like to filter to any specific domains?"
3. Wait for response
4. Call `mcp__mcp-metrics__list_available_metrics` with or without `domains` parameter
5. Display ALL results in a table with columns: **Metric Name** | **Description**

---

## Step 4: Search Metrics

Call `mcp__mcp-metrics__metric_store_search` with:
- `search_text`: comma-delimited keywords
- `brand`: if detected in Step 1
- `domains`: if user specified or from prior conversation
- `cut_off`: `"0.5"` for baseline (use `"0.3"` for broader, `"0.6"` for exact)

### Interpret the response:

**If `use_block_metric_store` is `false`:**
- STOP — no matching metrics found
- Explain that no pre-built metrics match their request
- **DO NOT provide sample data or fabricated results**
- Present two options:
  1. "Submit a request for the metrics team to add this metric"
  2. "Search for dashboards that might contain this information"
- Wait for user to choose

**If `use_block_metric_store` is `true` AND `user_choice_required` is `true`:**
- Present `top_metrics` as a numbered list (1, 2, 3, etc.)
- Include which domain each metric belongs to
- Suggest which metric seems most relevant (without showing similarity scores)
- Say: "Which metric would you like to use? Please respond with the number. If none seem relevant, respond with 'none'."
- **STOP completely — do not call any other tools**
- Wait for user response
- If user says "none" → go to "No Metrics Found" flow above

**If `user_choice_required` is `false`:**
- Only one metric found — proceed directly to Step 5

---

## Step 5: Get Metric Details

Call `mcp__mcp-metrics__get_metric_details` with the selected metric name.

- **Always show governance level** to the user so they understand data reliability
- Show available dimensions
- Show available time grains
- If access is denied, use `check_permissions` to help the user get access to underlying tables

---

## Step 6: Validate Dimensions

**ALWAYS call `mcp__mcp-metrics__get_dimension_values` before applying filters.**

This step is mandatory when the user wants to filter data by any dimension:

1. Call `get_dimension_values` with the metric name and dimension name
2. Review the returned values — they are **case-sensitive** and must match exactly
3. If `filter_grep` is used and returns no results, try a broader pattern or call without `filter_grep` to see all values
4. **Never assume dimension values** from one metric apply to another metric, even if dimensions share the same name

### Important:
- Default date range: 1 month ago to yesterday
- Provide explicit `start_date` and `end_date` if the user needs a different range
- Values are returned for the specified date range — older data may have different values

---

## Step 7: Fetch Metric Data

Call `mcp__mcp-metrics__fetch_metric_data` with:

- `metric_name`: the selected metric
- `granularity`: time grain if requested (e.g., `"day"`, `"month"`)
- `start_date` / `end_date`: ISO format (`YYYY-MM-DD`). Defaults to 1 month ago → yesterday if not specified. Both inclusive.
- `dimensions`: list of dimensions to group by
- `filters`: structured filters using validated dimension values from Step 6
- `sort_by`: optional sorting (string, list, or list of `{column: direction}` dicts)
- `limit`: defaults to 1000

### Filter format examples:
```json
{"country": "US"}
{"revenue": {"operator": ">", "value": 1000}}
{"categories": ["Electronics", "Books"]}
```

### Present results:
- Show data in a clear table format
- Include the date range used
- Include the Snowflake query link if provided
- Include the validation source link if provided

---

## No Metrics Found Fallback

When `use_block_metric_store` is `false` OR the user responds "none" to metric choices:

1. **STOP** — explain no pre-built metrics match. **Do not fabricate data.**
2. Present two options:
   - **Option 1**: "Submit a request for the metrics team to add this metric"
   - **Option 2**: "Search for dashboards that might contain this information"
3. Wait for user selection

### If Option 1 (Submit request):
1. Ask for metric description, optional SQL query, optional documentation
2. Draft the feedback and show to user for review
3. **Only call `submit_feedback` after explicit user confirmation**

### If Option 2 (Dashboard search):
- Call `mcp__mcp-metrics__dashboard_search` with original search terms
- Follow the [Dashboard Workflow](dashboard-workflow.md)
