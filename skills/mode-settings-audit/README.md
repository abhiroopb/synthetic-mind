# Mode Settings Audit

> Audit Mode Analytics workspace settings, permissions, data sources, and configurations.

## What it does

Mode Settings Audit reviews and analyzes Mode Analytics workspace configurations against security best practices. It checks data source connections, user permissions, sharing settings, query execution policies, and organization-level security. The skill retrieves current settings via the Mode API, compares them against recommended policies, and produces a findings report with actionable recommendations.

## Usage

Use this skill when you need to review or verify Mode Analytics configurations, especially during security audits or access reviews.

**Trigger phrases:**
- "Audit the Mode workspace settings"
- "Review Mode permissions"
- "Check Mode data source connections"
- "Inspect Mode dashboard sharing settings"
- "Are our Mode settings following best practices?"

## Examples

- `"Audit the Mode workspace"` — Runs the full audit checklist: data sources, permissions, sharing, scheduled queries, and unused resources.
- `"Check if Mode data sources use service accounts"` — Focuses on the data source connections and verifies they don't use personal credentials.
- `"Review who has access to sensitive dashboards"` — Checks sharing settings and membership for restricted content.

## Why it was created

Analytics platforms accumulate configuration drift over time — personal credentials on shared data sources, overly broad sharing, unused connections. This skill automates the review process, catching issues that would otherwise require manual inspection of every setting.
