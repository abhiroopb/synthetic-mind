# Flow B: During Development

Load when PM selects phase "During Development."

This flow helps PMs keep Blueprint continuously updated once their project is In Progress, At Risk, or Blocked. Blueprint is the source of truth — everything downstream (bundle inclusion, GTM, CS/AM enablement, InnerCore summaries) depends on it being accurate and current.

## B1. Verify Project Creation Fields

Display the current values of all "At Project Creation" fields and ask the PM: **"Do these still look correct, or does anything need updating?"**

If the PM flags changes or any required fields are missing, try to fill them automatically before asking for manual input:
1. **GDrive** — Ask for a doc ID/URL (PRD, spec, project brief), read with gdrive, extract values.
2. **Slack** — Search relevant channels for context.
3. **Manual input** — Only fall back to asking the PM directly if GDrive and Slack don't surface the answer.

## B2. Validate In Progress Fields

Present a checklist of all "Status = In Progress, At Risk, Blocked" fields from `field-checklists.md` (10 required + 3 conditional + 5 recommended). For each field, show filled/missing/stale status.

Group by category: Overview (Resources), Team & Ownership (Eng, PM, Design are recommended), Timeline (Target Date, Cycle, Rollout Start Date; Development Start Date is recommended; iOS Version, Android Version if applicable), Classification (Launch Type), Reach (Locale, P&P Tier), Launch Comms (Legal Regulatory Comms Required; Demo Video URL is recommended), Status Updates (Weekly Status, Update, Risks/Blockers if applicable).

For any missing fields, try to fill them automatically before asking for manual input:
1. **GDrive** — Ask for a doc ID/URL (PRD, spec, project brief), read with gdrive, extract values.
2. **Slack** — Search relevant channels for context.
3. **Manual input** — Only fall back to asking the PM directly if GDrive and Slack don't surface the answer.

**Pay special attention to:**
- **Target Date** — Check the project's GTM Tier (set at project creation). If Tier 1 or 2, Target Date must align with a bundle date (see go/featurebundlescalendar). Flag if it doesn't match.
- **Rollout Start Date** — If GTM Tier is 1 or 2, this should fall on 1% GA of the bundled features app version rollout.
- **Resources** — Check that LaunchDarkly and Linear are linked. These are required for bundle inclusion.
- **Project Status** — Should accurately reflect current state. Reference sample scenarios:
  - Not Started + Staffed = project staffed but not yet begun
  - In Progress + Staffed = actively being worked on
  - In Progress + Staffed + Rollout Start Date = rolling out
  - Delivered + Staffed = 100% rolled out
  - Blocked + Not Staffed = no longer resourced or paused
  - Blocked + Staffed = blocked by dependency or decision
  - At Risk + Staffed = in progress but at risk of being blocked

## B3. Weekly Status Update

Help the PM create or update their weekly status:

- [ ] Ask for current Weekly Status (🟢 on track / 🟡 at risk / 🔴 blocked)
- [ ] Ask for Update text (what happened this week)
- [ ] Ask for Risks/Blockers text (if applicable)
- [ ] Write to the Status Updates table (`tblgBokQjqQd6QzAW`), not directly on the project record

Remind the PM: "These updates will be scraped and summarized for InnerCore, and directly determine what is included in a Bi-Weekly Feature Bundle."

## B4. Update Airtable

- [ ] Show PM a diff of all proposed changes
- [ ] Get explicit PM approval
- [ ] Execute updates (project fields to Projects table, status updates to Status Updates table)

## B5. Summary

Present:
- Fields updated (count by category)
- Current project status and health
- Any fields still missing or stale
- If GTM Tier is 1 or 2: "Your feature is targeting bundle inclusion. Make sure you're ready for Go/No-Go ~3 weeks before your target date. Use the **Pre-Launch** flow when you're approaching that milestone."
- Recommended next steps
