---
name: trust-feature-validation
description: "Validate that a product feature is working correctly during rollout. Use when validating feature behavior during ramps, spot-checking affected users from Slack or escalations, running periodic audits, or investigating false positives and false negatives. Walks users through structured intake questions, queries data warehouses and other data sources, applies feature-specific validation logic, and outputs verdicts to terminal or Google Sheets. Supports pluggable initiative configs for any product area."
depends-on: [snowflake, gdrive]
argument-hint: "<initiative> [tokens or --date YYYY-MM-DD or --slack <url>] [--sheets]"
metadata:
  version: "1.0.0"
  status: experimental
---

# Feature Validation Skill

Validates that a product feature is working correctly during rollout. Works across any product area — identity, payments, banking, compliance, etc. Each initiative defines its own data sources, validation logic, and expected behavior.

**Use when**: validating feature behavior during ramps, spot-checking affected users from Slack/escalations, running periodic audits, or investigating false positives/negatives for any feature.

## Quick Start

```
/feature-validation
```

The skill will walk you through a structured intake. You can also be specific:

```
/feature-validation <initiative-name> <tokens>
/feature-validation <initiative-name> --date 2026-04-01 --sheets
/feature-validation <initiative-name> --recent 20
```

## Interactive Intake

When invoked, determine what information you already have from the user's prompt and **only ask questions for what's missing**.

**Rule**: Never re-ask something the user already provided. Parse their prompt first, then fill gaps.

### Question 1: Which initiative?

Present available initiatives from the `initiatives/` directory. If the feature isn't listed, offer to build a new config.

### Question 2: Which entities?

```
How do you want to identify the affected entities?

1. Paste tokens — I have specific tokens to check
2. Slack thread — extract tokens from a Slack thread URL
3. Date range — find all affected entities on a specific date
4. Data warehouse table — query a table for the population
5. Recent — validate the N most recently affected entities
```

### Question 3: Output format?

```
1. Terminal summary — quick verdict table in the conversation
2. Google Sheets — full multi-tab spreadsheet with Summary, Detail, and Analysis tabs
```

## New Initiative Intake

When the user wants to validate a feature that doesn't have a config yet, ask:

1. **What does the feature do?** Expected behavior, feature flag, ramp %
2. **What entity type?** customer_token, account_token, merchant_token, order_id, etc.
3. **How to find affected entities?** Data warehouse table, metrics, derived data
4. **What data validates correctness?** Primary and supplementary data sources
5. **What are the rules?** Trigger conditions, exclusions, edge cases

Then build the config, save to `initiatives/`, confirm, and proceed.

## Validation Pipeline

Every initiative follows the same 7-step pipeline:

### Step 1: Resolve Entities
Parse identifiers from args, Slack thread, data warehouse table, or query by date/recent.

### Step 2: Query Primary Data
Run the initiative's primary query against the relevant data source.

### Step 3: Handle Missing Entities
Run missing entity checks (e.g., account merges, ETL lag, cross-system lookups).

### Step 4: Query Supplementary Data
Run initiative-specific supplementary queries for additional context.

### Step 5: Apply Feature Logic
Run the initiative's validation function against the queried data. Compare expected vs actual outcome.

### Step 6: Compute Verdicts

For each entity:
- **CORRECT** — feature behaved as expected
- **FALSE POSITIVE** — entity was affected but shouldn't have been
- **FALSE NEGATIVE** — entity was not affected but should have been
- **INCONCLUSIVE** — insufficient data to determine

### Step 7: Output Results
- **Terminal**: Summary table with per-entity verdicts
- **Google Sheets**: Multi-tab spreadsheet with Summary, Detail, and Analysis tabs

## Adding a New Initiative

Create a file in `initiatives/` named `<initiative-slug>.md`. Required sections:

1. Feature Description
2. Entity Type
3. Affected Population
4. Primary Query
5. Supplementary Queries
6. Validation Logic
7. Expected Behavior Matrix
8. Known Edge Cases
9. Output Schema
10. Data Best Practices

See `initiatives/_template.md` for a blank template.

## General Data Practices

1. **Look up table schemas and business rules** before writing queries
2. **Cross-check across data sources** — flag discrepancies rather than silently picking one
3. **Handle timezone**: Data warehouse timestamps are UTC; compare carefully with local dates
4. **Check for ETL lag**: Recent events (< 24h) may not be in analytics tables
5. **Consult domain-specific guides**: Each product area may have its own data guide
