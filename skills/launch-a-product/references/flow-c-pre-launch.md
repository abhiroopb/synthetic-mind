# Flow C: Pre-Launch (Bundle Inclusion)

Load when PM selects phase "Pre-Launch."

This flow prepares features for inclusion in a biweekly bundled feature release. Under the unified release process, GA launches are automated — Blueprint fields trigger Feature Log, seller emails, in-product alerts, and AM enablement automatically. The PM's role shifts from "drive GTM" to "ensure inputs are correct."

## C1. Confirm Bundle Readiness

Ask the PM:
- "Which bundle are you targeting?" (reference go/featurebundlescalendar for upcoming dates)
- "Is your feature stable and meeting the bundle bar?"
- "Has the feature been beta tested (ideally via shared TestFlight pool)?"

If the feature isn't ready, help the PM identify what's blocking and suggest targeting a later bundle.

## C2. Verify Project Creation Fields

Display the current values of all "At Project Creation" fields and ask the PM: **"Do these still look correct, or does anything need updating?"**

If the PM flags changes or any required fields are missing, try to fill them automatically before asking for manual input:
1. **GDrive** — Ask for a doc ID/URL (PRD, spec, project brief), read with gdrive, extract values.
2. **Slack** — Search relevant channels for context.
3. **Manual input** — Only fall back to asking the PM directly if GDrive and Slack don't surface the answer.

## C3. Verify In Progress Fields

Display the current values of all "Status = In Progress, At Risk, Blocked" fields and ask the PM: **"Do these still look correct, or does anything need updating?"**

If the PM flags changes or any required fields are missing, try to fill them automatically before asking for manual input:
1. **GDrive** — Ask for a doc ID/URL (PRD, spec, project brief), read with gdrive, extract values.
2. **Slack** — Search relevant channels for context.
3. **Manual input** — Only fall back to asking the PM directly if GDrive and Slack don't surface the answer.

**Bundle-critical field checks:**
- **Resources** — LaunchDarkly and Linear MUST be linked. Without these, the feature cannot be included in a bundle.
- **Target Date** — Must fall on the 100% GA date of the target bundle (see go/featurebundlescalendar). Do not use binary version numbers as bundle identifiers.
- **Rollout Start Date** — Must fall on the 1% GA date of the bundled features app version rollout.
- **GTM Tier** — Must be Tier 1 or 2 for bundle inclusion. Tier 3 and 4 features are not bundled.
- **Launch Type** — Should be set to "GA" if targeting full bundle rollout.
- **Project Status** — Should be "In Progress" with rollout imminent.
- **Share Externally** — Should be "Yes" for seller-facing features going into a bundle.
- **Project Description** — Must be accurate and complete — this feeds automated GTM comms.
- **Demo Video URL** — Strongly encouraged. Used by GTM teams to learn about the feature.

Flag any fields that are missing, stale, or inconsistent with bundle expectations.

Continue to `flow-c-pre-launch-wrapup.md` for steps C4-C7.
