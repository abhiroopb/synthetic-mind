# 🛠️ Skills Library

A collection of 98 AI agent skills built for [Amp](https://ampcode.com) — covering productivity, development workflows, data analysis, communication, and more.

Each skill is a self-contained module with a `SKILL.md` that defines its behavior, triggers, and instructions for an AI agent.

---

## 📋 Quick Index

| # | Skill | Category | Description |
|---|-------|----------|-------------|
| 1 | [address-pr-comments](./address-pr-comments) | Git & PRs | Address and resolve GitHub PR review comments |
| 2 | [agent-browser](./agent-browser) | Browser & Web | Debug visual bugs and interact with web apps via CLI |
| 3 | [airtable](./airtable) | Data & Integrations | Manage Airtable bases, tables, records, and automations |
| 4 | [android-emulator](./android-emulator) | Mobile & Devices | Manage Android emulators (AVDs) for testing |
| 5 | [ask-questions-if-underspecified](./ask-questions-if-underspecified) | Agent Behavior | Clarify requirements before implementing |
| 6 | [auto-pilot](./auto-pilot) | Agent Behavior | Orchestrate all skills automatically — routes requests to the right skill |
| 7 | [block-data](./block-data) | Data & Analytics | Query business metrics, dashboards, and permissions |
| 8 | [block-writing](./block-writing) | Writing & Content | Write and review product content with brand voice standards |
| 9 | [blockcell](./blockcell) | Deployment | Deploy static website prototypes for internal sharing |
| 10 | [cash](./cash) | Mobile Development | Cash App iOS & Android developer tasks (build, test, lint) |
| 11 | [cash-rounding-responder](./cash-rounding-responder) | Email & Triage | Triage and draft replies to cash-rounding emails |
| 12 | [code-review-general](./code-review-general) | Git & PRs | Address PR code review feedback and resolve threads |
| 13 | [codesearch](./codesearch) | Search & Discovery | Search internal Sourcegraph codesearch across all repos |
| 14 | [controlling-computer](./controlling-computer) | System & macOS | Control Mac via AppleScript — apps, windows, settings |
| 15 | [converting-gdocs-to-markdown](./converting-gdocs-to-markdown) | Documents | Convert Google Docs to markdown files |
| 16 | [create-permission](./create-permission) | Infrastructure | Create or modify permissions across proto files and configs |
| 17 | [creating-builderbot-tasks](./creating-builderbot-tasks) | Task Management | Create Builderbot tasks via CLI |
| 18 | [creating-experiments](./creating-experiments) | Experimentation | Create and manage A/B experiments and feature flags |
| 19 | [data-analyst](./data-analyst) | Data & Analytics | Drive insightful visualizations and charts from data |
| 20 | [databricks](./databricks) | Data & Analytics | Query Databricks Lakehouse using SQL |
| 21 | [datadog](./datadog) | Observability | Query logs, metrics, traces, monitors, and RUM |
| 22 | [deploying-prd-prototypes](./deploying-prd-prototypes) | Deployment | Deploy interactive prototypes from PRDs |
| 23 | [dev-guides](./dev-guides) | Search & Discovery | Search and retrieve developer documentation |
| 24 | [device-settings-audit](./device-settings-audit) | Audit & Compliance | Query device profile change history |
| 25 | [ditto](./ditto) | Testing | Create and manage staging test accounts |
| 26 | [early-feature-access](./early-feature-access) | Product | Add features to Early Feature Access page |
| 27 | [eng-ai-chat](./eng-ai-chat) | Search & Discovery | Search internal company knowledge across multiple sources |
| 28 | [feature-overview-updater](./feature-overview-updater) | Documentation | Scan features directory and regenerate README index |
| 29 | [feedback-searcher](./feedback-searcher) | Research & Insights | Search and synthesize seller feedback across channels |
| 30 | [flag-simulator](./flag-simulator) | Experimentation | Evaluate LaunchDarkly feature flags via API |
| 31 | [free-disk-space](./free-disk-space) | System & macOS | Survey and clean up disk space on macOS |
| 32 | [gcal](./gcal) | Calendar & Scheduling | Create, update, and manage Google Calendar events |
| 33 | [gdrive](./gdrive) | Documents | Interact with Google Drive, Docs, Sheets, and Slides |
| 34 | [gh-pr-read](./gh-pr-read) | Git & PRs | Read and summarize GitHub pull requests |
| 35 | [git-worktree](./git-worktree) | Git & PRs | Manage git worktrees for parallel branch work |
| 36 | [glean](./glean) | Search & Discovery | Search Glean enterprise knowledge and people directory |
| 37 | [gmail](./gmail) | Email & Triage | Interact with Gmail |
| 38 | [go-link](./go-link) | Navigation | Translate internal go/ links to full URLs |
| 39 | [historical-info](./historical-info) | Memory & Context | Search across sources to find past work history |
| 40 | [ios-simulator](./ios-simulator) | Mobile & Devices | Manage iOS simulators for testing |
| 41 | [jack-guidance](./jack-guidance) | Writing & Content | Concise, direct coaching for internal communication |
| 42 | [kb-distill](./kb-distill) | Memory & Context | Distill observations into structured knowledge notes |
| 43 | [kb-promote](./kb-promote) | Memory & Context | Promote knowledge notes into permanent rules or skills |
| 44 | [kb-style-matrix](./kb-style-matrix) | Memory & Context | Analyze communication style to build a voice profile |
| 45 | [kochiku](./kochiku) | CI/CD | Fetch Kochiku build data, logs, and artifacts |
| 46 | [launchdarkly-cli](./launchdarkly-cli) | Experimentation | Manage LaunchDarkly feature flags and experiments |
| 47 | [linear](./linear) | Task Management | Interact with Linear for issue tracking and project management |
| 48 | [linear-to-execution](./linear-to-execution) | Task Management | Pick up a Linear issue and prepare for execution |
| 49 | [logging-feature-requests](./logging-feature-requests) | Product | Digest and log feature requests from Slack |
| 50 | [looker](./looker) | Data & Analytics | Interact with Looker dashboards, queries, and explores |
| 51 | [market-react](./market-react) | Frontend | Reference docs for Market React UI components |
| 52 | [memory](./memory) | Memory & Context | Persistent cross-session memory system |
| 53 | [merchant-factory](./merchant-factory) | Testing | Create staging merchants with catalogs and subscriptions |
| 54 | [mobile-releases](./mobile-releases) | Mobile Development | Browse, download, and install mobile app builds |
| 55 | [mode-settings-audit](./mode-settings-audit) | Audit & Compliance | Audit Mode Analytics workspace settings and permissions |
| 56 | [navigation](./navigation) | Frontend | Add or update Dashboard navigation menu links |
| 57 | [notion](./notion) | Documents | Access Notion workspace — read, search, create, update |
| 58 | [people-api](./people-api) | Search & Discovery | Query employee data — search by name, LDAP, Slack ID |
| 59 | [plan-to-linear](./plan-to-linear) | Task Management | Convert structured plans into Linear issues and projects |
| 60 | [playpen](./playpen) | Deployment | Deploy and debug applications using Playpen service |
| 61 | [pos-releases](./pos-releases) | Mobile Development | Query POS release train schedules and version info |
| 62 | [pr-manager](./pr-manager) | Git & PRs | Commit changes, create PRs, supports Graphite stacked PRs |
| 63 | [product](./product) | Product | Search product requirements and feature architecture |
| 64 | [project-status](./project-status) | Project Management | Gather project state from Slack, Drive, GitHub, LaunchDarkly |
| 65 | [prototype-builder](./prototype-builder) | Deployment | Scaffold and build interactive HTML prototypes |
| 66 | [push-pr](./push-pr) | Git & PRs | Push branch and create a draft PR with AI-generated description |
| 67 | [query-expert](./query-expert) | Data & Analytics | Discover tables and execute SQL on Snowflake |
| 68 | [ralph-loop](./ralph-loop) | Agent Behavior | Iterative work-review loop using two AI models |
| 69 | [rebasing-git-branches](./rebasing-git-branches) | Git & PRs | Rebase git branches onto upstream targets |
| 70 | [reflect](./reflect) | Writing & Content | Reflection coach for thoughtful performance insights |
| 71 | [registry-api](./registry-api) | Infrastructure | Query Registry API for apps, users, groups, and roles |
| 72 | [registry-info](./registry-info) | Infrastructure | Query application metadata from Registry |
| 73 | [regulator](./regulator) | Search & Discovery | Search Regulator for merchant accounts, cases, payments |
| 74 | [requesting-pr-reviews-from-owners](./requesting-pr-reviews-from-owners) | Git & PRs | Track PR review status and generate Slack reminders |
| 75 | [reviewing-calendar](./reviewing-calendar) | Calendar & Scheduling | Visual weekly calendar view with conflict detection |
| 76 | [rpi](./rpi) | Methodology | Research, Plan, Implement — structured task methodology |
| 77 | [rpi-implement](./rpi-implement) | Methodology | Execute approved RPI implementation plans phase by phase |
| 78 | [rpi-iterate](./rpi-iterate) | Methodology | Iterate on existing RPI plans with targeted updates |
| 79 | [rpi-plan](./rpi-plan) | Methodology | Create detailed implementation plans using RPI |
| 80 | [rpi-research](./rpi-research) | Methodology | Research codebase for complex tasks using RPI |
| 81 | [saving-cash-rounding-feedback](./saving-cash-rounding-feedback) | Product | Save seller feedback to tracking Google Doc |
| 82 | [seller-snapshot](./seller-snapshot) | Search & Discovery | Seller snapshot lookup |
| 83 | [setting-up-builderbot](./setting-up-builderbot) | Setup & Config | Guide through Builderbot CLI setup |
| 84 | [skill-management](./skill-management) | Agent Behavior | Manage Amp skills — list, add, remove, inspect, edit |
| 85 | [slack](./slack) | Communication | Search, read, and post Slack messages across workspaces |
| 86 | [snagit](./snagit) | System & macOS | Capture screenshots and recordings via Snagit |
| 87 | [snowflake](./snowflake) | Data & Analytics | Query Snowflake data warehouse with Okta SSO |
| 88 | [spec-creator](./spec-creator) | Product | Create and iterate on product requirement specs |
| 89 | [start-of-day](./start-of-day) | Productivity | Morning triage of Slack, Gmail, Calendar, and notifications |
| 90 | [summarize-video](./summarize-video) | Documents | Summarize videos — extract transcript and generate summary |
| 91 | [swarm](./swarm) | Agent Behavior | Multi-perspective exploration with adversarial challenge |
| 92 | [tarkin-segment-tokens](./tarkin-segment-tokens) | Infrastructure | Add or remove tokens from Tarkin segments |
| 93 | [test-plan-creator](./test-plan-creator) | Testing | Create test plans and acceptance criteria from specs |
| 94 | [testing-party-doc](./testing-party-doc) | Testing | Generate structured testing party docs for feature launches |
| 95 | [viewing-figma-files](./viewing-figma-files) | Design | View Figma files, inspect structure, export images |
| 96 | [web-research](./web-research) | Research & Insights | Search the web and synthesize external information |
| 97 | [writing-feedback](./writing-feedback) | Writing & Content | Write performance feedback using IBB model |
| 98 | [writing-requirements-docs](./writing-requirements-docs) | Product | Write thorough PRDs from rough notes with evidence |

---

## 📂 By Category

### 🤖 Agent Behavior
Skills that control how the AI agent operates.

- [ask-questions-if-underspecified](./ask-questions-if-underspecified) — Clarify before implementing
- [auto-pilot](./auto-pilot) — Auto-route requests to the right skill
- [ralph-loop](./ralph-loop) — Iterative two-model work-review loop
- [skill-management](./skill-management) — Manage skills (list, add, remove, edit)
- [swarm](./swarm) — Multi-perspective exploration with consensus

### 🧠 Memory & Context
Persistent memory and knowledge management.

- [historical-info](./historical-info) — Search past work history
- [kb-distill](./kb-distill) — Distill observations into knowledge notes
- [kb-promote](./kb-promote) — Promote notes into permanent rules
- [kb-style-matrix](./kb-style-matrix) — Build communication voice profile
- [memory](./memory) — Cross-session persistent memory system

### 🔬 Methodology
Structured approaches to complex tasks.

- [rpi](./rpi) — Research, Plan, Implement router
- [rpi-implement](./rpi-implement) — Execute plans phase by phase
- [rpi-iterate](./rpi-iterate) — Iterate on plans with targeted updates
- [rpi-plan](./rpi-plan) — Create detailed implementation plans
- [rpi-research](./rpi-research) — Research codebase comprehensively

### 🔀 Git & PRs
Git workflows and pull request management.

- [address-pr-comments](./address-pr-comments) — Resolve PR review comments
- [code-review-general](./code-review-general) — Address PR code review feedback
- [gh-pr-read](./gh-pr-read) — Read and summarize PRs
- [git-worktree](./git-worktree) — Work on multiple branches in parallel
- [pr-manager](./pr-manager) — Commit, create PRs, Graphite support
- [push-pr](./push-pr) — Push and create draft PRs
- [rebasing-git-branches](./rebasing-git-branches) — Rebase branches
- [requesting-pr-reviews-from-owners](./requesting-pr-reviews-from-owners) — Track review status

### 📊 Data & Analytics
Query and analyze data across platforms.

- [block-data](./block-data) — Business metrics and dashboards
- [data-analyst](./data-analyst) — Visualizations and charts
- [databricks](./databricks) — Databricks SQL queries
- [looker](./looker) — Looker dashboards and explores
- [query-expert](./query-expert) — Snowflake table discovery and SQL
- [snowflake](./snowflake) — Snowflake data warehouse queries

### 🔍 Search & Discovery
Find information across systems.

- [codesearch](./codesearch) — Sourcegraph codesearch
- [dev-guides](./dev-guides) — Developer documentation
- [eng-ai-chat](./eng-ai-chat) — Internal company knowledge
- [glean](./glean) — Enterprise knowledge search
- [people-api](./people-api) — Employee data lookup
- [regulator](./regulator) — Merchant accounts and cases
- [seller-snapshot](./seller-snapshot) — Seller snapshot lookup

### 🧪 Experimentation
A/B testing and feature flags.

- [creating-experiments](./creating-experiments) — Create and manage experiments
- [flag-simulator](./flag-simulator) — Evaluate LaunchDarkly flags
- [launchdarkly-cli](./launchdarkly-cli) — Manage flags via CLI

### 📱 Mobile Development
Mobile app development and releases.

- [cash](./cash) — Cash App iOS & Android tasks
- [mobile-releases](./mobile-releases) — Browse and install app builds
- [pos-releases](./pos-releases) — POS release train schedules

### 📱 Mobile & Devices
Simulator and emulator management.

- [android-emulator](./android-emulator) — Manage Android emulators
- [ios-simulator](./ios-simulator) — Manage iOS simulators

### 🚀 Deployment
Deploy apps and prototypes.

- [blockcell](./blockcell) — Deploy static sites for internal sharing
- [deploying-prd-prototypes](./deploying-prd-prototypes) — Deploy prototypes from PRDs
- [playpen](./playpen) — Deploy and debug via Playpen
- [prototype-builder](./prototype-builder) — Scaffold interactive prototypes

### 📝 Product
Product management workflows.

- [early-feature-access](./early-feature-access) — Add features to EFA page
- [logging-feature-requests](./logging-feature-requests) — Log feature requests from Slack
- [product](./product) — Search product requirements
- [saving-cash-rounding-feedback](./saving-cash-rounding-feedback) — Save seller feedback
- [spec-creator](./spec-creator) — Create product requirement specs
- [writing-requirements-docs](./writing-requirements-docs) — Write thorough PRDs

### 📅 Task & Project Management
Issue tracking and project status.

- [creating-builderbot-tasks](./creating-builderbot-tasks) — Create Builderbot tasks
- [linear](./linear) — Linear issue tracking
- [linear-to-execution](./linear-to-execution) — Execute Linear issues
- [plan-to-linear](./plan-to-linear) — Convert plans to Linear issues
- [project-status](./project-status) — Gather project state across tools

### ✍️ Writing & Content
Writing, editing, and communication coaching.

- [block-writing](./block-writing) — Product content with brand voice
- [jack-guidance](./jack-guidance) — Direct coaching for internal comms
- [reflect](./reflect) — Reflection coach for performance insights
- [writing-feedback](./writing-feedback) — Performance feedback (IBB model)

### 📄 Documents
Document creation and management.

- [converting-gdocs-to-markdown](./converting-gdocs-to-markdown) — Google Docs to markdown
- [gdrive](./gdrive) — Google Drive, Docs, Sheets, Slides
- [notion](./notion) — Notion workspace access
- [summarize-video](./summarize-video) — Video transcript and summary

### 🔧 Infrastructure
Internal platform and infrastructure tools.

- [create-permission](./create-permission) — Create/modify permissions
- [registry-api](./registry-api) — Registry API queries
- [registry-info](./registry-info) — Application metadata
- [tarkin-segment-tokens](./tarkin-segment-tokens) — Manage Tarkin segments

### 🔍 Audit & Compliance
Audit and compliance workflows.

- [device-settings-audit](./device-settings-audit) — Device profile change history
- [mode-settings-audit](./mode-settings-audit) — Mode Analytics workspace audit

### 🌐 Browser & Web
Web browsing and automation.

- [agent-browser](./agent-browser) — Browser automation via CLI

### 🎨 Design
Design tools and workflows.

- [viewing-figma-files](./viewing-figma-files) — View and inspect Figma files

### 🖥️ Frontend
Frontend development.

- [market-react](./market-react) — Market React UI components
- [navigation](./navigation) — Dashboard navigation menu

### 🧪 Testing
Test creation and QA.

- [ditto](./ditto) — Staging test accounts
- [merchant-factory](./merchant-factory) — Staging merchants
- [test-plan-creator](./test-plan-creator) — Test plans from specs
- [testing-party-doc](./testing-party-doc) — Testing party documents

### 💬 Communication
Messaging and email.

- [cash-rounding-responder](./cash-rounding-responder) — Triage cash-rounding emails
- [gmail](./gmail) — Gmail interaction
- [slack](./slack) — Slack messaging across workspaces

### 📆 Calendar & Scheduling
Calendar management.

- [gcal](./gcal) — Google Calendar events
- [reviewing-calendar](./reviewing-calendar) — Visual weekly calendar view

### ⚙️ CI/CD
Build and deployment pipelines.

- [kochiku](./kochiku) — Kochiku build data and logs

### 🖥️ System & macOS
System automation and utilities.

- [controlling-computer](./controlling-computer) — macOS control via AppleScript
- [free-disk-space](./free-disk-space) — Disk space cleanup
- [snagit](./snagit) — Screenshots and recordings

### ⏰ Productivity
Daily workflows and productivity.

- [start-of-day](./start-of-day) — Morning triage across all channels

### 🔗 Navigation
Internal link resolution.

- [go-link](./go-link) — Resolve go/ shortlinks

### 🔧 Setup & Config
Initial setup and configuration.

- [setting-up-builderbot](./setting-up-builderbot) — Builderbot CLI setup

### 🔎 Research & Insights
Research and synthesis.

- [feedback-searcher](./feedback-searcher) — Synthesize seller feedback
- [web-research](./web-research) — Web research and synthesis

---

## How to Use

Each skill folder contains:
- **`SKILL.md`** — The main skill definition (YAML frontmatter + instructions)
- **`references/`** — Supporting docs, templates, or examples (when applicable)
- **`scripts/`** — Helper scripts (when applicable)
- **`SETUP.md`** — Setup instructions (when applicable)

To use a skill with Amp, add it via:
```bash
amp skills add <path-to-skill-folder>
```

## License

MIT
