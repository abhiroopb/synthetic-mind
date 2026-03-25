# Blueprint Field Checklists — At Project Creation

Load when validating Blueprint fields for any phase.

Fields are organized by category with three timing tiers:
- **At Project Creation** — must be filled when the project is first created
- **Status = In Progress, At Risk, Blocked** — must be filled and kept current once the project reaches these statuses (used in the During Development flow)
- **Optional** — not required but encouraged

Required? values: **Yes** (required), **Yes, if applicable** (conditional), **Recommended** (encouraged but not required), **No** (optional).

**Removed fields** (no longer in Blueprint): Seller Cohort, Seller Sub-Cohort, Legal Review Required, Short Form CTA Text, Short Form CTA Link. These outputs are now automated via AI understanding of project description and other fields.

For In Progress fields, see `field-checklists-in-progress.md`. For output format, see `validation-output-creation.md` and `validation-output-in-progress.md`.

## Overview

| # | Field | Required? | Description | Options |
|---|-------|-----------|-------------|---------|
| 1 | Project Name | Yes | Brief tagline of the project or feature | Free text |
| 2 | Project Description | Yes | What: Outcome. Why: Need & links. [Primary Metric, Goal] if applicable | Free text |
| 3 | Project Status | Yes | Current status, regularly updated | Not Started, In Progress, Blocked, At Risk, Delivered, Backlog, Cancelled |
| 5 | Staffed | Yes | Is the project staffed across all dependent teams? | Yes, Not Staffed |
| 6 | Prioritization | Yes | Relative priority | P0 (must deliver), P1 (important), P2 (nice to have) |
| 7 | Notes | No (Optional) | Additional project notes | Free text |

## Team & Ownership

| # | Field | Required? | Description | Options |
|---|-------|-----------|-------------|---------|
| 8 | DRI | Yes | Accountable owner. Only one DRI | User select |
| 9 | Owning Organization | Yes | Which Org L1/2/3 is responsible? | Linked record |

## Strategy

| # | Field | Required? | Description | Options |
|---|-------|-----------|-------------|---------|
| 13 | Work Type | Yes | Strategic Priority, Refine, or Functional Priority | Strategic Priority, Refine, Functional Priority |
| 14 | Strategic Priority (Primary) | Yes, if applicable | Required if Work Type = Strategic Priority or Refine Priority | Linked record |
| 15 | Sub-Priority | Yes, if applicable | Required if Work Type = Strategic Priority | Linked record |
| 16 | Program Name | Yes | Select existing or create new | Dropdown (dynamic) |
| 17 | Functional Priority | Recommended | Appropriate Functional Priority | Linked record |

## Timeline, Classification, Reach, Launch Comms, Dependencies

| # | Field | Required? | Description | Options |
|---|-------|-----------|-------------|---------|
| 18 | Roadmap Quarter | Yes | Quarter(s) for roadmap. Select multiple if needed | Quarter select (multi) |
| 26 | Change Type | Yes | Type of change being shipped | New product, New feature, Pricing change, Change to existing feature (Workflow Critical UI / Other), Feature removal/deprecation, N/A |
| 27 | Platform | Yes | Which platform(s) | Android, Web, iOS, Platform (multi-select) |
| 29 | Seller Impact | Yes | Impact level per classification guide | Severe, High, Medium, Low, None |
| 31 | GTM Tier | Yes | Marketing tier. Tier 1+2 = bundle inclusion, requires Target Date match | Tier 1, Tier 2, Tier 3, Tier 4 |
| 32 | Share Externally | Yes | Default Yes for seller-facing features | Yes, No |
| 35 | Dependent Org(s) | Recommended | Which Org(s) must contribute to deliver? | Linked record (multi) |

## Summary

- **15 required** + 2 conditional (Strategic Priority, Sub-Priority) + 2 recommended (Functional Priority, Dependent Orgs) + 1 optional (Notes) = **20 fields**
