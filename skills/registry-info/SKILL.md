---
name: registry-info
description: Query application metadata from Square's Registry. Use when you need to find service information, dependencies, deployment details, ownership, or links to documentation/monitoring.
roles: [frontend]
allowed-tools: Bash(sq app:*)
---

# Registry Information Skill

Query Square's Registry to discover application metadata, dependencies, deployment information, and operational details.

## What is Registry?

Registry is Square's central catalog of all applications and services. It stores:
- Application metadata (description, ownership, contact info)
- Deployment information (datacenters, endpoints, nodes)
- Dependency relationships
- Links to operational resources (Slack, Jira, runbooks, dashboards)
- Git repository information

## Command Overview

All Registry queries use the `sq app` command.

```bash
# List applications
sq app list

# Get app details
sq app describe <appname>
sq app show <appname>

# Find dependencies
sq app dependencies <appname>
sq app dependents <appname>

# Get operational info
sq app endpoints <appname> <staging|production>
sq app dcs <appname>
sq app nodes <appname>
sq app slack <appname>

# Extract specific fields
sq app field <appname> <field>
sq app raw <appname>

# Find apps you own
sq app owned

# Detect current app
sq app which
```

## Common Use Cases

### 1. Find Application Information

Get a high-level overview of any service:

```bash
sq app describe sales-eg
```

Returns: name, description, git repo, Slack channel, Jira project, Datadog dashboard, runbook, Registry link.

### 2. Check Deployment Status

See where an app is deployed and get pod/node information:

```bash
# Get deployment endpoints
sq app endpoints sales-eg production

# Get datacenters
sq app dcs sales-eg

# Get node information (deprecated, use endpoints)
sq app nodes sales-eg
```

The `endpoints` command shows:
- Environment (production, sandbox, staging)
- Region (us-east-1, us-west-2, etc.)
- Target groups
- Individual pod names

### 3. Understand Dependencies

Find what an app depends on or what depends on it:

```bash
# What does sales-eg depend on?
sq app dependencies sales-eg

# What depends on sales-eg?
sq app dependents sales-eg
```

This is critical for:
- Impact analysis before making changes
- Understanding data flow
- Finding downstream consumers

### 4. Contact the Right Team

Find the team that owns a service:

```bash
# Get Slack channel
sq app slack sales-eg
# Output: sales-data-platform-team

# Get full contact info
sq app field sales-eg contact
# Output: sales-data-platform@squareup.com

# Find all your apps
sq app owned
```

### 5. Get Operational Links

Access monitoring and documentation:

```bash
# Get Datadog dashboard
sq app field sales-eg datadog_dashboard

# Get runbook
sq app field sales-eg runbook

# Get Jira project
sq app field sales-eg jira_project

# Get PagerDuty schedule
sq app field sales-eg pagerduty_schedule
```

### 6. Find Git Repository

Locate the source code:

```bash
sq app field sales-eg git_repo
# Output: https://github.com/squareup/tf-sales-eg

# Detect app from current directory
sq app which
```

### 7. Extract Raw Data

Get complete Registry data as JSON:

```bash
sq app raw sales-eg | jq .
```

This returns all fields including:
- `application_type`
- `cost_center_id`
- `data_safety_level_rating`
- `reliability_tier`
- `team_id`
- And more...

## Available Fields

Use `sq app field <appname> <field>` to extract specific fields:

| Field | Description |
|-------|-------------|
| `name` | Application name |
| `description` | Short description |
| `git_repo` | GitHub repository URL |
| `git_repo_path` | Subdirectory path in monorepo |
| `slack_channel` | Primary Slack channel |
| `contact` | Team email |
| `jira_project` | Jira project key |
| `datadog_dashboard` | Datadog dashboard URL |
| `runbook` | Runbook URL |
| `pagerduty_schedule` | PagerDuty schedule URL |
| `documentation` | Documentation URL |
| `team_id` | Owning team ID |
| `reliability_tier` | Service tier (1-4) |
| `data_safety_level_rating` | Data sensitivity (1-5) |
| `application_type` | Type (service, library, etc.) |
| `production_service` | Boolean if in production |

## Examples

### Example 1: Debugging a Service Issue

You're investigating slow queries in sales-eg:

```bash
# Get the Slack channel to ask questions
sq app slack sales-eg
# sales-data-platform-team

# Get the runbook for troubleshooting steps
sq app field sales-eg runbook
# https://www.notion.so/square-seller/Sales-Graph-Runbook-...

# Find what depends on it to assess impact
sq app dependents sales-eg
# Lists 30 services including beemoreporter, cp-reporting, etc.

# Get production endpoints to check pod health
sq app endpoints sales-eg production
# Shows pods in us-east-1 and us-west-2
```

### Example 2: Planning a Migration

You need to update sales-eg's API:

```bash
# Find all consumers
sq app dependents sales-eg

# For each dependent, get their team
sq app slack beemoreporter
sq app slack cp-reporting
# ... etc

# Check deployment regions to coordinate rollout
sq app endpoints sales-eg production
```

### Example 3: Onboarding to a Service

You're new to a service:

```bash
# Get overview
sq app describe payment-reporter

# Find the code
sq app field payment-reporter git_repo

# Find documentation
sq app field payment-reporter documentation

# Join the Slack channel
sq app slack payment-reporter

# Understand dependencies
sq app dependencies payment-reporter
```

### Example 4: Finding Apps by Team

```bash
# List all apps you own
sq app owned

# Search for apps (using grep)
sq app list | grep -i payment
```

## Tips and Best Practices

1. **Start with `describe`**: Always start with `sq app describe <appname>` to get a comprehensive overview

2. **Check dependencies before changes**: Run `sq app dependents <appname>` before making breaking changes

3. **Use `raw` for scripting**: The `sq app raw <appname>` output is JSON and perfect for automation:
   ```bash
   sq app raw sales-eg | jq -r '.slack_channel'
   ```

4. **Find apps from git repos**: Use `sq app which` in any repo to detect the associated Registry app

5. **Combine with other tools**: Registry data pairs well with other debugging tools:
   ```bash
   # Get Slack channel and join it
   open "slack://channel?team=T0259RXRY&id=$(sq app slack sales-eg)"

   # Get Datadog dashboard and open it
   sq app field sales-eg datadog_dashboard | xargs open
   ```

6. **List vs Search**: `sq app list` returns ALL apps (thousands). Use grep to filter:
   ```bash
   sq app list | grep -i "my-service"
   ```

## Troubleshooting

**"failed to parse id" error**: The app name may not exist or you may be using the wrong command. Use `sq app list | grep <name>` to search.

**Empty output for `nodes` or `dcs`**: The app may not be deployed, or you may need to check `endpoints` instead.

**"No apps found in Registry where git_repo..."**: The current directory is not associated with a Registry app. This is normal for non-deployed services or local tools.

**Some fields return null even though they are available on registry UI**: They may need to be requested using --full.

```
sq app field --full sales-eg reliability_tier
```

## Related Skills

- **opensearch-kibana**: Query OpenSearch cluster health for ElasticGraph services
- **elasticgraph-query**: Query ElasticGraph data (like sales-eg, orders-data)
- **presidio-logs**: Search application logs
- **rpc-admin-console**: Call RPC methods on services

## Support

For Registry issues or questions:
- Ask in **#deploy**
- Registry docs: https://go/registry
- Source: https://github.com/squareup/registry
