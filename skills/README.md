# 🛠️ Skills Library

A collection of 44 reusable AI agent skills built for [Amp](https://ampcode.com) — covering productivity, development workflows, communication, and more.

Each skill is a self-contained module with a `SKILL.md` that defines its behavior, triggers, and instructions for an AI agent. All skills here are **generic and portable** — they work with any codebase or team.

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
| 7 | [code-review-general](./code-review-general) | Git & PRs | Address PR code review feedback and resolve threads |
| 8 | [controlling-computer](./controlling-computer) | System & macOS | Control Mac via AppleScript — apps, windows, settings |
| 9 | [converting-gdocs-to-markdown](./converting-gdocs-to-markdown) | Documents | Convert Google Docs to markdown files |
| 10 | [deploying-prd-prototypes](./deploying-prd-prototypes) | Deployment | Deploy interactive prototypes from PRDs |
| 11 | [free-disk-space](./free-disk-space) | System & macOS | Survey and clean up disk space on macOS |
| 12 | [gcal](./gcal) | Calendar & Scheduling | Create, update, and manage Google Calendar events |
| 13 | [gdrive](./gdrive) | Documents | Interact with Google Drive, Docs, Sheets, and Slides |
| 14 | [gh-pr-read](./gh-pr-read) | Git & PRs | Read and summarize GitHub pull requests |
| 15 | [git-worktree](./git-worktree) | Git & PRs | Manage git worktrees for parallel branch work |
| 16 | [gmail](./gmail) | Communication | Interact with Gmail |
| 17 | [ios-simulator](./ios-simulator) | Mobile & Devices | Manage iOS simulators for testing |
| 18 | [jack-guidance](./jack-guidance) | Writing & Content | Concise, direct coaching for internal communication |
| 19 | [kb-distill](./kb-distill) | Memory & Context | Distill observations into structured knowledge notes |
| 20 | [kb-promote](./kb-promote) | Memory & Context | Promote knowledge notes into permanent rules or skills |
| 21 | [kb-style-matrix](./kb-style-matrix) | Memory & Context | Analyze communication style to build a voice profile |
| 22 | [launchdarkly-cli](./launchdarkly-cli) | Feature Flags | Manage LaunchDarkly feature flags and experiments |
| 23 | [linear](./linear) | Task Management | Interact with Linear for issue tracking and project management |
| 24 | [memory](./memory) | Memory & Context | Persistent cross-session memory system |
| 25 | [notion](./notion) | Documents | Access Notion workspace — read, search, create, update |
| 26 | [pr-manager](./pr-manager) | Git & PRs | Commit changes, create PRs, supports Graphite stacked PRs |
| 27 | [prototype-builder](./prototype-builder) | Deployment | Scaffold and build interactive HTML prototypes |
| 28 | [push-pr](./push-pr) | Git & PRs | Push branch and create a draft PR with AI-generated description |
| 29 | [ralph-loop](./ralph-loop) | Agent Behavior | Iterative work-review loop using two AI models |
| 30 | [rebasing-git-branches](./rebasing-git-branches) | Git & PRs | Rebase git branches onto upstream targets |
| 31 | [reviewing-calendar](./reviewing-calendar) | Calendar & Scheduling | Visual weekly calendar view with conflict detection |
| 32 | [rpi](./rpi) | Methodology | Research, Plan, Implement — structured task methodology |
| 33 | [rpi-implement](./rpi-implement) | Methodology | Execute approved RPI implementation plans phase by phase |
| 34 | [rpi-iterate](./rpi-iterate) | Methodology | Iterate on existing RPI plans with targeted updates |
| 35 | [rpi-plan](./rpi-plan) | Methodology | Create detailed implementation plans using RPI |
| 36 | [rpi-research](./rpi-research) | Methodology | Research codebase for complex tasks using RPI |
| 37 | [skill-management](./skill-management) | Agent Behavior | Manage Amp skills — list, add, remove, inspect, edit |
| 38 | [slack](./slack) | Communication | Search, read, and post Slack messages across workspaces |
| 39 | [snagit](./snagit) | System & macOS | Capture screenshots and recordings via Snagit |
| 40 | [summarize-video](./summarize-video) | Documents | Summarize videos — extract transcript and generate summary |
| 41 | [swarm](./swarm) | Agent Behavior | Multi-perspective exploration with adversarial challenge |
| 42 | [test-plan-creator](./test-plan-creator) | Testing | Create test plans and acceptance criteria from specs |
| 43 | [viewing-figma-files](./viewing-figma-files) | Design | View Figma files, inspect structure, export images |
| 44 | [web-research](./web-research) | Research | Search the web and synthesize external information |

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

### 📄 Documents & Productivity
Document creation, management, and daily workflows.

- [converting-gdocs-to-markdown](./converting-gdocs-to-markdown) — Google Docs to markdown
- [gcal](./gcal) — Google Calendar events
- [gdrive](./gdrive) — Google Drive, Docs, Sheets, Slides
- [gmail](./gmail) — Gmail interaction
- [notion](./notion) — Notion workspace access
- [reviewing-calendar](./reviewing-calendar) — Visual weekly calendar view
- [summarize-video](./summarize-video) — Video transcript and summary

### 💬 Communication & Writing
Messaging and writing coaching.

- [jack-guidance](./jack-guidance) — Direct coaching for internal comms
- [slack](./slack) — Slack messaging across workspaces

### 🌐 Browser & Web
Web browsing, automation, and research.

- [agent-browser](./agent-browser) — Browser automation via CLI
- [web-research](./web-research) — Web research and synthesis

### 📱 Mobile & Devices
Simulator and emulator management.

- [android-emulator](./android-emulator) — Manage Android emulators
- [ios-simulator](./ios-simulator) — Manage iOS simulators

### 🚀 Deployment
Deploy apps and prototypes.

- [deploying-prd-prototypes](./deploying-prd-prototypes) — Deploy prototypes from PRDs
- [prototype-builder](./prototype-builder) — Scaffold interactive prototypes

### 🏷️ Feature Flags
Feature flag management.

- [launchdarkly-cli](./launchdarkly-cli) — Manage LaunchDarkly flags via CLI

### 📋 Task Management
Issue tracking.

- [linear](./linear) — Linear issue tracking

### 🔗 Data & Integrations
External platform integrations.

- [airtable](./airtable) — Airtable API integration

### 🧪 Testing
Test creation and QA.

- [test-plan-creator](./test-plan-creator) — Test plans from specs

### 🎨 Design
Design tools and workflows.

- [viewing-figma-files](./viewing-figma-files) — View and inspect Figma files

### 🖥️ System & macOS
System automation and utilities.

- [controlling-computer](./controlling-computer) — macOS control via AppleScript
- [free-disk-space](./free-disk-space) — Disk space cleanup
- [snagit](./snagit) — Screenshots and recordings

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

---

> 📁 Looking for platform-specific skills? See [`/skills-internal`](../skills-internal/) for 54 additional skills built for specific enterprise environments.
