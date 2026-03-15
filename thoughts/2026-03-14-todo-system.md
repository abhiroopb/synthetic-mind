# I Stopped Maintaining My To-Do List and Let the Agent Do It

## TL;DR

I'm bad at to-do lists. I forget to check them, forget to update them, and forget they exist. So I built one that doesn't need me. It watches every incoming signal — Slack, Gmail, Calendar, Linear, Notion — auto-captures action items, prioritizes them, adds them to my calendar, and surfaces them at the start of every session. I don't manage the list. The list manages me.

## Context

I've tried every to-do system. Todoist, Things, Apple Reminders, Notion databases, plain text files. They all have the same problem: they require me to use them. I have to remember to open the app, remember to add items, remember to check items off. And I just... don't. Not consistently.

The pattern is always the same. Someone asks me something in Slack. I think "I'll do that later." I don't write it down. Three days pass. They follow up. I feel bad. Repeat.

It's not a discipline problem. It's a workflow problem. The places where action items appear (Slack DMs, email threads, PR reviews, meeting follow-ups) are completely disconnected from the place where I'm supposed to track them. The gap between "I should do this" and "I wrote this down" is where everything falls through.

## The Idea

What if the to-do list didn't need me at all?

Not "what if it had a nice UI" or "what if it synced across devices." What if it literally watched everything coming in, decided what needed action, created the task, set the priority, and then told me about it at exactly the right time?

That's what the `todo` skill does. It's a JSON file at `~/.config/amp/todo.json` — dead simple storage — paired with a set of behaviors that make it proactive instead of passive.

### Auto-capture: I never add items manually

When my `start-of-day` skill runs through Slack unreads, Gmail, Calendar, and comments — every actionable item I skip or save for later automatically becomes a to-do. I don't say "add this to my list." The agent recognizes it's an action item and captures it silently:

```
📌 Added 3 items to your to-do list
```

That line shows up at the end of triage. I didn't do anything. Three tasks are now tracked.

The same thing happens during any session. Someone DMs me in Slack asking for a review? To-do. Email from a seller needing follow-up? To-do. Linear issue assigned to me? To-do. I don't context-switch to a task manager. The agent handles it in the background.

### Auto-prioritize: I never decide what's urgent

Every captured item gets a priority based on signals:

- **P1 (urgent)** — sender is a VP or the message literally says "urgent" or "ASAP"
- **P2 (high)** — direct ask from a person, needs my input
- **P3 (normal)** — review requests, FYI items, docs to read
- **P4 (low)** — bot notifications, automated alerts

I used to spend mental energy triaging. Now the agent does it based on who's asking and how they're asking. It's not perfect, but it's right 90% of the time, and I can bump priorities with a quick "prioritize 3 as P1."

### Calendar sync: I never forget deadlines

Here's the part that changed everything. When a to-do item has a future due date, the agent creates a 15-minute calendar event at 3pm ET. Color-coded by priority: red for urgent, yellow for high, blue for normal. If multiple items are due the same day, they stagger by 15 minutes.

I live in my calendar. I don't live in a to-do app. So instead of hoping I remember to check a list, I get a calendar notification at 3pm that says "Review PR #4521 for tip buttons." The task comes to me in the tool I actually look at.

### Session start: the list finds me

Every time I start a session with my agent, the to-do list surfaces automatically. Top 5 items, sorted by priority and due date:

```
## ✅ To-Do List (8 open items)

1. 🔴 [P1] Reply to Sarah's escalation email — Gmail, 3h ago
2. 🟠 [P2] Review PR #4521 for tip buttons — GitHub, 1d ago
3. 🟡 [P3] Update Q1 OKRs in Google Doc — Google Docs, 2d ago
4. 🟡 [P3] Follow up with Andrea on pre-auth tipping — Slack, 1d ago
5. 🔵 [P4] Read the new POS release notes — Notion, 3d ago

> 📋 +3 more items (1 normal, 2 low priority)
```

I don't open a list. The list opens itself. Every session starts with "here's what you owe people." It's impossible to forget.

### Auto-complete: I never check things off

When I reply to Sarah's email during a session, the agent recognizes that maps to to-do item #1 and marks it done automatically:

```
✅ Marked done: "Reply to Sarah's escalation email"
```

I didn't tell it to. It connected the action to the task and closed the loop. This is the part that makes it feel less like a system I'm fighting and more like a system that's working with me.

### Auto-reconcile: it cleans up after me

At the start of each session, the agent scans all connected sources — Slack sent messages, Gmail sent mail, Calendar events I attended — for evidence that open items were completed. If I replied to that email from my phone yesterday, the agent sees the sent message and marks the to-do done. Silently. No double-tracking.

## What I Learned

**The best to-do system is one you never touch.** Every to-do app assumes you'll maintain it. That assumption is wrong for people like me. The breakthrough was removing myself from the maintenance loop entirely. I'm the decision-maker, not the bookkeeper.

**Put tasks where you already look.** Calendar sync is the single highest-impact feature. I check my calendar 20 times a day. I check a to-do app maybe once. Meeting the user where they are — even when the user is yourself — is Product Management 101.

**Auto-capture beats manual capture every time.** The gap between "I should do this" and "I wrote this down" is where tasks die. Eliminating that gap by capturing at the source — in the same session where the request arrives — means nothing falls through.

**Proactive > reactive.** The old model: I go to my to-do list. The new model: my to-do list comes to me. Every session, every morning, every time something is due. The system is proactive, and I just respond.

**Simple storage, smart behaviors.** The whole thing is a JSON file. No database, no API, no sync service. All the intelligence is in the skill's behaviors — when to capture, how to prioritize, when to surface, when to close. The storage is dumb. The orchestration is smart.

---

*This pairs with [I Replaced My Morning Routine with a Single Command](./2026-03-05-start-of-day.md) — the to-do system plugs into the start-of-day skill as Section 0, surfacing open items before anything else.*

*[← Back to all thoughts](../thoughts/README.md) · [🧠 synthetic-mind](../README.md)*
