# Flow A: Just Starting the Project

Load when PM selects phase "Just Starting."

This flow helps PMs create their Blueprint project with all required fields for project creation, and craft positioning/narrative.

## A1. Validate Project Creation Fields

Present a checklist of all "At Project Creation" fields from `field-checklists.md` (15 required + 2 conditional + 2 recommended + 1 optional). For each field, show filled/missing status.

Group by category: Overview (Project Name, Project Description, Project Status, Staffed, Prioritization; Notes is optional), Team & Ownership (DRI, Owning Organization), Strategy (Work Type, Strategic Priority if applicable, Sub-Priority if applicable, Program Name; Functional Priority is recommended), Timeline (Roadmap Quarter), Classification (Change Type, Platform), Reach (Seller Impact, GTM Tier), Launch Comms (Share Externally), Dependencies (Dependent Orgs is recommended).

For conditional Strategy fields (Strategic Priority, Sub-Priority), check Work Type value to determine if they apply.

## A2. Fill Missing Fields

For each missing field, try to fill it automatically before asking the PM for manual input:

1. **Google Doc or GitHub markdown** — Ask the PM for a doc ID/URL (e.g., PRD, spec, project brief), read it with gdrive, and extract relevant field values. Try this first.
2. **Slack search** — Search relevant channels for context that could inform the field value (e.g., project announcements, team discussions, prior planning threads).
3. **Manual input** — Only fall back to asking the PM directly if GDrive and Slack don't surface the answer.

**Special attention:**
- **Program Name** — Search existing program names in the dropdown first, then offer to create a new one if needed.
- **GTM Tier** — Selecting Tier 1 or 2 indicates the feature will be included in an upcoming bundle and requires Target Date to match. Confirm the PM understands the implications.
- **Seller Impact** — Use the classification guide to help the PM determine the correct level.

## A3. Craft Positioning/Narrative

For the Project Description field:

- [ ] Read the GTM Messaging Toolkit (`1KFVMwE3oZl8IgAX_2KGBlHN7SVD-gvs8oK_Jr3r1sFw`) for frameworks and value props
- [ ] Read the GTM Guide for PMs (`13kDJqv2V10Y4t_LffFOmCloADvVYzaCjfmCNyty5Xn4`) for problem/bet/win structure
- [ ] Draft a Project Description emphasizing seller value
- [ ] Present for PM review and iterate until approved
- [ ] Ask: **"Would you like me to put this positioning into a Google Doc for easy sharing?"**

## A4. Update Airtable

- [ ] Show PM a diff of all proposed changes
- [ ] Get explicit PM approval
- [ ] Execute the update

## A5. Summary

Present:
- Fields filled (count by category)
- Positioning/narrative crafted
- What internal teams should know
- Reminder: "Once your project moves to In Progress, use the **During Development** flow to keep Blueprint current with the additional required fields (Resources, Target Date, Cycle, Launch Type, Locale, P&P Tier, Weekly Status, etc.)"
- Recommended next steps (e.g., "Share the Blueprint link with your eng lead")
