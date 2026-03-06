---
name: mode-settings-audit
description: Audits Mode Analytics workspace settings, permissions, data sources, and configurations. Use when asked to audit, review, inspect, or check Mode dashboard settings, access controls, or workspace configurations.
---

# Mode Settings Audit

Audits and reviews Mode Analytics workspace settings, permissions, data sources, and configurations.

## Capabilities

- Audit Mode workspace settings and configurations
- Review data source connections and credentials
- Check user permissions and access controls
- Inspect dashboard and report sharing settings
- Verify query execution policies and schedules
- Review organization-level security settings

## Workflow

1. **Identify scope**: Determine which Mode workspace or resources to audit
2. **Gather settings**: Use the Mode API to retrieve current configurations
3. **Analyze**: Compare settings against security best practices and organizational policies
4. **Report**: Present findings with recommendations

## Mode API Access

Use `sq curl` to interact with the Mode API:

```bash
# List workspaces
sq curl "https://app.mode.com/api/<org>/spaces"

# Get data sources
sq curl "https://app.mode.com/api/<org>/data_sources"

# Get workspace members
sq curl "https://app.mode.com/api/<org>/memberships"

# Get report details
sq curl "https://app.mode.com/api/<org>/reports/<report_token>"
```

## Audit Checklist

- [ ] Data source connections use service accounts (not personal credentials)
- [ ] Sharing settings follow least-privilege principle
- [ ] Scheduled queries have appropriate timeouts
- [ ] Sensitive dashboards are restricted to appropriate groups
- [ ] Unused data sources are identified for cleanup
- [ ] User permissions align with current team membership
