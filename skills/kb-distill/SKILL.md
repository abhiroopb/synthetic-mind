---
name: kb-distill
description: "Distill raw observations into structured knowledge notes and propose AGENTS.md rules. Use when asked to distill, synthesize, compress, review, or summarize accumulated memory/observations. Also runs automatically when triggered by session-start or weekly cadence."
---

# kb-distill — Knowledge Distillation

Compresses raw `amp-mem` observations into structured knowledge and proposes behavioral rules for AGENTS.md. This is the middle layer of the Second Me flywheel: observations → **distilled notes** → promoted rules.

## When to Run

- User says "distill", "synthesize my observations", "what have I learned recently", "compress memory"
- Weekly cadence (check `amp-mem distill-status` — if >50 pending observations or >7 days since last run)
- On session start, if `amp-mem distill-status` shows significant backlog

## Workflow

### Phase 1: Gather Raw Material

```bash
# Check what's pending
amp-mem distill-status

# Dump all observations since last distillation
amp-mem distill-dump
```

If `--since DATE` is needed (e.g., user says "distill the last month"):
```bash
amp-mem distill-dump --since 2026-02-01
```

### Phase 2: Analyze & Cluster

Read all dumped observations and identify:

1. **Repeated patterns** — Actions performed 3+ times (e.g., "looked up merchant token via Regulator" appearing across sessions). These are rule candidates.
2. **Topic clusters** — Groups of related observations that form a coherent knowledge area (e.g., "checkout flow debugging", "cash rounding seller feedback workflow").
3. **Decision chains** — Sequences where a decision was made, tested, and confirmed or revised.
4. **One-off facts** — Individual observations worth preserving but not patterns.

### Phase 3: Produce Outputs

For each cluster/pattern, produce one of three output types:

#### A. Distilled Notes (saved to amp-mem)

For topic clusters, save a synthesized note:
```bash
amp-mem save distilled "<topic>" "<synthesized summary>" --tags "distilled,<cluster-tags>"
```

The summary should be:
- **Actionable** — tells future-you what to do, not just what happened
- **Concise** — shorter than the sum of source observations
- **Cross-referenced** — mentions source observation IDs for traceability

Example:
```bash
amp-mem save distilled "Merchant Token Lookup Workflow" \
  "To look up a merchant token: (1) Use Regulator omniSearch GraphQL with email/name, (2) If omniSearch fails, provide the advanced search UI link: https://regulator.sqprod.co/o/advanced-search. (3) Can also search by MT directly in Iterable (Audience → Contact Lookup). Derived from observations #12, #34, #67." \
  --tags "distilled,regulator,merchant-lookup"
```

#### B. Proposed Rules (for AGENTS.md)

For repeated patterns (3+ occurrences), propose a rule to add to AGENTS.md. **Present each rule to the user for approval** — do NOT auto-add.

Format the proposal like:
```
📋 PROPOSED RULE (based on pattern seen N times):
  "When looking up a merchant token, always try Regulator omniSearch first, then fall back to the advanced search UI link."

  Evidence: observations #12, #34, #67
  Add to AGENTS.md? [Present to user]
```

If the user approves, append the rule to `~/AGENTS.md` in the appropriate section.

#### C. Implicit Behavior Inference

This is the key differentiator. Look for patterns the user **never explicitly stated** but consistently does:
- Tools always used in a specific order
- Preferences about output format (Google Doc vs chat, inline vs browser)
- Recurring questions to specific people/channels
- Default approaches to certain problem types

For these, frame the proposal as:
```
🔍 INFERRED PREFERENCE (observed but never stated):
  You always create a Google Doc when producing reports, never output to chat.
  Seen in: observations #5, #19, #28, #41

  Codify this? [Present to user]
```

### Phase 4: Record & Report

After producing all outputs:

```bash
# Record that distillation happened
amp-mem distill-record <observation_count> <notes_produced> <rules_proposed> "<brief summary>"
```

Then present a summary to the user:
```
✅ Distillation Complete
━━━━━━━━━━━━━━━━━━━━━━━━
  Observations processed: 47
  Notes produced:         8
  Rules proposed:         3
  Inferred preferences:   2

  📝 Notes:
  1. "Merchant Token Lookup Workflow" — consolidated 4 observations
  2. "Cash Rounding Feedback Process" — consolidated 6 observations
  ...

  📋 Proposed Rules:
  1. Always use Regulator omniSearch for merchant lookups
  2. Save cash rounding feedback to Post-Launch sub-tab
  3. ...

  🔍 Inferred Preferences:
  1. Always create Google Docs for reports (never raw text)
  2. ...
```

## Integration with Session Start

On session start, after loading context, check:
```bash
amp-mem distill-status
```

If pending observations > 50 or last distillation > 7 days ago, **auto-run silently**:
1. Execute the full Phase 1–4 workflow
2. Save distilled notes automatically (no approval needed for notes)
3. For proposed AGENTS.md rules, append them at the end of your first response to the user:
   ```
   ---
   🧠 While warming up, I distilled N observations and noticed:
   📋 Rule: "Always use Regulator omniSearch for merchant lookups" → approve / skip
   🔍 Inferred: "You prefer Google Docs over chat for reports" → approve / skip
   ```
4. If the user ignores them, that's fine — they're non-blocking.

The user should **never have to ask** for distillation. It just happens.

## Examples

**User says:** "distill my recent work"
→ Run the full Phase 1–4 workflow above.

**User says:** "what patterns have you noticed?"
→ Run Phase 1–2 only, then present findings without saving.

**User says:** "distill and auto-approve all rules"
→ Run Phase 1–4, but add all proposed rules to AGENTS.md without asking.

**User says:** "distill the last month"
→ `amp-mem distill-dump --since $(date -v-30d +%Y-%m-%d)` then proceed normally.
