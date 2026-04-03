---
name: slack-saved-triage
description: Prioritize and group Slack saved messages. Use when the user wants help managing, triaging, reviewing, clearing, or organizing their Slack "Save for later" queue or saved messages.
---

# Saved Messages Triage

Prioritize, group, and triage the user's Slack "Save for later" queue.

## Steps

### Step 1: Fetch saved messages

Fetch all saved messages via `search.messages?query=is:saved`, retrieve thread or surrounding context for each, resolve user names, and write output to a temp directory:
- `summary.txt` — index of all saved messages with channel, user, preview, permalink
- `saved-NNN.txt` — per-message files with the saved message and its context
- `data.json` — full JSON data

### Step 2: Filter out reminded items

The Slack API does not expose reminder/due-date data on saved items. Ask the user for a screenshot of their Slack "Later" view so you can identify which items have reminders set:

1. Ask the user to take a screenshot and drop it into the chat
2. Read the screenshot(s). Items with "Due in ..." labels have reminders already set
3. Match reminded items to fetched messages and exclude them
4. List filtered items at the top of the output so the user can verify

If the user says to skip this step, proceed without filtering.

### Step 3: Read and categorize messages

Read each per-message file to understand context. Categorize each saved message:

**Needs action** — Things that need the user's attention or response now. Questions directed at them, time-sensitive decisions, blockers, review requests.

**Topic clusters** — Group related saved messages about the same project or topic. Give each cluster a descriptive name. This is the most valuable part — the user saves many messages around the same topic and wants to see them together.

**Stale** — Items that were important when saved but the moment has passed. Old rollouts that completed, resolved incidents, discussions that concluded. Include a brief reason.

**Consider removing** — Items that probably don't need to be saved. Bot notifications, simple acknowledgements, messages where the action was already taken.

### Step 4: Write output file

Write the triage to a dated markdown file.

**Ordering:** Needs action first, then topic clusters (largest/most important first), then stale and consider-removing at the bottom.

```markdown
# Saved Messages Triage — YYYY-MM-DD HH:MM

**86 saved messages** — N have reminders (filtered out), N remaining

## Needs action (N items)
- **[#channel](permalink)** — description of what needs doing

## Topic: [descriptive topic name] (N items)
- [#channel](permalink) — summary of saved message

## Topic: [another topic] (N items)
- ...

---
## Stale (N items)
| Message | Channel | Why stale |
|---|---|---|
| [brief description](permalink) | #channel | Rollout complete / resolved / etc |

## Consider removing (N items)
| Message | Channel | Why |
|---|---|---|
| [brief description](permalink) | #channel | Bot post / already actioned / etc |
```

### Step 5: Open and report

Convert to HTML and open in browser. Give the user a brief summary: how many need action, how many topics found, how many could be cleaned up. Ask if they want to take any action.
