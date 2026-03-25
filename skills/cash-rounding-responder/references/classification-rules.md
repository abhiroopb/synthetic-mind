# Email Classification Rules

Load when classifying incoming cash rounding emails to determine how to draft a response.

| Category | Signals | Draft approach |
|----------|---------|----------------|
| **Activation request** | Seller does NOT have the feature yet and wants to enable it ("enable", "turn on", "opt in", "activate", "join beta") | Use this standard activation response: "You can add yourself by going to this link: https://app.example.com/dashboard/early-feature-access. And you can learn more about the feature here: https://example.com/help/article/feature-setup" |
| **Troubleshooting — version issue** | "not working", "failure", "doesn't show", app version mentioned and < 6.94 | Tell them to update to at least v6.94. |
| **Troubleshooting — already enabled** | Seller clearly already has cash rounding enabled but is experiencing issues (e.g., report discrepancies, rounding not appearing correctly) | Ask for specifics — screenshots, examples, device/app details. Do NOT tell them to enable via Early Feature Access since they already have it. |
| **Feature request** | "round up only", "nearest dime", custom rounding behavior | Acknowledge the request, explain current behavior (rounds to nearest $0.05 symmetrically), note it's not possible at the moment. |
| **General inquiry** | Broad questions about cash rounding, how it works, wanting more info before enabling | Use the seller-facing response template and direct to Early Feature Access. |
| **Other / unclear** | Doesn't fit above categories, missing critical details | Flag for manual review — do NOT auto-draft. |

## Drafting Guidelines

- **Read the email carefully.** If the seller mentions issues with an already-enabled feature (e.g., "end of day reports conflicting", "rounding not reflecting"), do NOT suggest enabling — they already have it. Instead, ask clarifying questions (screenshots, examples).
- **Be concise and relevant.** Only include information that directly addresses what the seller asked about.
- **Ask for details when troubleshooting.** Request screenshots, app version, device info, or specific examples of the problem.
