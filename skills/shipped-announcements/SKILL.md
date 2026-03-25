---
name: shipped-announcements
description: "Use when writing, drafting, creating, composing, posting, formatting, building, or preparing a shipped post, launch announcement, release announcement, feature announcement, or shipping update to #shipped."
depends-on: [slack]
---

# Shipped Announcements

Craft polished #shipped launch announcements for Slack using Block Kit JSON.

**STOP** if the user has not provided at least one source of context (Slack channels, documents, or Blueprint link). Ask for these inputs before proceeding.

## Workflow

### Step 1: Gather Inputs (REQUIRED — do not skip)

Ask the user to provide:
- [ ] **Relevant Slack channels** — channels where the project has been discussed
- [ ] **Documents** — Google Docs, PRDs, one-pagers, design docs, etc.
- [ ] **Blueprint link** — the Block Roadmap (Airtable) project link

All three are **mandatory**. Do not proceed without them.

### Step 2: Research & Extract Information

Read all provided sources (Slack channels, docs, Blueprint) and extract:

| Field | Description | Required |
|-------|-------------|----------|
| **Title** | Short punchy name + emoji | ✅ |
| **WHAT** | 2-3 paragraphs: context, problem, headline change. Bold the key announcement. | ✅ |
| **Feature breakdown** | Individual features/milestones with emoji bullets, bold titles, _(dates)_ in italics | ✅ |
| **IMPACT** | 2-4 metrics showing before → after | ✅ |
| **MARKETS** | Country flags + coverage description | ✅ |
| **ROLLOUT PLAN** | Rollout % over time if doing staged rollout | Optional |
| **WHAT'S NEXT** | 2-4 upcoming items with timeline | ✅ |
| **LEARN MORE** | Demo video link, doc links, relevant Slack channels | ✅ |
| **KUDOS** | @mentions of individuals + team names | ✅ |

If any required field is missing from the docs, **ASK the user** for it. Do not guess or skip.

### Step 3: Resolve Slack User IDs for Kudos

- [ ] Look up each person's Slack user ID by name/email
- [ ] Format as `<@UXXXXXXXX>` mentions
- [ ] Group remaining team names at the end

### Step 4: Build Block Kit JSON

Build the post as a Slack Block Kit JSON array following this structure:

1. **Header** — title with emoji
2. **Section** — WHAT narrative (2-3 paragraphs, bold the key announcement)
3. **Section** — what this specific launch changes
4. **Section** — transition to feature breakdown
5. **Divider**
6. **One section per feature/milestone** — emoji + bold title + _(date)_ + description
7. **Divider**
8. **Section with two fields** — Impact (left) and Markets (right)
9. **Section with two fields** — What's Next (left) and Learn More (right)
10. **Divider**
11. **Context block** — Kudos with @mentions (renders in smaller text)

### Step 5: Save & Preview

- [ ] Save the Block Kit JSON to `/tmp/shipped-announcement.json`
- [ ] Send it to the user as a Slack DM so they can preview the rendering
- [ ] Show the JSON in chat as well for reference
- [ ] Ask for feedback and iterate on drafts as needed

### Step 6: Post to #shipped

Once the user approves:
- [ ] Confirm: "Ready to post to #shipped?"
- [ ] Only post after explicit approval
- [ ] Post to the `#shipped` channel

## Writing Style

- **Tone:** Confident, direct, slightly witty. Not corporate-speak.
- **Structure:** Problem → Solution → Impact. Lead with the headline.
- **Details:** Use specific numbers, dates, and real examples.
- **Length:** Comprehensive but scannable. Each feature section is 1-3 sentences max.
