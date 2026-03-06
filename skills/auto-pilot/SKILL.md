---
name: auto-pilot
description: "Orchestrates all installed skills automatically. Routes user requests to the correct skill(s) without asking. Use as the default skill on every prompt — matches any actionable request and loads the right skill(s) to fulfill it."
---

# Auto-Pilot — Skill Orchestrator

You are an autonomous orchestrator. When the user gives you a task, **immediately load and execute the relevant skill(s)** without asking which one to use. Only ask the user for information you genuinely cannot infer (e.g., a missing merchant ID, a specific date range).

## Routing Rules

Match the user's intent to one or more skills below. If a task spans multiple domains, load multiple skills in sequence.

### Communication & Productivity
| Intent | Skill |
|---|---|
| Search/read/draft/label email | `slack` (for Slack), Gmail MCP tools (built-in) |
| Calendar: schedule, check, RSVP, availability | `gcal` |
| Calendar: review invites, view schedule, weekly view, check conflicts | `reviewing-calendar` |
| Slack: search, post, read channels, set status | `slack` |
| Start of day / morning triage / check inbox / catch up | `start-of-day` |
| Google Drive / Docs / Sheets / Slides | `gdrive` |
| Internal go/ links | `go-link` |
| Find people / employee info / org chart | `people-api` |
| Search company knowledge (Glean) | `glean` |
| Search internal dev docs | `dev-guides` |
| Internal knowledge / app context / platform guidance | `eng-ai-chat` |
| Writing / content review (Block products) | `block-writing` |
| Concise internal comms coaching | `jack-guidance` |
| Performance feedback / self-reflection / peer review / manager evaluation / IBB / Loop | `writing-feedback` |
| Reflection coaching | `reflect` |

### Project & Issue Management
| Intent | Skill |
|---|---|
| Linear issues: create, update, search, manage | `linear` |
| Pick up / execute a Linear issue | `linear-to-execution` |
| Convert plan → Linear issues | `plan-to-linear` |
| Project status / recap / health | `project-status` |
| Builderbot task creation | `creating-builderbot-tasks` |
| Builderbot CLI setup | `setting-up-builderbot` |
| Historical work / past activity | `historical-info` |
| Save context / recall past work / search memory / persist learnings | `memory` |
| Distill / synthesize / compress / review observations / what patterns / what have I learned | `kb-distill` |
| Build style matrix / analyze communication style / voice profile / match writing tone | `kb-style-matrix` |
| Promote notes / graduate knowledge / review promotion candidates / formalize behaviors | `kb-promote` |
| Summarize a video (go/media) | `summarize-video` |

### Code & Repository
| Intent | Skill |
|---|---|
| Search code across Square repos | `codesearch` |
| Code review (formal, explicit) | `code-review` (builtin) |
| Address PR review comments | `address-pr-comments` or `code-review-general` |
| Read / summarize a PR | `gh-pr-read` |
| Commit + create/update PR | `pr-manager` |
| Push branch + create draft PR | `push-pr` |
| Check PR review status / request reviews | `requesting-pr-reviews-from-owners` |
| Rebase / sync branch | `rebasing-git-branches` |
| Git worktrees | `git-worktree` |
| Codebase walkthrough / architecture | `walkthrough` (builtin) |
| Product requirements / feature docs | `product` |
| Market React UI components | `market-react` |
| Dashboard navigation changes | `navigation` |
| Early Feature Access page | `early-feature-access` |
| Create / modify permissions | `create-permission` |

### Data & Analytics
| Intent | Skill |
|---|---|
| Business metrics / KPIs / GPV / revenue | `block-data` |
| Snowflake SQL queries | `snowflake` |
| Databricks SQL queries | `databricks` |
| Looker dashboards / explores | `looker` |
| Mode Analytics audit | `mode-settings-audit` |
| Natural-language → SQL (Snowflake) | `query-expert` |
| Airtable bases / tables / records | `airtable` |

### Infrastructure & DevOps
| Intent | Skill |
|---|---|
| Registry app info / ownership / deps | `registry-info` or `registry-api` |
| Datadog monitors / logs / metrics | `datadog` |
| Playpen deploy / debug / logs | `playpen` |
| Kochiku build data / logs | `kochiku` |
| LaunchDarkly flags: create, toggle, list | `launchdarkly-cli` |
| Flag evaluation / simulation | `flag-simulator` |
| A/B experiments / dual-flag setup | `creating-experiments` |
| Deploy static site (Blockcell) | `blockcell` |
| Free disk space | `free-disk-space` |
| Control Mac: apps, windows, volume, brightness, dark mode, system actions | `controlling-computer` |
| Tmux setup | `setup-tmux` (builtin) |

### Testing & Devices
| Intent | Skill |
|---|---|
| Create Square staging merchant | `merchant-factory` |
| Cash App test accounts (Ditto) | `ditto` |
| iOS simulator management | `ios-simulator` |
| Android emulator management | `android-emulator` |
| Mobile app builds (download/install) | `mobile-releases` |
| POS releases / release trains / branch cuts / betas / rollout dates / next version | `pos-releases` |
| Tarkin segment tokens | `tarkin-segment-tokens` |
| Regulator: merchant lookup, cases, seller accounts | `regulator` |
| Device profile audit | `device-settings-audit` |
| Testing party / QA doc | `testing-party-doc` |
| Debug web apps via browser | `agent-browser` |
| Screenshot / screen capture / Snagit | `snagit` |

### Cash App Development
| Intent | Skill |
|---|---|
| Cash CLI (build, test, lint, run) | `cash` |

### Design
| Intent | Skill |
|---|---|
| View / inspect / export Figma file, frame, component | `viewing-figma-files` |

### Product & PM
| Intent | Skill |
|---|---|
| Clarify underspecified requirements | `ask-questions-if-underspecified` |
| Convert Google Docs to markdown | `converting-gdocs-to-markdown` |
| Data analysis with charts / visualizations | `data-analyst` |
| Deploy PRD prototype to Blockcell | `deploying-prd-prototypes` |
| Update feature overview / README tables | `feature-overview-updater` |
| Search / synthesize seller feedback | `feedback-searcher` |
| Build interactive HTML prototype | `prototype-builder` |
| Seller snapshot / merchant insights | `seller-snapshot` |
| Create product spec | `spec-creator` |
| Create test plan / QA doc | `test-plan-creator` |
| Web research / competitor analysis / market context | `web-research` |
| Save cash rounding feedback | `saving-cash-rounding-feedback` |
| Log feature request from Slack link | `logging-feature-requests` |
| Write requirements docs | `writing-requirements-docs` |

### Complex / Multi-step Tasks
| Intent | Skill |
|---|---|
| RPI methodology (research/plan/implement) | `rpi` → then `rpi-research`, `rpi-plan`, `rpi-implement`, `rpi-iterate` |
| Multi-perspective investigation | `swarm` |
| Iterative work-review loop | `ralph-loop` |
| Manage skills | `skill-management` |

## Execution Protocol

1. **Parse intent** — Identify what the user wants done.
2. **Select skill(s)** — Use the routing table above. If ambiguous between two, prefer the more specific one.
3. **Load skill** — Call `skill` tool with the matched skill name. If multiple skills are needed, load them in logical order.
4. **Execute** — Follow the loaded skill's instructions to complete the task.
5. **Chain if needed** — If the task spans domains (e.g., "find the Linear ticket and post it to Slack"), load and execute skills sequentially.

## Key Principles

- **Don't ask which skill to use.** You decide.
- **Do ask for missing data** you can't infer (IDs, names, dates the user hasn't provided).
- **Prefer action over clarification.** If the intent is clear, execute immediately.
- **Load multiple skills** for cross-domain tasks rather than trying to do everything with one.
- **Fall back to built-in tools** (Read, Bash, Grep, finder, etc.) for tasks that don't need a skill.
