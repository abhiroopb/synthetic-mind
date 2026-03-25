# Flow E: Manual GA (Bespoke Rollouts)

Load when PM selects "Manual Beta/GA" and chooses GA. Use for Early Feature Access (EFA), bespoke rollouts, or features that need more white-glove service than the standard bundle process. Same structure as Flow D with these key differences.

## E1. Confirm Beta Feedback Incorporation

Before proceeding, ask the PM:
- "Has beta feedback been reviewed and incorporated?"
- "Are there any open issues from beta that block GA?"
- "Has the Project Description been updated to reflect what was learned in beta?"

If not addressed, pause and help the PM resolve before continuing.

## E2. Validate All Fields

Validate all 38 fields from `field-checklists.md`, with GA-specific value checks:

- **Launch Type** should be "GA"
- **Rollout Start Date** must be set to GA date
- **Project Status** should reflect GA stage
- All conditional fields should be resolved (not left as "TBD")

## E3. Identify Interested Sellers

Same Slack search as Flow D. Include sellers from beta who provided positive feedback.

## E4. Define GA Rollout Plan

**Step 1:** Summarize what's known about the beta rollout, then ask:

```text
1) How did the beta rollout go? What worked and what didn't?
2) Are there segments that need a different GA timeline?
3) What's your biggest concern going from beta to GA? (scale / support readiness / seller experience / dependencies / other)
4) How quickly do you want to ramp to full availability? (gradual / fast / big bang)
5) Should beta sellers automatically roll into GA, or need migration?
6) Are there sellers or segments to explicitly hold back from GA?
```

**Step 2:** Build the GA rollout plan. Determine wave count, beta→GA transition, gating criteria from answers.

**Step 3:** For each wave define: name/rationale, seller criteria, approximate count, duration, success gate, rollback criteria.

**Step 4:** Present for review — this should be the final, approved version. After approval, ask: **"Would you like me to put this rollout plan into a Google Doc for easy sharing?"**

## E5. Draft GA Comms

Same categories as Flow D, but **final and polished** (not drafts).

**Internal CS/AM Prep Materials:**
- Final briefing doc with full feature scope
- Complete FAQ with answers validated during beta
- CS/AM readiness confirmation checklist
- GA rollout schedule

**Seller-Facing GA Announcement:**
- Publication-ready announcement language (tailored per wave if needed)
- Full feature description and benefits
- Getting started guide
- Support resources

After presenting, ask: **"Would you like me to put these comms into a Google Doc for easy sharing?"**

## E6. Lifecycle Comms

> System TBD. Draft manual comms for now.

Prepare final lifecycle comms: launch announcement, onboarding sequence, adoption check-in.

After presenting, ask: **"Would you like me to put these lifecycle comms into a Google Doc for easy sharing?"**

## E7. Update Airtable

Same as Flow D.

## E8. GA Launch Readiness Summary

Same format as Flow D with GA-specific framing and a "ready to ship" confidence assessment.
