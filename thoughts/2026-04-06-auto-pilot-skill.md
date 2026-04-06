# I Stopped Telling My Agent Which Tool to Use

## TL;DR

The auto-pilot skill is a routing layer that sits between me and 97 AI skills. I describe what I want done, and it picks the right skill — or chains multiple skills together — without asking. It turned my agent from a toolbox into an assistant.

## Context

By late February, I had 30+ skills installed. Start-of-day, Slack, Gmail, Linear, Snowflake, PRD writing, code review. Each one worked great in isolation. The problem was me.

Every time I wanted something done, I had to remember which skill to use. "Search Slack" → load `slack`. "Check my calendar" → load `gcal`. "Draft a PRD" → load `prd-draft`. It felt like having a car where you manually engage each gear, every time, from a 97-option menu.

So I built a skill whose only job is picking the right skill.

## How It Works

Auto-pilot has three pieces:

### 1. Intent parsing

When I say something like "find the Linear ticket for cash rounding and post it to Slack," auto-pilot breaks that into two intents: search Linear, then post to Slack. No fancy NLP — the agent's language model handles the parsing natively.

### 2. Routing tables

A `routing-tables.md` file maps intents to skills across every domain:

| Intent | Skill |
|--------|-------|
| Search/read/draft email | `gmail` |
| Calendar: schedule, check, RSVP | `gcal` |
| Linear issues: create, update, search | `linear` |
| Snowflake SQL queries | `snowflake` |
| Draft PRD / feature spec | `prd-draft` |
| Project status / recap | `project-status` |
| Deploy static site | `blockcell` |

There are 100+ entries across communication, project management, code, data, infrastructure, testing, product, strategy, and prototyping. The table is the skill's brain — everything else is just execution logic.

### 3. Execution protocol

Five steps, every time:

1. **Parse intent** — what does the user want done?
2. **Select skill(s)** — match against routing tables
3. **Load skill** — pull the right SKILL.md into context
4. **Execute** — follow the skill's instructions
5. **Chain if needed** — load additional skills for multi-domain tasks

The key principle: **don't ask which skill to use.** The agent decides. Only ask for genuinely missing data — a merchant ID the user hasn't mentioned, a date range that's ambiguous.

## The Chaining Part

This is where it gets interesting. Most of my real work spans multiple tools:

- "Check if the cash rounding flag is ramped, and if so, update the Blueprint project status" → `launchdarkly-cli` → `blueprint-project-update`
- "Find yesterday's Slack thread about neighborhoods and create a Linear ticket" → `slack` → `linear`
- "Pull the checkout completion rate from Snowflake and draft a status update for the team" → `snowflake` → `status-update`

Auto-pilot handles these by loading skills sequentially, passing context from one to the next. The output of the Snowflake query becomes the input for the status update. No manual copy-pasting between tools.

## Active vs. Archived Skills

With 97 skills, loading all of them into context would be wasteful. So there are two tiers:

- **Active** (`~/.agents/skills/`) — always available, loaded via the `skill` tool
- **Archived** (`~/.agents/skills-archive/`) — loaded on demand by reading the SKILL.md directly

Frequently used skills stay active. Rarely used ones get archived. Auto-pilot knows where each one lives and loads from the right place.

## The Safety Valve

There's one important guardrail: if the request is ambiguous enough that routing to the wrong skill would cause **unrecoverable side effects** — posting to a public Slack channel vs. sending a private email, for example — auto-pilot stops and asks to clarify. It prefers action over clarification, but not at the cost of sending the wrong message to the wrong place.

## What I Learned

**Routing tables beat AI reasoning for skill selection.** I tried letting the agent "figure out" which skill to use based on descriptions alone. It worked 80% of the time. The routing table brought it to 99%. Explicit mappings beat fuzzy matching for production workflows.

**The real value is chaining, not routing.** Single-skill tasks are easy — I could just load the skill myself. The magic is when auto-pilot chains three skills together for a task I would have done in three separate sessions before.

**Maintenance is the cost.** Every new skill needs a routing table entry. Every renamed skill needs an update. It's a small tax, but it's non-zero. I've automated most of it — new skill installs auto-add to the routing table — but it's worth knowing the trade-off.

**You need boundaries elsewhere.** Auto-pilot decides *what* to do, but `AGENTS.md` decides *how* to do it. The boundaries section ("ask before posting to Slack," "preview emails before sending") acts as the safety net. Without it, auto-pilot would be dangerously efficient.

---

*[← Back to all thoughts](../thoughts/README.md) · [🧠 synthetic-mind](../README.md)*
