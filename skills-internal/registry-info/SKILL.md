---
name: registry-info
description: Query application metadata from a service registry. Use when you need to find service information, dependencies, deployment details, ownership, or links to documentation/monitoring.
roles: [frontend]
allowed-tools: Bash(cli app:*)
---

# Service Registry Information Skill

Query a service registry to discover application metadata, dependencies, deployment information, and operational details.

## What is the Service Registry?

The service registry is a central catalog of all applications and services. It stores:
- Application metadata (description, ownership, contact info)
- Deployment information (datacenters, endpoints, nodes)
- Dependency relationships
- Links to operational resources (Slack, issue tracker, runbooks, dashboards)
- Git repository information

## Command Overview

All registry queries use the `cli app` command.

```bash
# List applications
cli app list

# Get app details
cli app describe <appname>
cli app show <appname>

# Find dependencies
cli app dependencies <appname>
cli app dependents <appname>

# Get operational info
cli app endpoints <appname> <staging|production>
cli app dcs <appname>
cli app nodes <appname>
cli app slack <appname>

# Extract specific fields
cli app field <appname> <field>
cli app raw <appname>

# Find apps you own
cli app owned

# Detect current app
cli app which
```

## Common Use Cases

### 1. Find Application Information

```bash
cli app describe my-service
```

Returns: name, description, git repo, Slack channel, issue tracker project, dashboard, runbook, registry link.

### 2. Check Deployment Status

```bash
cli app endpoints my-service production
cli app dcs my-service
```

### 3. Understand Dependencies

```bash
cli app dependencies my-service
cli app dependents my-service
```

### 4. Contact the Right Team

```bash
cli app slack my-service
cli app field my-service contact
cli app owned
```

### 5. Get Operational Links

```bash
cli app field my-service datadog_dashboard
cli app field my-service runbook
cli app field my-service jira_project
cli app field my-service pagerduty_schedule
```

### 6. Find Git Repository

```bash
cli app field my-service git_repo
cli app which
```

### 7. Extract Raw Data

```bash
cli app raw my-service | jq .
```

## Available Fields

Use `cli app field <appname> <field>` to extract specific fields:

| Field | Description |
|-------|-------------|
| `name` | Application name |
| `description` | Short description |
| `git_repo` | GitHub repository URL |
| `git_repo_path` | Subdirectory path in monorepo |
| `slack_channel` | Primary Slack channel |
| `contact` | Team email |
| `jira_project` | Issue tracker project key |
| `datadog_dashboard` | Monitoring dashboard URL |
| `runbook` | Runbook URL |
| `pagerduty_schedule` | On-call schedule URL |
| `documentation` | Documentation URL |
| `team_id` | Owning team ID |
| `reliability_tier` | Service tier (1-4) |
| `data_safety_level_rating` | Data sensitivity (1-5) |
| `application_type` | Type (service, library, etc.) |
| `production_service` | Boolean if in production |

## Tips and Best Practices

1. **Start with `describe`**: Always start with `cli app describe <appname>` to get a comprehensive overview
2. **Check dependencies before changes**: Run `cli app dependents <appname>` before making breaking changes
3. **Use `raw` for scripting**: The `cli app raw <appname>` output is JSON and perfect for automation
4. **Find apps from git repos**: Use `cli app which` in any repo to detect the associated registry app
5. **List vs Search**: `cli app list` returns ALL apps. Use grep to filter.

## Troubleshooting

**"failed to parse id" error**: The app name may not exist. Use `cli app list | grep <name>` to search.

**Empty output for `nodes` or `dcs`**: The app may not be deployed, or you may need to check `endpoints` instead.

**Some fields return null**: They may need to be requested using `--full`.

## Related Skills

- **registry-api**: Query the registry using the Python client library (more endpoints, full API access)
