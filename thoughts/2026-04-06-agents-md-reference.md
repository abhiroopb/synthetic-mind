# The File That Runs My Entire AI Setup

## TL;DR

I published a sanitized version of my `AGENTS.md` — the single file that configures how my AI agent behaves across 76+ skills. It defines my identity, session startup routine, memory system, to-do automation, output preferences, and tool routing. If you want to build your own AI-powered workflow, this is the blueprint.

## Context

Every time I talk about my AI setup — the [start-of-day skill](./2026-03-05-start-of-day.md), the [memory system](./2026-03-05-building-amp-mem.md), the [76 skills](./2026-03-24-automating-workflows-with-ai-skills.md) — people ask the same question: "Where does all the configuration live?"

One file. `AGENTS.md` in my project root.

It's not a config file in the traditional sense. It's a markdown document that the agent reads at the start of every session. Think of it as a combination of a `.bashrc`, a runbook, and a personality profile — except it's written in plain English.

## What's In It

Here's the structure, section by section:

### Identity

```markdown
- Name: Abhi Basu
- Team: Profiles (Online Ordering)
- Working folder: /Development
```

This is how the agent knows who it's working for. It affects tone, Slack attribution, email signatures, and which projects to prioritize.

### Session Start

Seven steps that run silently every time a session begins:

1. Check VPN connection
2. Load the to-do list and surface open items
3. Check if memory needs distillation
4. Check if communication style profile is stale
5. Run start-of-day if it hasn't run in 12 hours
6. Load skills and warm up MCP servers
7. Set the terminal tab title to the current task

The agent doesn't ask permission for any of these. They just happen. The session is ready to work by the time I type my first message.

### Memory System

The [amp-mem plugin](./2026-03-05-building-amp-mem.md) runs passively in the background:

- **Passive capture** — watches tool results from Slack, Gmail, Linear, etc. Uses AI gating (probability > 0.65) to decide what's worth saving.
- **Noise filtering** — ignores read-only tools, short commands, and noisy operations.
- **Pattern learning** — after 3+ repeated actions across sessions, proposes codifying it as a rule in AGENTS.md itself.

The memory system is self-improving. The more I use it, the smarter the file gets.

### To-Do System

The [to-do system](./2026-03-14-todo-system.md) is fully automated:

- **Auto-capture** from conversations, Slack, email, Linear
- **Auto-reconcile** at session start — checks if items were already completed
- **Auto-complete** when I finish something during a session
- **Calendar sync** — future items get 15-minute calendar blocks, color-coded by priority

I haven't manually added a to-do item in weeks. The agent captures them as they come up.

### Boundaries

This is the part most people skip, and it's the most important:

```markdown
✅ Always: Use skills before raw tool calls
⚠️ Ask first: Modifying AGENTS.md, posting to Slack, sending emails
🚫 Never: Commit secrets, send emails without preview
```

Without boundaries, the agent will do too much. The `Ask first` tier is critical — it means I stay in the loop on anything that goes out to other people.

### Tool Preferences

This section is where I encode my workflow opinions:

- Enterprise search first, Slack/web search as fallback
- Snowflake over Databricks for data queries
- Google Docs via gdrive, never local files
- "Add to backlog" means the roadmap tool, not the sprint tracker

These sound trivial, but they eliminate a whole category of "did you mean..." back-and-forth. The agent just knows.

## Why This Works

Three reasons:

**1. It's plain English.** No YAML schema to learn. No special syntax. The agent reads markdown and follows instructions. If I want to change a behavior, I edit a sentence.

**2. It's self-reinforcing.** The memory system watches my corrections and proposes new rules. When I say "don't use emdashes" three times, it suggests adding that to Output Preferences. The file evolves with my habits.

**3. It's the single source of truth.** Every skill, every session, every workstream reads this file. There's no drift between "how the agent should behave" and "how the agent actually behaves" because there's only one place to look.

## Get the File

The full sanitized reference is here: **[agents-md-reference.md](../agents-md-reference.md)**

All internal URLs, proprietary tool names, and company-specific references have been replaced with generic placeholders. The structure and logic are exactly what I use every day.

To use it:

1. Copy it to your project root as `AGENTS.md`
2. Replace the identity section with your info
3. Remove sections you don't need yet (start with Identity, Boundaries, and Output Preferences)
4. Add sections as your workflow evolves

You don't need all 76 skills to get value from this. Even with just the identity and boundaries sections, your agent sessions will feel noticeably more consistent.

## What I Learned

**Start small.** My first AGENTS.md was 10 lines: name, team, and "be concise." Everything else grew organically from corrections and preferences I noticed repeating.

**Boundaries matter more than capabilities.** The `Never` and `Ask first` sections prevent more problems than all the other sections combined. An agent that does too much is worse than one that does too little.

**The file is never done.** I edit it 2-3 times a week. It's a living document that reflects how I actually work, not how I think I should work. That's the whole point.

---

*[← Back to all thoughts](../thoughts/README.md) · [🧠 synthetic-mind](../README.md)*
