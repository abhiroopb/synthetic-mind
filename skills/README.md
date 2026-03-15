# 🛠️ Skills Library

**99 AI agent skills built for Amp — covering productivity, development, data, communication, and more.**

Each skill lives in its own folder with a `SKILL.md` that Amp loads on demand. Skills are loaded via the `skill` tool or auto-routed by the `auto-pilot` skill.

---

## Quick Index

| # | Skill | Category | Description |
|---|-------|----------|-------------|
| 1 | [address-pr-comments](./address-pr-comments/) | 🔀 Git & PRs | Resolve GitHub PR review comments |
| 2 | [agent-browser](./agent-browser/) | 🌐 Browser & Web | Debug & interact with web apps via CLI |
| 3 | [airtable](./airtable/) | 📊 Data & Analytics | Manage Airtable bases, tables, and records |
| 4 | [android-emulator](./android-emulator/) | 📱 Mobile & Devices | Manage Android emulators (AVDs) |
| 5 | [ask-questions-if-underspecified](./ask-questions-if-underspecified/) | 🤖 Agent Behavior | Clarify requirements before implementing |
| 6 | [auto-pilot](./auto-pilot/) | 🤖 Agent Behavior | Route requests to the correct skill(s) |
| 7 | [block-data](./block-data/) | 📊 Data & Analytics | Query business metrics and dashboards |
| 8 | [block-writing](./block-writing/) | ✍️ Writing & Content | Brand voice for product content |
| 9 | [blockcell](./blockcell/) | 🚀 Deployment | Deploy static sites for internal sharing |
| 10 | [cash](./cash/) | 📱 Mobile Development | Cash App iOS & Android dev CLI |
| 11 | [cash-rounding-responder](./cash-rounding-responder/) | 💬 Communication | Triage & reply to team inbox emails |
| 12 | [code-review-general](./code-review-general/) | 🔀 Git & PRs | Address PR code review feedback |
| 13 | [codesearch](./codesearch/) | 🔍 Search & Discovery | Search Sourcegraph across all repos |
| 14 | [controlling-computer](./controlling-computer/) | 🖥️ System & macOS | Control Mac via AppleScript & shell |
| 15 | [converting-gdocs-to-markdown](./converting-gdocs-to-markdown/) | 📄 Documents | Convert Google Docs to markdown |
| 16 | [create-permission](./create-permission/) | 🔧 Infrastructure | Create/modify permissions end-to-end |
| 17 | [creating-builderbot-tasks](./creating-builderbot-tasks/) | 📋 Task & Project Management | Create tasks via CLI with labels & status |
| 18 | [creating-experiments](./creating-experiments/) | 🧪 Experimentation | Set up A/B experiments & flag patterns |
| 19 | [data-analyst](./data-analyst/) | 📊 Data & Analytics | Drive visualizations with follow-up Qs |
| 20 | [databricks](./databricks/) | 📊 Data & Analytics | Query Databricks Lakehouse via SQL |
| 21 | [datadog](./datadog/) | 📊 Data & Analytics | Query logs, metrics, traces, and monitors |
| 22 | [deploying-prd-prototypes](./deploying-prd-prototypes/) | 🚀 Deployment | Deploy prototypes from PRDs to hosting |
| 23 | [dev-guides](./dev-guides/) | 🔍 Search & Discovery | Search & retrieve internal dev docs |
| 24 | [device-settings-audit](./device-settings-audit/) | 🔍 Audit & Compliance | Query device profile change history |
| 25 | [ditto](./ditto/) | 🧪 Testing | Provision & manage staging test accounts |
| 26 | [early-feature-access](./early-feature-access/) | 📝 Product | Add features to Early Feature Access page |
| 27 | [eng-ai-chat](./eng-ai-chat/) | 🔍 Search & Discovery | Search internal engineering knowledge |
| 28 | [feature-overview-updater](./feature-overview-updater/) | 📝 Product | Regenerate feature README index tables |
| 29 | [feedback-searcher](./feedback-searcher/) | 🔎 Research & Insights | Synthesize customer feedback across sources |
| 30 | [flag-simulator](./flag-simulator/) | 🧪 Experimentation | Evaluate LaunchDarkly flags via API |
| 31 | [free-disk-space](./free-disk-space/) | 🖥️ System & macOS | Survey & clean up macOS disk space |
| 32 | [gcal](./gcal/) | 📆 Calendar & Scheduling | Schedule, manage & query calendar events |
| 33 | [gdrive](./gdrive/) | 📄 Documents | Google Drive, Docs, Sheets, and Slides |
| 34 | [gh-pr-read](./gh-pr-read/) | 🔀 Git & PRs | Read & summarize GitHub pull requests |
| 35 | [git-worktree](./git-worktree/) | 🔀 Git & PRs | Manage git worktrees for parallel branches |
| 36 | [glean](./glean/) | 🔍 Search & Discovery | Search enterprise knowledge & people |
| 37 | [gmail](./gmail/) | 💬 Communication | Search, read, send & manage emails |
| 38 | [go-link](./go-link/) | 🔗 Navigation | Resolve internal go/ shortlinks to URLs |
| 39 | [historical-info](./historical-info/) | 🧠 Memory & Context | Find what you've been working on |
| 40 | [ios-simulator](./ios-simulator/) | 📱 Mobile & Devices | Manage iOS simulators for testing |
| 41 | [jack-guidance](./jack-guidance/) | ✍️ Writing & Content | Concise, direct communication coaching |
| 42 | [kb-distill](./kb-distill/) | 🧠 Memory & Context | Distill observations into knowledge notes |
| 43 | [kb-promote](./kb-promote/) | 🧠 Memory & Context | Promote notes into AGENTS.md rules |
| 44 | [kb-style-matrix](./kb-style-matrix/) | 🧠 Memory & Context | Build communication voice profile |
| 45 | [kochiku](./kochiku/) | ⚙️ CI/CD | Fetch CI build data, logs & artifacts |
| 46 | [launchdarkly-cli](./launchdarkly-cli/) | 🧪 Experimentation | Manage feature flags via ldcli |
| 47 | [linear](./linear/) | 📋 Task & Project Management | Issue tracking & project management |
| 48 | [linear-to-execution](./linear-to-execution/) | 📋 Task & Project Management | Pick up a Linear issue for execution |
| 49 | [logging-feature-requests](./logging-feature-requests/) | 📝 Product | Log feature requests from Slack to sheet |
| 50 | [looker](./looker/) | 📊 Data & Analytics | Interact with Looker dashboards & queries |
| 51 | [market-react](./market-react/) | 🖥️ Frontend | Market React design system components |
| 52 | [memory](./memory/) | 🧠 Memory & Context | Persistent cross-session memory system |
| 53 | [merchant-factory](./merchant-factory/) | 🧪 Testing | Create staging test merchant accounts |
| 54 | [mobile-releases](./mobile-releases/) | 📱 Mobile Development | Browse & install mobile app builds |
| 55 | [mode-settings-audit](./mode-settings-audit/) | 🔍 Audit & Compliance | Audit Mode Analytics workspace settings |
| 56 | [navigation](./navigation/) | 🖥️ Frontend | Add/update Dashboard nav menu links |
| 57 | [notion](./notion/) | 📄 Documents | Read, search, create & update Notion pages |
| 58 | [people-api](./people-api/) | 🔍 Search & Discovery | Query employee directory & org data |
| 59 | [plan-to-linear](./plan-to-linear/) | 📋 Task & Project Management | Convert plans into Linear issues |
| 60 | [playpen](./playpen/) | 🚀 Deployment | Deploy & debug in ephemeral staging pods |
| 61 | [pos-releases](./pos-releases/) | 📱 Mobile Development | Query POS release trains & schedules |
| 62 | [pr-manager](./pr-manager/) | 🔀 Git & PRs | Commit, create & update PRs |
| 63 | [product](./product/) | 📝 Product | Search product docs & requirements |
| 64 | [project-status](./project-status/) | 📋 Task & Project Management | Gather project state across sources |
| 65 | [prototype-builder](./prototype-builder/) | 🚀 Deployment | Scaffold interactive HTML prototypes |
| 66 | [push-pr](./push-pr/) | 🔀 Git & PRs | Push branch & create draft PR |
| 67 | [query-expert](./query-expert/) | 📊 Data & Analytics | Discover tables & run Snowflake SQL |
| 68 | [ralph-loop](./ralph-loop/) | 🔬 Methodology | Iterative two-model work-review loop |
| 69 | [rebasing-git-branches](./rebasing-git-branches/) | 🔀 Git & PRs | Rebase branches onto upstream target |
| 70 | [reflect](./reflect/) | ✍️ Writing & Content | Guided reflection coach for reviews |
| 71 | [registry-api](./registry-api/) | 🔧 Infrastructure | Query service registry via Python API |
| 72 | [registry-info](./registry-info/) | 🔧 Infrastructure | Look up service metadata & ownership |
| 73 | [regulator](./regulator/) | 🔍 Search & Discovery | Search merchant accounts & payments |
| 74 | [requesting-pr-reviews-from-owners](./requesting-pr-reviews-from-owners/) | 🔀 Git & PRs | Track & request PR review approvals |
| 75 | [reviewing-calendar](./reviewing-calendar/) | 📆 Calendar & Scheduling | Visual weekly calendar view with conflicts |
| 76 | [rpi](./rpi/) | 🔬 Methodology | Research-Plan-Implement task router |
| 77 | [rpi-implement](./rpi-implement/) | 🔬 Methodology | Execute approved RPI plans phase by phase |
| 78 | [rpi-iterate](./rpi-iterate/) | 🔬 Methodology | Iterate on RPI plans with updates |
| 79 | [rpi-plan](./rpi-plan/) | 🔬 Methodology | Create detailed implementation plans |
| 80 | [rpi-research](./rpi-research/) | 🔬 Methodology | Research codebase before planning |
| 81 | [saving-cash-rounding-feedback](./saving-cash-rounding-feedback/) | 📝 Product | Save customer feedback to tracking doc |
| 82 | [seller-snapshot](./seller-snapshot/) | 🔍 Search & Discovery | Generate merchant 360° snapshot |
| 83 | [setting-up-builderbot](./setting-up-builderbot/) | 🔧 Setup & Config | Guide CLI tool setup & configuration |
| 84 | [skill-management](./skill-management/) | 🤖 Agent Behavior | List, add, remove & inspect skills |
| 85 | [slack](./slack/) | 💬 Communication | Search, read & post Slack messages |
| 86 | [snagit](./snagit/) | 🖥️ System & macOS | Capture screenshots & recordings |
| 87 | [snowflake](./snowflake/) | 📊 Data & Analytics | Query Snowflake data warehouse via SQL |
| 88 | [spec-creator](./spec-creator/) | 📝 Product | Create & iterate on product specs |
| 89 | [start-of-day](./start-of-day/) | ⏰ Productivity | Morning triage of Slack, Gmail & Calendar |
| 90 | [summarize-video](./summarize-video/) | 📄 Documents | Summarize videos with transcript & quotes |
| 91 | [swarm](./swarm/) | 🔬 Methodology | Multi-perspective parallel exploration |
| 92 | [tarkin-segment-tokens](./tarkin-segment-tokens/) | 🔧 Infrastructure | Add/remove tokens from audience segments |
| 93 | [test-plan-creator](./test-plan-creator/) | 🧪 Testing | Create test plans & acceptance criteria |
| 94 | [testing-party-doc](./testing-party-doc/) | 🧪 Testing | Generate structured QA testing party docs |
| 95 | [viewing-figma-files](./viewing-figma-files/) | 🎨 Design | View, inspect & export Figma files |
| 96 | [web-research](./web-research/) | 🔎 Research & Insights | Search & synthesize external information |
| 97 | [writing-feedback](./writing-feedback/) | ✍️ Writing & Content | Write performance feedback (IBB model) |
| 98 | [writing-requirements-docs](./writing-requirements-docs/) | 📝 Product | Write PRDs from rough notes & evidence |
| 99 | [todo](./todo/) | ⏰ Productivity | Persistent to-do list with proactive reminders and auto-capture |

---

## By Category

### 🤖 Agent Behavior
- [ask-questions-if-underspecified](./ask-questions-if-underspecified/) — Clarify requirements before implementing
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
- [requesting-pr-reviews-from-owners](./requesting-pr-reviews-from-owners/) — Track and request PR review approvals

### 📊 Data & Analytics
- [airtable](./airtable/) — Manage Airtable bases, tables, and records
- [block-data](./block-data/) — Query business metrics, KPIs, and dashboards
- [data-analyst](./data-analyst/) — Drive insightful visualizations and charts
- [databricks](./databricks/) — Query Databricks Lakehouse via SQL
- [datadog](./datadog/) — Query logs, metrics, traces, monitors, and RUM
- [looker](./looker/) — Interact with Looker dashboards, queries, and explores
- [query-expert](./query-expert/) — Discover tables and execute Snowflake SQL
- [snowflake](./snowflake/) — Query Snowflake data warehouse via SQL

### 🔍 Search & Discovery
- [codesearch](./codesearch/) — Search Sourcegraph across all repositories
- [dev-guides](./dev-guides/) — Search and retrieve internal developer documentation
- [eng-ai-chat](./eng-ai-chat/) — Search internal engineering knowledge base
- [glean](./glean/) — Search enterprise knowledge, docs, and people
- [people-api](./people-api/) — Query employee directory and org data
- [regulator](./regulator/) — Search merchant accounts, cases, and payments
- [seller-snapshot](./seller-snapshot/) — Generate comprehensive merchant 360° snapshot

### 🧪 Experimentation
- [creating-experiments](./creating-experiments/) — Set up A/B experiments and flag patterns
- [flag-simulator](./flag-simulator/) — Evaluate LaunchDarkly feature flags via API
- [launchdarkly-cli](./launchdarkly-cli/) — Manage feature flags via ldcli

### 📱 Mobile Development
- [cash](./cash/) — Cash App iOS & Android developer CLI
- [mobile-releases](./mobile-releases/) — Browse, download, and install mobile app builds
- [pos-releases](./pos-releases/) — Query POS release train schedules and versions

### 📱 Mobile & Devices
- [android-emulator](./android-emulator/) — Manage Android emulators (AVDs)
- [ios-simulator](./ios-simulator/) — Manage iOS simulators for testing

### 🚀 Deployment
- [blockcell](./blockcell/) — Deploy static sites for internal sharing
- [deploying-prd-prototypes](./deploying-prd-prototypes/) — Deploy prototypes from PRDs to hosting
- [playpen](./playpen/) — Deploy and debug in ephemeral staging pods
- [prototype-builder](./prototype-builder/) — Scaffold interactive HTML prototypes

### 📝 Product
- [early-feature-access](./early-feature-access/) — Add features to Early Feature Access page
- [feature-overview-updater](./feature-overview-updater/) — Regenerate feature README index tables
- [logging-feature-requests](./logging-feature-requests/) — Log feature requests from Slack to sheet
- [product](./product/) — Search product docs and requirements
- [saving-cash-rounding-feedback](./saving-cash-rounding-feedback/) — Save customer feedback to tracking doc
- [spec-creator](./spec-creator/) — Create and iterate on product specs
- [writing-requirements-docs](./writing-requirements-docs/) — Write PRDs from rough notes with evidence

### 📋 Task & Project Management
- [creating-builderbot-tasks](./creating-builderbot-tasks/) — Create tasks via CLI with labels and status
- [linear](./linear/) — Issue tracking and project management
- [linear-to-execution](./linear-to-execution/) — Pick up a Linear issue for agent execution
- [plan-to-linear](./plan-to-linear/) — Convert structured plans into Linear issues
- [project-status](./project-status/) — Gather project state across multiple sources

### ✍️ Writing & Content
- [block-writing](./block-writing/) — Brand voice for product content
- [jack-guidance](./jack-guidance/) — Concise, direct communication coaching
- [reflect](./reflect/) — Guided reflection coach for performance reviews
- [writing-feedback](./writing-feedback/) — Write performance feedback using IBB model

### 📄 Documents
- [converting-gdocs-to-markdown](./converting-gdocs-to-markdown/) — Convert Google Docs to markdown
- [gdrive](./gdrive/) — Google Drive, Docs, Sheets, and Slides
- [notion](./notion/) — Read, search, create, and update Notion pages
- [summarize-video](./summarize-video/) — Summarize videos with transcript and quotes

### 🔧 Infrastructure
- [create-permission](./create-permission/) — Create/modify permissions end-to-end
- [registry-api](./registry-api/) — Query service registry via Python API
- [registry-info](./registry-info/) — Look up service metadata and ownership
- [tarkin-segment-tokens](./tarkin-segment-tokens/) — Add/remove tokens from audience segments

### 🔍 Audit & Compliance
- [device-settings-audit](./device-settings-audit/) — Query device profile change history
- [mode-settings-audit](./mode-settings-audit/) — Audit Mode Analytics workspace settings

### 🌐 Browser & Web
- [agent-browser](./agent-browser/) — Debug and interact with web apps via CLI

### 🎨 Design
- [viewing-figma-files](./viewing-figma-files/) — View, inspect, and export Figma files

### 🖥️ Frontend
- [market-react](./market-react/) — Market React design system components
- [navigation](./navigation/) — Add/update Dashboard navigation menu links

### 🧪 Testing
- [ditto](./ditto/) — Provision and manage staging test accounts
- [merchant-factory](./merchant-factory/) — Create staging test merchant accounts
- [test-plan-creator](./test-plan-creator/) — Create test plans and acceptance criteria
- [testing-party-doc](./testing-party-doc/) — Generate structured QA testing party docs

### 💬 Communication
- [cash-rounding-responder](./cash-rounding-responder/) — Triage and reply to team inbox emails
- [gmail](./gmail/) — Search, read, send, and manage emails
- [slack](./slack/) — Search, read, and post Slack messages

### 📆 Calendar & Scheduling
- [gcal](./gcal/) — Schedule, manage, and query calendar events
- [reviewing-calendar](./reviewing-calendar/) — Visual weekly calendar view with conflict detection

### ⚙️ CI/CD
- [kochiku](./kochiku/) — Fetch CI build data, logs, and artifacts

### 🖥️ System & macOS
- [controlling-computer](./controlling-computer/) — Control Mac via AppleScript and shell commands
- [free-disk-space](./free-disk-space/) — Survey and clean up macOS disk space
- [snagit](./snagit/) — Capture screenshots and recordings

### ⏰ Productivity
- [start-of-day](./start-of-day/) — Morning triage of Slack, Gmail, and Calendar
- [todo](./todo/) — Persistent to-do list with proactive reminders and auto-capture

### 🔗 Navigation
- [go-link](./go-link/) — Resolve internal go/ shortlinks to full URLs

### 🔧 Setup & Config
- [setting-up-builderbot](./setting-up-builderbot/) — Guide CLI tool setup and configuration

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
3. Register in `~/bin/install-amp-skills.sh`
4. Add an entry to this README

---

*Last updated: March 2026*
