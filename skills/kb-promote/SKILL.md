---
Skill name: kb-promote
Skill description: Promote high-value memory notes into permanent AGENTS.md rules or new skills. Use when asked to promote notes, graduate knowledge, review promotion candidates, or formalize learned behaviors.
---

# kb-promote — Knowledge Promotion

Formalizes the note → AGENTS.md graduation path. Identifies high-stability distilled notes and proposes them as permanent behavioral rules or new skills. This is the final layer of the Second Me flywheel: observations → distilled notes → **promoted rules**.

## When to Run

- User says "promote", "graduate my notes", "what should be permanent", "review promotion candidates"
- After a `kb-distill` run that produced proposed rules the user wants to act on
- User says "promote <topic>" to target a specific note

## Workflow

### Phase 1: Identify Promotion Candidates

Search amp-mem for high-value notes using stability signals:

```bash
# Get all distilled notes
amp-mem search "distilled" --type distilled --limit 50

# Also check for rules proposed by kb-distill but not yet added
amp-mem search "proposed rule" --limit 20
```

Score each candidate on **stability** (higher = more promotable):

| Signal                        | Points |
|-------------------------------|--------|
| Referenced in 3+ sessions     | +3     |
| Created > 14 days ago         | +2     |
| Never contradicted/revised    | +2     |
| Derived from 5+ observations  | +2     |
| Matches an existing behavior  | +1     |
| Recently created (< 3 days)   | -2     |
| Contradicted by later note    | -5     |

Notes scoring **5+** are strong candidates. Present them ranked.

### Phase 2: Classify Destination

For each candidate, determine where it should live:

#### A. AGENTS.md Rule
For behavioral preferences and recurring workflows. These are short, imperative instructions.

**Examples:**
- "When looking up a user account, always try the admin dashboard search first"
- "Always create Google Docs for reports, never raw text in chat"
- "When drafting emails, check the Communication Style Matrix first"

#### B. Existing Skill Enhancement
For knowledge that improves an existing skill's instructions. Append to the relevant SKILL.md.

**Examples:**
- A better workflow step discovered for an existing responder skill
- A new channel to search in `feedback-searcher`

#### C. New Skill
For complex workflows that deserve their own skill file. Only propose this for patterns with 3+ distinct steps.

**Examples:**
- A repeated multi-tool workflow for debugging a specific service
- A recurring report generation process

### Phase 3: Present Candidates

Show all candidates to the user with clear proposals:

```
🎓 Promotion Candidates
━━━━━━━━━━━━━━━━━━━━━━━━

1. ⭐ "User Account Lookup Workflow" (stability: 8/10)
   📍 Destination: AGENTS.md rule
   📝 Proposed rule: "When looking up a user account, always try the admin
      dashboard search first, then fall back to the advanced search UI."
   📊 Evidence: 7 observations across 4 sessions
   → promote / skip / edit

2. ⭐ "Feature Feedback — Tracking Tab" (stability: 7/10)
   📍 Destination: Enhance feedback tracking skill
   📝 Proposed addition: Add step to always save to the tracking sub-tab
   📊 Evidence: 5 observations across 3 sessions
   → promote / skip / edit

3. ⚠️ "Release Check Workflow" (stability: 4/10)
   📍 Destination: Not ready — needs more evidence
   📝 Note: Only seen twice, wait for more repetitions
   → defer / force-promote
```

### Phase 4: Execute Promotions

For each approved candidate:

#### Promoting to AGENTS.md
1. Read current `~/AGENTS.md`
2. Find the appropriate section (or create one if needed)
3. Append the rule in the established format
4. Show the diff to the user for confirmation
5. Save the edit

```bash
# Record the promotion
amp-mem save decision "Promoted: <topic>" \
  "Graduated '<topic>' to AGENTS.md. Rule: '<rule text>'. Based on observations: <IDs>." \
  --tags "promoted,agents-md"
```

#### Promoting to Skill Enhancement
1. Read the target SKILL.md
2. Identify where the new knowledge fits
3. Propose the edit with a diff preview
4. Apply after user approval

```bash
amp-mem save decision "Enhanced skill: <skill-name>" \
  "Added '<knowledge>' to <skill-name> SKILL.md. Based on observations: <IDs>." \
  --tags "promoted,skill-enhancement"
```

#### Promoting to New Skill
1. Use the `building-skills` skill to scaffold the new skill
2. Populate SKILL.md with the workflow from distilled notes
3. Show the full skill to the user for review

```bash
amp-mem save decision "Created skill: <skill-name>" \
  "New skill '<skill-name>' created from distilled knowledge. Based on observations: <IDs>." \
  --tags "promoted,new-skill"
```

### Phase 5: Report

```
✅ Promotion Complete
━━━━━━━━━━━━━━━━━━━━━━━━
  Candidates reviewed:  [N]
  Promoted to AGENTS.md: [N]
  Skills enhanced:       [N]
  New skills created:    [N]
  Deferred:              [N]

  Changes made:
  • ~/AGENTS.md — added 2 rules (lines XX-YY)
  • ~/.agents/skills/feedback-responder/SKILL.md — added tracking tab step
```

## Guardrails

- **Never auto-promote.** Always present candidates and wait for explicit approval.
- **Never delete the source note.** Promoted notes stay in amp-mem for traceability.
- **Show diffs before writing.** The user must see exactly what will change.
- **One rule per behavior.** Don't merge unrelated patterns into a single rule.
- **Respect existing structure.** When editing AGENTS.md, preserve formatting and section organization.

## Examples

**User says:** "promote"
→ Run full Phase 1–5 workflow, present all candidates.

**User says:** "promote the account lookup workflow"
→ Search for that specific note, skip to Phase 3 with just that candidate.

**User says:** "what's ready to promote?"
→ Run Phase 1–2 only, present candidates without acting.

**User says:** "force promote everything"
→ Run Phase 1–4, promote all candidates scoring 3+ without individual approval (but still show the report).
