# Automating Every PM Workflow with AI Agent Skills

## TL;DR

I built 35+ custom skills for [Amp](https://ampcode.com) that automate everything from morning triage to email replies to project status reports. I'm a PM, not an engineer. Here's how the system works and how you can build your own.

## Context

I spend my days as a PM doing a lot of operational work — checking email, triaging Slack, updating Linear tickets, writing status reports, scanning channels for feature requests. Important work, but repetitive. I wanted to spend more time *thinking about product* and less time doing the busywork around it.

The insight: AI coding agents like Amp can do way more than write code. They can read your Slack, draft your emails, manage your calendar, triage your inbox, and update your project tracker — if you teach them how. That's what skills are. Markdown files that teach an agent a workflow.

## The System

Four pieces make it all work.

### 1. AGENTS.md — The Brain

This is the instruction manual for your agent. It defines who you are, what you care about, how you want output formatted, and what should happen at session start. Think of it as your agent's personality and preferences file.

A simplified version looks like this:

```markdown
# Identity
You are an AI assistant for a product manager.

# Preferences
- Be concise. No fluff.
- Default to action over asking permission.
- When triaging, surface only what needs my attention.

# Session Startup
1. Load memory for context
2. Check to-do list
3. Surface anything urgent
```

Every session, the agent reads this first. It's the foundation everything else builds on.

### 2. Skills — Modular Automation

Each skill is a `SKILL.md` file with instructions for a specific workflow. I organize mine into categories:

| Category | Skills | What They Do |
|----------|--------|-------------|
| **Morning triage** | `start-of-day` | Triages Slack unreads, Gmail inbox, Calendar, GitHub PRs, Figma/Drive/Linear/Notion notifications. One command, full inbox zero. |
| **Communication** | `slack`, `gcal`, `gmail` | Read/write Slack, manage calendar events, draft email replies |
| **Project management** | `linear`, `plan-to-linear`, `project-status`, `todo` | Create/manage issues, aggregate status from Slack + GitHub + Drive + feature flags, auto-capture action items |
| **Knowledge** | `memory`, `kb-distill`, `kb-promote` | Persistent cross-session memory, compress observations into structured notes, promote patterns into permanent rules |
| **Product** | `feature-request-scanner`, `launch-a-product` | Daily scans of feedback channels for feature requests, GTM readiness checks |
| **Meta** | `auto-pilot`, `skill-management`, `building-skills` | Auto-routing, self-management, creating new skills |

Each skill is self-contained. You can use one skill or thirty — they compose but don't depend on each other.

### 3. Auto-Pilot — The Router

This is the skill that changed everything. Instead of remembering which skill does what, I just say what I need and `auto-pilot` routes it to the right skill automatically. "Scan my inbox" → `start-of-day`. "Log this feature request" → `feature-request-scanner`. "What's the status of Project X?" → `project-status`.

One entry point for everything.

### 4. Memory — The Glue

I built a persistent memory system backed by SQLite + FTS5 (full-text search). No vector DB, no infra to manage. It passively captures decisions, preferences, and context during every session. When a new session starts, relevant memories get loaded automatically.

This is what makes the agent feel like it *knows you*. It remembers that you prefer bullet points over paragraphs, that Project X ships on Thursday, that you already replied to that email thread yesterday.

### 5. To-Do System

Action items get auto-captured from Slack messages, Gmail, Calendar events, and Linear tickets. They sync to Google Calendar so I see them on my phone. At session start, the agent surfaces what's due. Nothing falls through cracks.

## How to Build Your Own

1. **Start with AGENTS.md.** Define who you are and what you want automated. Even five lines makes a difference.
2. **Build your first skill.** Pick the workflow you repeat most. I'd suggest `start-of-day` — morning triage is universal and the ROI is immediate.
3. **Add auto-pilot routing.** Write one routing skill so you stop needing to invoke skills by name.
4. **Add memory.** Even a simple SQLite store that captures key decisions changes everything about session continuity.
5. **Let skills compose.** `start-of-day` calls `slack`, `gmail`, `gcal`, and `todo`. `project-status` pulls from Slack, GitHub, Drive, Linear, and feature flags. Skills calling skills is where it gets powerful.

## What I Learned

**The compound effect is real.** Each skill makes every other skill more useful. Memory makes triage smarter. Triage feeds the to-do list. The to-do list informs project status. It snowballs.

**Start with the workflow you hate most.** That's where you'll feel the impact fastest and stay motivated to build more.

**Skills don't need to be perfect.** They need to save you five minutes a day. That's 20 hours a year per skill. Multiply by 35.

**The agent learns your preferences over time** — but only if you give it memory. Without persistence, every session starts from zero.

**Non-engineers can build this.** SKILL.md files are just markdown instructions. If you can write a checklist, you can write a skill. The agent does the hard part.

---

*The best automation isn't the one that replaces you. It's the one that gives you back the time to do the work only you can do.*
