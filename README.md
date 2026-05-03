# 🧠 synthetic-mind

AI thoughts, processes, skills, and experiments — a showcase of AI-augmented work.

**By [Abhi Basu](https://github.com/abhiroopb)**

---

## What is this?

A living collection of learnings from working deeply with AI agents, LLMs, and automation. Each entry captures something useful: a workflow that clicked, a control-plane decision that made the system sturdier, or a skill worth reusing.

Built primarily with [Amp](https://ampcode.com), these skills and routines power a PM's daily workflow, from morning triage to PRD writing to data analysis to deploying prototypes. Everything here is real, battle-tested, and actively used.

## Featured Project: The AI PM OS

One of the bigger things I've built recently is **the AI PM OS**: a control plane for product work built around AI agents, durable workstream context, and a clear ownership model for how the system behaves.

The current version is organized around a few durable ideas:

- repo-owned behavior in `AGENTS.md`, with home-directory files kept thin and adapter-like
- a Chief of Staff agent that decides what deserves focus today
- workstream folders with persistent `CONTEXT.md` files and live source snapshots
- `cmux` workspaces that spin up in parallel and resume from file-based state
- a lightweight state layer that can be rebuilt instead of trusted blindly
- an archive-backed skill model, where specialized skills can stay off the hot path until they are needed
- routines for meetings, comms triage, and recurring PM operations

If you want the overview first:

- **Landing page:** [Overview of the AI PM OS](https://abhiroopb.github.io/synthetic-mind/ai-pm-os/)
- **Repo:** [abhiroopb/ai-pm-os](https://github.com/abhiroopb/ai-pm-os)
- **Thoughts:** [the control plane model](./thoughts/2026-05-03-how-i-turned-my-ai-setup-into-a-real-control-plane.md), [what it is](./thoughts/2026-04-12-ai-pm-os.md), [how it works](./thoughts/2026-04-12-how-ai-pm-os-works.md), [why it matters](./thoughts/2026-04-12-why-ai-pm-os-is-powerful.md)

## Structure

| Directory | Contents |
|-----------|----------|
| **[`/skills`](./skills)** | 100 AI agent skills — [browse the full catalog →](./skills/README.md) |
| **[`/thoughts`](./thoughts)** | Write-ups on AI workflows, observations, and takeaways |
| **[`/processes`](./processes)** | Documented processes for AI-augmented work |

## Skills at a Glance

**100 public skills**, organized as a working system rather than a flat pile of prompts:

| Area | What it covers |
|------|----------------|
| **Control plane** | `auto-pilot`, memory, distillation, final judgment, and the routing layer that keeps the environment coherent |
| **Daily PM loops** | start-of-day, closing-day, syncing-context, project status, roadmap intake, comms triage |
| **Execution workflows** | RPI planning and implementation, PR management, CI repair, repo cloning, cloud workstations |
| **Data and validation** | Snowflake, Databricks, Looker, Datadog, LaunchDarkly, feature validation |
| **Comms and docs** | Slack, Gmail, Google Drive, Notion, drafting-docs, manager summaries, writing feedback |
| **Specialists** | Merchant lookup, code search, protos, release tracking, ecommerce research, mobile simulators, browser automation |

**[Browse the full catalog →](./skills/README.md)**

## What makes this different

These aren't toy examples. Each skill is:

- **Production-grade** — YAML frontmatter, reference docs, helper scripts, setup guides
- **Composable** — Skills call other skills. `auto-pilot` routes to the right one automatically
- **Battle-tested** — Used daily across product management, data analysis, and engineering workflows
- **Sanitized** — Enterprise-pattern skills have all internal references stripped and replaced with generic placeholders, so you can adapt the patterns for your own environment

## How to use these skills

Each skill is an [Amp](https://ampcode.com) skill module. To use one:

```bash
amp skills add <path-to-skill-folder>
```

Or clone the repo and point Amp at the `skills/` directory. The `auto-pilot` skill will automatically route your requests to the right skill.

## Changelog

| Date | Update |
|------|--------|
| 2026-05-03 | 📝 New thought: [How I Turned My AI Setup Into a Real Control Plane](./thoughts/2026-05-03-how-i-turned-my-ai-setup-into-a-real-control-plane.md) — the ownership model behind repo policy, home adapters, and archive-backed specialization |
| 2026-05-03 | 📝 New thought: [The Prepare-Then-Approve Pattern](./thoughts/2026-05-03-the-prepare-then-approve-pattern.md) — why bounded corroboration and prebuilt follow-through beats letting agents act first |
| 2026-05-03 | 🧹 Site refresh: homepage, AI PM OS overview, and skills front door now reflect the control-plane story and current 100-skill public catalog |
| 2026-04-21 | 📝 New thought: [Start, Sync, Close: The AI Work Loop I Actually Needed](./thoughts/2026-04-21-start-sync-close-loop.md) — why the AI PM OS only started feeling stable once the workflow covered the middle and the end of the day too |
| 2026-04-21 | 🆕 New skill: [checking-your-lens](./skills/checking-your-lens/) — a lightweight final judgment pass for making AI output sound more grounded, direct, and context-aware |
| 2026-04-22 | 🆕 2 new skills: [closing-day](./skills/closing-day/) and [syncing-context](./skills/syncing-context/) — small but useful PM OS loops for wrapping the day and refreshing the lightweight state layer |
| 2026-04-21 | 🆕 AI PM OS refresh: public repo now includes repo-local context-sync and closing-day workflows, and the overview page reflects the full start → sync → close loop |
| 2026-04-12 | 🆕 The AI PM OS landing page: [overview](https://abhiroopb.github.io/synthetic-mind/ai-pm-os/) — how the system works, what it automates, and how to install it |
| 2026-04-12 | 📝 New thought: [I Built an AI PM OS](./thoughts/2026-04-12-ai-pm-os.md) — what the system is and why I built it |
| 2026-04-12 | 📝 New thought: [How the AI PM OS Spins Up My Entire Workday](./thoughts/2026-04-12-how-ai-pm-os-works.md) — the mechanics behind the command center, workstreams, and routines |
| 2026-04-12 | 📝 New thought: [Why the AI PM OS Feels More Powerful Than a Chatbot](./thoughts/2026-04-12-why-ai-pm-os-is-powerful.md) — why durable context plus orchestration changes the experience |
| 2026-04-03 | 🆕 21 new skills: blox, blueprint-project-status, blueprint-project-update, blueprint-status-update, check-ci, cloning-squareup-repos, dev-guides, drafting-docs, ecom-great-stores, ecom-research, eng-ai-chat, go-link, hermit, jira, manager-slack-summary, monitoring-prs, protos, slack-saved-triage, staging-account-builder, trust-feature-validation, weekly-status-summary |
| 2026-03-24 | 📝 New thought: [How I Automated Every Workflow with AI Skills](./thoughts/2026-03-24-automating-workflows-with-ai-skills.md) — a practical guide to building 35+ AI agent skills for morning triage, email, project management, and more |
| 2026-03-24 | 📝 New thought: [We Built an AI Skill That Writes Product Requirements Docs](./thoughts/2026-03-24-writing-requirements-docs.md) — how a team went from markdown-first specs to an agent skill that writes PRDs with auto-referenced internal sources |
| 2026-03-23 | 📝 New thought: [Cutting 80% of the Noise from My AI Memory System](./thoughts/2026-03-23-amp-mem-noise-reduction.md) — 7 plugin changes that cut observation volume by ~80% while preserving signal |
| 2026-03-23 | 🆕 6 new skills: enterprise-search, feature-request-scanner, roadmap-intake, graphql-schema-discovery, communication-coach, merchant-lookup |
| 2026-03-14 | 📝 New thought: [I Stopped Maintaining My To-Do List and Let the Agent Do It](./thoughts/2026-03-14-todo-system.md) — a proactive to-do system that auto-captures, prioritizes, and syncs to calendar |
| 2026-03-14 | 🆕 New skill: [todo](./skills/todo/) — persistent to-do list with proactive reminders and auto-capture |
| 2026-03-11 | 🐛 New thought: [When Your Plugin Works but Nothing Happens](./thoughts/2026-03-11-debugging-the-dollar-api.md) — debugging silent failures in Amp's `$` API |
| 2026-03-11 | 📝 New thought: [The Signal-to-Noise Problem in AI Memory](./thoughts/2026-03-11-tuning-memory-noise.md) — tuning amp-mem's context injection |
| 2026-03-05 | 🚀 Initial release — 98 skills uploaded, categorized, and indexed |
| 2026-03-05 | 🔒 Secrets scrubbed (OAuth credentials, API tokens) |
| 2026-03-05 | 🧹 54 enterprise skills sanitized — all internal URLs, brand names, Slack channels, Snowflake tables, and proprietary tool references replaced with generic placeholders |
| 2026-03-05 | 📚 Unified all skills into single `/skills` directory with full categorized README |

## License

MIT
