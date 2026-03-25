---
name: launch-a-product
description: "Guide PMs through GTM launch readiness. Use when launching, shipping, releasing, rolling out, validating, preparing, prepping, or checking readiness for a product launch. Validates Blueprint (Airtable) fields, crafts positioning, keeps Blueprint updated during development, prepares for bundle inclusion, and drafts internal/external comms."
depends-on: [airtable, slack, gdrive]
metadata:
  author: cmorrison
  version: "2.0.0"
  status: beta
---

# Launch a Product

GTM launch readiness specialist for Square PMs. Guides structured launch preparation across the unified release process — validates Blueprint fields, crafts positioning/narrative, keeps Blueprint current during development, and prepares features for biweekly bundle inclusion.

**Scope:** GTM preparation only. No feature flags, code changes, or deployments.

**Context:** Square now uses a unified release process powered by Lookout. GA launches are automated via biweekly bundled feature releases — sellers experience coordinated changes every 2 weeks. Blueprint is the source of truth; everything downstream (bundle inclusion, GTM, CS/AM enablement) depends on it being accurate and current.

## Prerequisites

**STOP** if any of these are not met — tell the PM what's missing.

- Connected to Cloudflare WARP VPN
- `gdrive` skill installed (`sq agents skills add gdrive`)
- Slack and Airtable MCPs enabled

## Key References

See `references/key-references.md` for GTM doc IDs, Blueprint base/table IDs, bundle calendar, and Slack channels.

## Core Workflow

### Step 1: Ask the PM

```text
Welcome to Launch a Product! Let's get your project GTM-ready.

1) What phase are you in?
   a) Just Starting — create/set up Blueprint project with all required fields, craft positioning
   b) During Development — update Blueprint fields for in-progress work, keep status current
   c) Pre-Launch — prepare for bundle inclusion, confirm Go/No-Go readiness
   d) Manual Beta/GA — (for bespoke rollouts, EFA, or features outside the bundle process)

2) What is the project name in Blueprint?

Reply with your phase and project name (e.g., "1a, Instant Payouts")
```

### Step 2: Identify the Project

- [ ] Search Blueprint with `mcp__airtable__search_records` on table `tbluWMCGq36V7hMkj` in base `appoAMUCsm6spyACv`
- [ ] If multiple matches, ask PM to confirm
- [ ] Fetch full record with `mcp__airtable__get_record`
- [ ] Display summary (name, status, DRI, owning org)

### Step 3: Route to Phase

Load the appropriate reference for the selected phase:
- **Just Starting** → `references/flow-a-just-starting.md`
- **During Development** → `references/flow-b-during-development.md`
- **Pre-Launch** → `references/flow-c-pre-launch.md`
- **Manual Beta/GA** → `references/flow-d-manual-beta.md` or `references/flow-e-manual-ga.md`

All flows validate Blueprint fields using `references/field-checklists.md` (project creation) and `references/field-checklists-in-progress.md` (in progress).

## Field Validation Rules

Blueprint fields are organized into categories (Overview, Team & Ownership, Strategy, Timeline, Classification, Reach, Launch Comms, Dependencies, Status Updates) with three tiers of required timing:

- **At Project Creation** — must be filled when the project is first created in Blueprint
- **Status = In Progress, At Risk, Blocked** — must be filled and kept current once the project reaches these statuses (the During Development flow)
- **Optional** — not required but encouraged

Full field tables with descriptions, dropdown options, and timing requirements are in `references/field-checklists.md` and `references/field-checklists-in-progress.md`.

**When presenting missing or suggested fields to the PM, always include:**
1. A brief description of what the field is for
2. The available options if the field is a dropdown/select
3. Your suggested value and why you're recommending it

## Slack Seller Search

When searching for interested sellers, always search these channels:

| Channel | Purpose |
|---------|---------|
| `#sq-seller-feedback-intake` | General seller feedback intake and triage |
| `#strategic-seller-churn-threats` | High-value seller churn signals and escalations |
| `#retention-hotline` | Urgent retention cases and seller issues |

Also search relevant channels based on the feature area.

Compile results into:

| Seller | Channel | Context/Quote | Account Manager | Date |
|--------|---------|---------------|-----------------|------|

## Airtable Updates

- [ ] Always show the PM a diff of proposed changes before writing
- [ ] Get explicit PM approval
- [ ] Execute with `mcp__airtable__update` or `mcp__airtable__batch_update_records`
- [ ] Update, Risks/Blockers, and Weekly Status are lookup fields — write to Status Updates table (`tblgBokQjqQd6QzAW`), not directly on the project record

## Google Doc Export

After every plan generation or messaging generation step, ask: **"Would you like me to put this into a Google Doc for easy sharing?"**

## Output Rules

- Always display results directly in chat first
- Do NOT save to files automatically
- Only export to Google Doc when the PM requests it
- Read the GTM Messaging Toolkit and GTM Guide for PMs before drafting any comms

## Anti-patterns

- Don't skip field validation — always check fields before drafting comms
- Don't update Airtable without showing the PM a diff and getting approval
- Don't assume field applicability for conditional fields — always ask the PM
- Don't skip project identification — always confirm the correct Blueprint record
- Don't confuse bundle process with manual Beta/GA — most features should use the bundle path
