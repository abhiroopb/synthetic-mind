---
name: kb-style-matrix
description: "One-time Slack analysis to build your communication profile. Use when asked to build a style matrix, analyze communication style, create a voice profile, or match writing tone."
---

# kb-style-matrix — Communication Style Matrix

Analyzes your Slack messages to build a reusable voice/tone profile so future drafts (emails, Slack, docs) match your natural communication style. Part of the Second Me flywheel.

## When to Run

- User says "build my style matrix", "analyze my communication style", "create my voice profile"
- First-time setup of the Second Me system
- User says "refresh my style matrix" (re-run with fresh data)

## Prerequisites

- `slack` skill must be available
- User's Slack identity must be resolvable (uses `abhiroop` / Abhi Basu)

## Workflow

### Phase 1: Gather Messages

Use the `slack` skill to pull the user's recent messages across a diverse set of channels. Target ~90 days of history across different audience types:

1. **Team/IC channels** — e.g., channels where the user talks to engineers, designers, PMs on their team
2. **Cross-functional channels** — broader org or company channels
3. **Manager/leadership channels** — DMs or channels with manager, skip-level
4. **External-facing** — channels involving partners, vendors, or public-facing comms

```
Search Slack for messages from the user across 5-8 channels they're most active in.
Pull ~50-100 messages per audience category.
```

### Phase 2: Analyze Patterns

For each audience category, extract:

#### Tone Dimensions
- **Formality** — casual ("hey team") vs. formal ("Hi all, I wanted to share")
- **Directness** — blunt ("We need to cut this") vs. hedged ("I'm wondering if we might consider")
- **Energy** — enthusiastic ("Love this!") vs. measured ("This looks reasonable")
- **Emoji/reaction usage** — frequency and types

#### Structural Patterns
- **Message length** — typical word count range
- **Paragraph structure** — bullets vs. prose, headers vs. inline
- **Opening patterns** — how messages typically start
- **Closing patterns** — how messages typically end (sign-off, CTA, open-ended)

#### Vocabulary Fingerprint
- **Signature phrases** — recurring expressions (e.g., "the punchline is", "net-net")
- **Jargon level** — how much internal/technical jargon vs. plain language
- **Filler words** — characteristic hedges or transitions

#### Audience Adaptation
- How tone shifts between audiences (e.g., more casual with ICs, more structured with leadership)

### Phase 3: Build the Matrix

Produce a structured profile and save it as a distilled note:

```bash
amp-mem save distilled "Communication Style Matrix" \
  "<structured profile>" \
  --tags "distilled,style-matrix,voice-profile,second-me"
```

The profile should follow this structure:

```
## Communication Style Matrix — [User Name]
Generated: [date] | Messages analyzed: [N]

### Default Voice
- Formality: [1-5 scale + description]
- Directness: [1-5 scale + description]
- Energy: [1-5 scale + description]
- Emoji frequency: [none/light/moderate/heavy]

### Audience Adaptations
| Audience       | Formality | Directness | Length    | Key Shifts          |
|----------------|-----------|------------|-----------|---------------------|
| Team ICs       | ...       | ...        | ...       | ...                 |
| Cross-functional | ...     | ...        | ...       | ...                 |
| Leadership     | ...       | ...        | ...       | ...                 |

### Signature Patterns
- Opens with: [typical openers]
- Closes with: [typical closers]
- Recurring phrases: [list]
- Bullet vs prose: [preference]

### Writing Rules (for voice-matching)
1. [Actionable rule, e.g., "Use 'hey' not 'Hi all' for team channels"]
2. [e.g., "Keep Slack messages under 4 sentences unless sharing a decision"]
3. [e.g., "Always end status updates with a clear next-step"]
...
```

### Phase 4: Report

Present the matrix to the user in chat for review:

```
✅ Style Matrix Built
━━━━━━━━━━━━━━━━━━━━━━━━
  Messages analyzed: [N]
  Channels scanned:  [N]
  Audience types:    [N]

  [Show the full matrix]

  Saved to amp-mem as "Communication Style Matrix"
  Future drafts will reference this profile for voice-matching.
```

## How Other Skills Use This

When drafting emails, Slack messages, or docs, other skills should:

```bash
amp-mem search "Communication Style Matrix"
```

Then apply the writing rules from the profile to match the user's voice. The audience type should be inferred from context (e.g., drafting to manager → use Leadership adaptation).

## Re-running

If the user says "refresh my style matrix":
1. Pull fresh Slack data
2. Rebuild the profile
3. Save as a new distilled note (the old one remains for comparison)
4. Highlight any shifts: "Your messages have gotten more direct over the past quarter"
