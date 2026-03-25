# Blueprint Field Checklists — Status = In Progress, At Risk, Blocked

Load when validating In Progress fields during the During Development or Pre-Launch flows. These must be filled and kept current once the project reaches In Progress, At Risk, or Blocked status.

For At Project Creation fields, see `field-checklists.md`.

## Overview

| # | Field | Required? | Description | Options |
|---|-------|-----------|-------------|---------|
| 4 | Resources | Yes | Link Slack, Linear, Github, LaunchDarkly. LD + Linear required for bundle inclusion | Links |

## Team & Ownership

| # | Field | Required? | Description | Options |
|---|-------|-----------|-------------|---------|
| 10 | Eng | Recommended | Primary Eng contact(s), if applicable | User select (multi) |
| 11 | PM | Recommended | Primary PM contact(s), if applicable | User select (multi) |
| 12 | Design | Recommended | Primary Design contact(s), if applicable | User select (multi) |

## Timeline

| # | Field | Required? | Description | Options |
|---|-------|-----------|-------------|---------|
| 19 | Target Date | Yes | 100% GA date. Tier 1&2: must match bundle GA date. Tier 3&4: team discretion | Date |
| 20 | Cycle | Yes | 6-week execution cycle | Linked record |
| 21 | Rollout Start Date | Yes | When rollout begins. Tier 1&2: must match bundle 1% GA date | Date |
| 22 | Development Start Date | Recommended | Target date to start development | Date |
| 23 | iOS Version | Yes, if applicable | iOS version for release | Version select |
| 24 | Android Version | Yes, if applicable | Android version for release | Version select |

## Classification, Reach, Launch Comms

| # | Field | Required? | Description | Options |
|---|-------|-----------|-------------|---------|
| 25 | Launch Type | Yes | CS support model depends on this | Experiment, Closed Beta, Open Beta, GA, Rolled Back |
| 28 | Locale | Yes | Geo(s) for launch | Geo select (multi) |
| 30 | P&P Tier | Yes | Pricing & Packaging tier. Add reasoning in Notes | Free, Plus, Premium |
| 33 | Legal, Regulatory Comms Required | Yes | Mandated for legal/regulatory/contractual purposes | Checkbox (true/false) |
| 34 | Demo Video URL | Recommended | Product demo for GTM teams | URL |

## Status Updates

Written to Status Updates table (`tblgBokQjqQd6QzAW`), not the project record.

| # | Field | Required? | Description | Options |
|---|-------|-----------|-------------|---------|
| 36 | Weekly Status | Yes | Progress this week | 🟢 (on track), 🟡 (at risk), 🔴 (blocked/off track) |
| 37 | Update | Yes | Update text for the week | Free text |
| 38 | Risks/Blockers | Yes, if applicable | Risks/blockers text, if applicable | Free text |

## Summary

- **10 required** + 3 conditional (iOS Version, Android Version, Risks/Blockers) + 5 recommended (Eng, PM, Design, Development Start Date, Demo Video URL) = **18 fields**
- **Total across both tiers: 38 fields**
