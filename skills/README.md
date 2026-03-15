# 🛠️ Skills Library

**59 AI agent skills built for Amp — covering productivity, development, data, communication, and more.**

Each skill lives in its own folder with a `SKILL.md` that Amp loads on demand. Skills are loaded via the `skill` tool or auto-routed by the `auto-pilot` skill.

---

## Quick Index

| # | Skill | Category | Description |
|---|-------|----------|-------------|
| 1 | [address-pr-comments](./address-pr-comments/) | 🔀 Git & PRs | Resolve GitHub PR review comments |
| 2 | [agent-browser](./agent-browser/) | 🌐 Browser & Web | Debug & interact with web apps via CLI |
| 3 | [airtable](./airtable/) | 📊 Data & Analytics | Manage Airtable bases, tables, and records |
| 4 | [android-emulator](./android-emulator/) | 📱 Mobile & Devices | Manage Android emulators (AVDs) |
| 5 | [auto-pilot](./auto-pilot/) | 🤖 Agent Behavior | Route requests to the correct skill(s) |
| 6 | [code-review-general](./code-review-general/) | 🔀 Git & PRs | Address PR code review feedback |
| 7 | [controlling-computer](./controlling-computer/) | 🖥️ System & macOS | Control Mac via AppleScript & shell |
| 8 | [converting-gdocs-to-markdown](./converting-gdocs-to-markdown/) | 📄 Documents | Convert Google Docs to markdown |
| 9 | [data-analyst](./data-analyst/) | 📊 Data & Analytics | Drive insightful visualizations and charts |
| 10 | [databricks](./databricks/) | 📊 Data & Analytics | Query Databricks Lakehouse via SQL |
| 11 | [datadog](./datadog/) | 📊 Data & Analytics | Query logs, metrics, traces, monitors, and RUM |
| 12 | [feedback-searcher](./feedback-searcher/) | 🔎 Research & Insights | Synthesize customer feedback across sources |
| 13 | [free-disk-space](./free-disk-space/) | 🖥️ System & macOS | Survey and clean up macOS disk space |
| 14 | [gcal](./gcal/) | 📆 Calendar & Scheduling | Schedule, manage & query calendar events |
| 15 | [gdrive](./gdrive/) | 📄 Documents | Google Drive, Docs, Sheets, and Slides |
| 16 | [gh-pr-read](./gh-pr-read/) | 🔀 Git & PRs | Read & summarize GitHub pull requests |
| 17 | [git-worktree](./git-worktree/) | 🔀 Git & PRs | Manage git worktrees for parallel branches |
| 18 | [gmail](./gmail/) | 💬 Communication | Search, read, send & manage emails |
| 19 | [historical-info](./historical-info/) | 🧠 Memory & Context | Find what you've been working on across sources |
| 20 | [ios-simulator](./ios-simulator/) | 📱 Mobile & Devices | Manage iOS simulators for testing |
| 21 | [kb-distill](./kb-distill/) | 🧠 Memory & Context | Distill raw observations into knowledge notes |
| 22 | [kb-promote](./kb-promote/) | 🧠 Memory & Context | Promote high-value notes into AGENTS.md rules |
| 23 | [kb-style-matrix](./kb-style-matrix/) | 🧠 Memory & Context | Build communication voice profile from Slack |
| 24 | [launchdarkly-cli](./launchdarkly-cli/) | 🧪 Experimentation | Manage feature flags via ldcli |
| 25 | [linear](./linear/) | 📋 Task & Project Management | Issue tracking & project management |
| 26 | [linear-to-execution](./linear-to-execution/) | 📋 Task & Project Management | Pick up a Linear issue for execution |
| 27 | [logging-feature-requests](./logging-feature-requests/) | 📝 Product | Log feature requests from Slack to sheet |
| 28 | [looker](./looker/) | 📊 Data & Analytics | Interact with Looker dashboards & queries |
| 29 | [memory](./memory/) | 🧠 Memory & Context | Persistent cross-session memory system |
| 30 | [notion](./notion/) | 📄 Documents | Read, search, create & update Notion pages |
| 31 | [plan-to-linear](./plan-to-linear/) | 📋 Task & Project Management | Convert structured plans into Linear issues |
| 32 | [pr-manager](./pr-manager/) | 🔀 Git & PRs | Commit, create & update PRs (supports Graphite) |
| 33 | [product](./product/) | 📝 Product | Search product docs & requirements |
| 34 | [project-status](./project-status/) | 📋 Task & Project Management | Gather project state across multiple sources |
| 35 | [prototype-builder](./prototype-builder/) | 🚀 Deployment | Scaffold interactive HTML prototypes |
| 36 | [push-pr](./push-pr/) | 🔀 Git & PRs | Push branch & create draft PR |
| 37 | [ralph-loop](./ralph-loop/) | 🔬 Methodology | Iterative two-model work-review loop |
| 38 | [rebasing-git-branches](./rebasing-git-branches/) | 🔀 Git & PRs | Rebase branches onto upstream target |
| 39 | [reflect](./reflect/) | ✍️ Writing & Content | Guided reflection coach for performance reviews |
| 40 | [reviewing-calendar](./reviewing-calendar/) | 📆 Calendar & Scheduling | Visual weekly calendar view with conflict detection |
| 41 | [rpi](./rpi/) | 🔬 Methodology | Research-Plan-Implement methodology router |
| 42 | [rpi-implement](./rpi-implement/) | 🔬 Methodology | Execute approved RPI plans phase by phase |
| 43 | [rpi-iterate](./rpi-iterate/) | 🔬 Methodology | Iterate on existing RPI plans with targeted updates |
| 44 | [rpi-plan](./rpi-plan/) | 🔬 Methodology | Create detailed, phased implementation plans |
| 45 | [rpi-research](./rpi-research/) | 🔬 Methodology | Research codebase for complex tasks before planning |
| 46 | [skill-management](./skill-management/) | 🤖 Agent Behavior | List, add, remove, inspect, and edit skills |
| 47 | [slack](./slack/) | 💬 Communication | Search, read & post Slack messages |
| 48 | [snagit](./snagit/) | 🖥️ System & macOS | Capture screenshots and recordings |
| 49 | [snowflake](./snowflake/) | 📊 Data & Analytics | Query Snowflake data warehouse via SQL |
| 50 | [spec-creator](./spec-creator/) | 📝 Product | Create and iterate on product specs |
| 51 | [start-of-day](./start-of-day/) | ⏰ Productivity | Morning triage of Slack, Gmail & Calendar |
| 52 | [summarize-video](./summarize-video/) | 📄 Documents | Summarize videos with transcript & quotes |
| 53 | [swarm](./swarm/) | 🔬 Methodology | Multi-perspective parallel exploration |
| 54 | [test-plan-creator](./test-plan-creator/) | 🧪 Testing | Create test plans & acceptance criteria |
| 55 | [todo](./todo/) | ⏰ Productivity | Persistent to-do list with proactive reminders and auto-capture |
| 56 | [viewing-figma-files](./viewing-figma-files/) | 🎨 Design | View, inspect & export Figma files |
| 57 | [web-research](./web-research/) | 🔎 Research & Insights | Search & synthesize external information |
| 58 | [writing-feedback](./writing-feedback/) | ✍️ Writing & Content | Write performance feedback (IBB model) |
| 59 | [writing-requirements-docs](./writing-requirements-docs/) | 📝 Product | Write PRDs from rough notes with evidence |

---

## By Category

### 🤖 Agent Behavior
- [auto-pilot](./auto-pilot/) — Route requests to the correct skill(s) automatically
- [skill-management](./skill-management/) — List, add, remove, inspect, and edit skills

### 🧠 Memory & Context
- [historical-info](./historical-info/) — Find what you've been working on across sources
- [kb-distill](./kb-distill/) — Distill raw observations into structured knowledge notes
- [kb-promote](./kb-promote/) — Promote high-value notes into AGENTS.md rules or new skills
- [kb-style-matrix](./kb-style-matrix/) — Build your communication voice profile from Slack
- [memory](./memory/) — Persistent cross-session memory with automatic capture

### 🔬 Methodology
- [ralph-loop](./ralph-loop/) — Iterative two-model work-review loop
- [rpi](./rpi/) — Research-Plan-Implement methodology router
- [rpi-implement](./rpi-implement/) — Execute approved RPI plans phase by phase
- [rpi-iterate](./rpi-iterate/) — Iterate on existing RPI plans with targeted updates
- [rpi-plan](./rpi-plan/) — Create detailed, phased implementation plans
- [rpi-research](./rpi-research/) — Research codebase for complex tasks before planning
- [swarm](./swarm/) — Multi-perspective parallel exploration with adversarial validation

### 🔀 Git & PRs
- [address-pr-comments](./address-pr-comments/) — Resolve GitHub PR review comments
- [code-review-general](./code-review-general/) — Address PR code review feedback
- [gh-pr-read](./gh-pr-read/) — Read and summarize GitHub pull requests
- [git-worktree](./git-worktree/) — Manage git worktrees for parallel branches
- [pr-manager](./pr-manager/) — Commit, create, and update PRs (supports Graphite)
- [push-pr](./push-pr/) — Push branch and create draft PR
- [rebasing-git-branches](./rebasing-git-branches/) — Rebase branches onto upstream target

### 📊 Data & Analytics
- [airtable](./airtable/) — Manage Airtable bases, tables, and records
- [data-analyst](./data-analyst/) — Drive insightful visualizations and charts
- [databricks](./databricks/) — Query Databricks Lakehouse via SQL
- [datadog](./datadog/) — Query logs, metrics, traces, monitors, and RUM
- [looker](./looker/) — Interact with Looker dashboards, queries, and explores
- [snowflake](./snowflake/) — Query Snowflake data warehouse via SQL

### 🧪 Experimentation
- [launchdarkly-cli](./launchdarkly-cli/) — Manage feature flags via ldcli

### 📱 Mobile & Devices
- [android-emulator](./android-emulator/) — Manage Android emulators (AVDs)
- [ios-simulator](./ios-simulator/) — Manage iOS simulators for testing

### 🚀 Deployment
- [prototype-builder](./prototype-builder/) — Scaffold interactive HTML prototypes

### 📝 Product
- [logging-feature-requests](./logging-feature-requests/) — Log feature requests from Slack to sheet
- [product](./product/) — Search product docs and requirements
- [spec-creator](./spec-creator/) — Create and iterate on product specs
- [writing-requirements-docs](./writing-requirements-docs/) — Write PRDs from rough notes with evidence

### 📋 Task & Project Management
- [linear](./linear/) — Issue tracking and project management
- [linear-to-execution](./linear-to-execution/) — Pick up a Linear issue for agent execution
- [plan-to-linear](./plan-to-linear/) — Convert structured plans into Linear issues
- [project-status](./project-status/) — Gather project state across multiple sources

### ✍️ Writing & Content
- [reflect](./reflect/) — Guided reflection coach for performance reviews
- [writing-feedback](./writing-feedback/) — Write performance feedback using IBB model

### 📄 Documents
- [converting-gdocs-to-markdown](./converting-gdocs-to-markdown/) — Convert Google Docs to markdown
- [gdrive](./gdrive/) — Google Drive, Docs, Sheets, and Slides
- [notion](./notion/) — Read, search, create, and update Notion pages
- [summarize-video](./summarize-video/) — Summarize videos with transcript and quotes

### 🌐 Browser & Web
- [agent-browser](./agent-browser/) — Debug and interact with web apps via CLI

### 🎨 Design
- [viewing-figma-files](./viewing-figma-files/) — View, inspect, and export Figma files

### 🧪 Testing
- [test-plan-creator](./test-plan-creator/) — Create test plans and acceptance criteria

### 💬 Communication
- [gmail](./gmail/) — Search, read, send, and manage emails
- [slack](./slack/) — Search, read, and post Slack messages

### 📆 Calendar & Scheduling
- [gcal](./gcal/) — Schedule, manage, and query calendar events
- [reviewing-calendar](./reviewing-calendar/) — Visual weekly calendar view with conflict detection

### 🖥️ System & macOS
- [controlling-computer](./controlling-computer/) — Control Mac via AppleScript and shell commands
- [free-disk-space](./free-disk-space/) — Survey and clean up macOS disk space
- [snagit](./snagit/) — Capture screenshots and recordings

### ⏰ Productivity
- [start-of-day](./start-of-day/) — Morning triage of Slack, Gmail, and Calendar
- [todo](./todo/) — Persistent to-do list with proactive reminders and auto-capture

### 🔎 Research & Insights
- [feedback-searcher](./feedback-searcher/) — Synthesize customer feedback across sources
- [web-research](./web-research/) — Search and synthesize external information

---

## How to Use

### Loading a skill

```
Use the `skill` tool to load any skill by name:
```

```json
{ "name": "auto-pilot" }
```

The `auto-pilot` skill is the default router — it reads your prompt and loads the right skill(s) automatically. You can also load skills directly by name.

### Skill anatomy

Each skill folder contains:

```
skill-name/
├── SKILL.md          # Frontmatter (name, description) + instructions
├── scripts/          # Optional helper scripts
└── resources/        # Optional reference files
```

The `SKILL.md` file uses YAML frontmatter with `name` and `description` fields, followed by markdown instructions that Amp loads into context.

### Adding a new skill

1. Create a folder under `skills/` with a `SKILL.md` file
2. Add routing in `auto-pilot/SKILL.md`
3. Add an entry to this README

---

*Last updated: March 2026*
