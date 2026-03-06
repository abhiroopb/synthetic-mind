---
name: people-api
description: "Query employee data from the People API at my.sqprod.co. Search, look up, list, or browse people by name, username, LDAP, Slack ID, function, or org. Use when asked to find someone, check employee info, resolve a username, query org charts, or map teams."
roles: [frontend]
metadata:
  author: ccroom
  version: "1.0"
  status: stable
---

# People API Skill

Query employee data from Block's internal People API (my.sqprod.co), powered by the [Go Rails application](https://github.com/squareup/go).

## Authentication

If `PEOPLE_API_TOKEN` is set, always include the header: `Authorization: Token $PEOPLE_API_TOKEN`. See `SETUP.md` for how to obtain a token.

Most endpoints also work without a token (WARP network access is sufficient), but using a token is recommended for reliability.

Use **List** (`/people/api/all.json`) for bulk export, incremental sync via `since`, or when you need fields like `github`, `slack_id`, `job_family`, or `start_date`. Use **Search** (`/api/people/search.json`) to filter by function or org hierarchy. Use **Get Person Details** for full profile lookups by username/LDAP, and **Slack Employee Lookup** to map a Slack ID to a person.

## Endpoints

Base URL: `https://my.sqprod.co`

### List People

```
GET /people/api/all.json?query=Charl&page=1&sort=username&dir=asc&since=2026-01-01
```

Paginated directory of all employees (500/page). All params are optional.

- `query` - prefix match on first name, last name, or username (min 2 chars)
- `page` - 1-indexed page number
- `since` - ISO date, only employees created/updated after this date
- `sort` - `username` or `started_at` (default)
- `dir` - `asc` (default) or `desc`

Pagination info is in response headers: `X-Page`, `X-Per-Page`, `X-Pages`, `X-Count`.

**Response fields:** `username`, `email`, `preferred_first_name`, `last_name`, `lead` (manager's username), `start_date`, `job_family`, `tech_lead`, `city`, `country_code`, `business_unit`, `slack_username`, `slack_id`, `github`, `twitter`, `cashtag`, `phone_mobile`, `personal_pronoun`, `contingent` (contractor flag), `discipline`, `abstraction`, `additional_role_info`, `primary_photo`, `authoritative_photo`, `org_chart_nodes`.

### Search People (with function/org filtering)

```
GET /api/people/search.json?function_l3=Web+Engineering&include_lead=true
```

Supports filtering by function and org hierarchy. Do NOT pass `initializeBlank=true` with hierarchy filters.

- `query` - text search on name/username (min 3 chars; optional when hierarchy filters are set)
- `function_l1` / `function_l2` / `function_l3` - filter by function level (e.g., "Engineering", "Product Engineering", "Web Engineering")
- `org_l1` / `org_l2` / `org_l3` - filter by org level
- `include_lead` - set to `true` to include lead details as a nested object

**Response:** `{"results": [...]}` with fields: `username`, `preferred_full_name`, `preferred_name`, `email`, `city`, `function_l1`/`l2`/`l3`, `org_l1`/`l2`/`l3`, `organization_id`, `organization_name`, `is_lead`, `out_of_office`, `talk_to_me_about`, `my_supervisory_orgs`, and optionally `lead` (nested object with username/name/photo).

### Get Person Details

```
GET /people/api/p/:username.json
```

Returns everything from the list endpoint plus: `bio`, `linkedin`, `timezone`, `cost_center`, `workday_id`, `manager` (boolean), `business_unit_name`, `preferred_pronunciation`, `phone_desk`, `phone_desk_extension`, `org_l1`/`org_l2`/`org_l3`, `function_l1`/`function_l2`/`function_l3` (e.g., "Engineering" / "Engineering Tech Lead" / "Web Tech Lead"), `photos`, `photos_accessible`, `executive_assistants`.

### Get Person's Lead

```
GET /people/api/p/:username/show_lead.json
```

Returns the full detail profile of the person's manager.

### Slack Employee Lookup

```
GET /api/slack_employee/:slack_id.json
```

Maps a Slack user ID to an employee record.

### Teams / Organizations

```
GET /people/api/teams.json
```

Returns a hierarchical tree. Each node: `name`, `reference_id`, `children` (nested).

### Org Chart Nodes

```
GET /people/api/org_chart_nodes.json?type=LEADERSHIP&page=1&parent_id=abc123
```

- `type` - `LEADERSHIP`, `INDIVIDUAL_CONTRIBUTOR`, or `ALL` (default)
- `parent_id` - filter to nodes whose parent matches this org node ID (use to get a manager's direct reports)
- `page` - paginated

Response fields: `name`, `id`, `parent_id`, `node_type`, `employee_username`, `sub_team_or_sub_function`, `wd_reference_id`, `slack_channel`, `slack_channel_url`, `google_group`, `office_hours`, `preferred_contact_method`.

### Direct Reports & Sub-Teams

To get a manager's direct reports with sub-team assignments:

1. Get the manager's org node ID from their profile (`org_chart_nodes[].id` on the detail or list endpoint)
2. Pass it as `parent_id` to `org_chart_nodes`
3. Group results by `sub_team_or_sub_function` for sub-team membership

The `sub_team_or_sub_function` field contains the custom sub-team label set by the manager in the org chart UI (e.g., "UI Stewards", "E2E"). It is `null` for ungrouped ICs.

See `references/direct-reports-with-subteams.md` for a working example.

### Photo URL

```
GET /people/api/p/:username/photos/url/:size
```

Redirects to photo. Sizes: `profile_main`, `profile_small`, `search_results`.

## Examples

See `references/` for working examples:
- `search-by-name.md` - Use when searching for a person by partial name
- `github-lookup-by-ldap.md` - Use when resolving an LDAP username to a GitHub handle
- `find-engineers-with-managers.md` - Use when listing engineers in a function with their managers
- `new-hires-since-date.md` - Use when finding employees who joined after a specific date
- `direct-reports-with-subteams.md` - Use when fetching a manager's direct reports grouped by sub-teams

## Tips

1. **Pagination**: List endpoint returns 500/page, ~27 pages total. Use `X-Pages` header to know when to stop.
2. **Photo URLs expire**: S3 URLs from the list endpoint expire after 1 hour. Use `/photos/url/:size` for stable redirects.
3. **Server-side caching**: The list endpoint is cached 12 hours server-side.
4. **Profile page**: `https://my.sqprod.co/profile/:username`
