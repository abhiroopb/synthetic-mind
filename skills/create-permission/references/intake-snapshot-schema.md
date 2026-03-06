# Intake Snapshot Schema

## Parsing the Intake Form

Ask: "Please paste the Notion URL for your approved intake form from the Permissions Working Group."

If the user hasn't submitted an intake form or doesn't have a URL, tell them: "This skill requires an approved intake form from the Permissions Working Group before proceeding with implementation. You can submit one at go/newpermission. Once it's been reviewed and approved, come back with the Notion URL and we'll get started." Do NOT proceed without it.

Once the user provides a Notion URL (any URL containing `notion.so` or `notion.site`):
- Use the Notion MCP `fetch` tool (or `notion-fetch`, depending on the client) to retrieve the page content.
- Parse the page content into the snapshot schema below. Look for:
  - Permission names (anything in SCREAMING_SNAKE_CASE or lowercase_snake_case that looks like a permission name)
  - Which components are needed (mentions of developer permission, employee permission, display permission, OAuth, Envoy SAFE, team permissions UI, employee_permission_mapping)
  - Context and motivation (why the permission is being created, what feature/project drives it, links)
  - Display permission details (group, access points, display name, description, feature flags, templates, backfill)
  - Mapping details (per-access-point employee enum mappings, SAFE mapping targets)
- After parsing, present the populated snapshot fields in a clear summary and ask the user to confirm: "Here's what I extracted from your intake form: [summary]. Does this look right? I'll ask about anything that wasn't covered."
- If the page can't be fetched (MCP not connected, page not accessible, etc.), tell the user: "I wasn't able to fetch that page — the Notion MCP may not be connected yet, or the page may not be accessible to the integration. Please paste the contents of your approved intake form directly and I'll work from that." Wait for them to paste the content before proceeding.

## Schema

When parsing the intake form, extract information into this canonical structure. Not all fields will be present in every intake — only populate what the form provides. This snapshot is the single source of truth that drives plan derivation, targeted Q&A, and execution.

```
request:
  summary: (why this permission is being created, what feature/project drives it)
  links: (Jira tickets, PRDs, design docs, Slack threads)
  owning_team: (team requesting the permission)

developer_permission:
  name: SCREAMING_SNAKE_CASE enum name
  description: short sentence for proto doc comment
  oauth:
    needed: yes/no
    display_group: DisplayGroup enum value
    methods: HTTP methods (GET, POST, etc.)
    status: ALPHA/BETA/PUBLIC
    version: Square API release train date
  safe_mapping:
    needed: yes/no
    employee_enum: name of employee enum to map under (new or existing)
    level: MERCHANT/UNIT/SELF

employee_permission:
  enums:
    - name: SCREAMING_SNAKE_CASE enum name
      description: short sentence for proto doc comment
    - name: (additional enum if per-access-point mapping requires different enums)
      description: ...

display_permission:
  id: lowercase_snake_case permission ID
  group: permission group name
  new_group: yes/no (if group doesn't exist yet)
  new_group_icon: Market icon name (only if new_group)
  new_group_position: ordering position (only if new_group)
  access_points: all_access_points / list of spos, mpos, dashboard
  parent_permission: parent permission ID or none
  type: regular/inherit_parent/full_access_only
  feature_flag: flag key or none
  display_name: seller-facing name
  description_text: longer description or none
  permission_set_templates: list of standard, enhanced or none
  backing: employee_enum / employee_enum_per_access_point / ui_only
  employee_permission_mapping:
    spos: employee_enum_name (lowercase)
    mpos: employee_enum_name (lowercase)
    dashboard: employee_enum_name (lowercase)

backfill:
  needed: yes/no
  type: all/conditional/none
  prerequisite_permission: permission ID (for conditional)
```

The `employee_permission_mapping` field is populated when different access points map to different employee enums. When all access points map to the same enum and the display permission ID matches the lowercased enum name, use the `employee_permission: true` shorthand instead. When the display permission ID differs from the enum name but all access points use the same enum, use `employee_permission_mapping` with the same enum for all access points.
