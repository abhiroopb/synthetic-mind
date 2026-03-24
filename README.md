# 🧠 synthetic-mind

AI thoughts, processes, skills, and experiments — a showcase of AI-augmented work.

**By [Abhi Basu](https://github.com/abhiroopb)**

---

## What is this?

A living collection of learnings from working deeply with AI agents, LLMs, and automation. Each entry captures something useful — a workflow that clicked, a skill that shipped, or a process worth sharing.

Built primarily with [Amp](https://ampcode.com), these skills power a PM's daily workflow — from morning triage to PRD writing to data analysis to deploying prototypes. Everything here is real, battle-tested, and actively used.

## Structure

| Directory | Contents |
|-----------|----------|
| **[`/skills`](./skills)** | 105 AI agent skills — [browse the full catalog →](./skills/README.md) |
| **[`/thoughts`](./thoughts)** | Write-ups on AI workflows, observations, and takeaways |
| **[`/processes`](./processes)** | Documented processes for AI-augmented work |

## Skills at a Glance

**105 skills** across 20+ categories:

| Category | Skills | Examples |
|----------|--------|----------|
| 🤖 **Agent Behavior** | 3 | Auto-pilot routing, swarm exploration, requirement clarification |
| 🧠 **Memory & Context** | 5 | Cross-session memory, knowledge distillation, voice profiling |
| 🔬 **Methodology** | 7 | RPI (Research → Plan → Implement), multi-model review loops |
| 📊 **Data & Analytics** | 8 | Snowflake, Databricks, Looker, Datadog, Airtable |
| 🔀 **Git & PRs** | 8 | PR creation, code review, rebasing, stacked PRs, worktrees |
| 📝 **Product** | 7 | PRDs, specs, feature requests, feedback tracking |
| 💬 **Communication** | 3 | Slack, Gmail, email triage |
| ✍️ **Writing** | 4 | Brand voice, communication coaching, performance feedback |
| 📄 **Documents** | 4 | Google Drive, Notion, video summaries, doc conversion |
| 🧪 **Experimentation** | 3 | A/B testing, LaunchDarkly flags, flag evaluation |
| 📱 **Mobile** | 5 | iOS/Android simulators, app builds, release trains |
| 🚀 **Deployment** | 4 | Static sites, staging environments, prototypes |
| 🔍 **Search** | 7 | Code search, enterprise knowledge, employee directory |
| 📋 **Project Mgmt** | 5 | Linear, task creation, project status aggregation |
| 🧪 **Testing** | 4 | Test accounts, test plans, QA docs |
| 🔧 **Infrastructure** | 4 | Permissions, service registry, audience segments |
| 🖥️ **System** | 3 | macOS control, disk cleanup, screenshots |
| 🎨 **Design** | 1 | Figma file inspection |
| + more | 13 | Calendar, CI/CD, browser automation, web research, etc. |

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
| 2026-03-24 | 📝 New thought: [How I Automated Every Workflow with AI Skills](./thoughts/2026-03-24-automating-workflows-with-ai-skills.md) — a practical guide to building 35+ AI agent skills for morning triage, email, project management, and more |
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
