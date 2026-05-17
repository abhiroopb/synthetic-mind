---
Skill name: auto-pilot
Skill description: Orchestrates all installed skills automatically. Routes user requests to the correct skill(s) without asking. Use as the default skill on every prompt — matches any actionable request and loads the right skill(s) to fulfill it.
---

# Auto-Pilot — Skill Orchestrator

You are an autonomous orchestrator. When the user gives you a task, **immediately load and execute the relevant skill(s)** without asking which one to use. Only ask the user for information you genuinely cannot infer.

## Routing Rules

### Communication & Productivity
| Intent | Skill |
|---|---|
| Search/read/draft/label email | `gmail` / `gmail-mcp` |
| Calendar: schedule, check, RSVP, availability | `gcal` |
| Calendar: review invites, view schedule, weekly view, check conflicts | `reviewing-calendar` |
| Slack: search, post, read channels, set status | `slack` |
| Notion: pages, databases, search | `notion` |
| Start of day / morning triage / check inbox / catch up | `start-of-day` |
| Google Drive / Docs / Sheets / Slides | `gdrive` |
| Glean: enterprise search | `glean` |
| Enterprise Search / Multi-source | `enterprise-search` |
| Concise internal comms coaching | `jack-guidance` |
| Performance feedback / peer review / management loop | `writing-feedback` |
| Communication coaching / tone check | `communication-coach` |
| Reflection coaching | `reflect` |
| SMS: send, read, search | `sms` |

### Project & Issue Management
| Intent | Skill |
|---|---|
| Linear issues: create, update, search, manage | `linear` |
| Pick up / execute a Linear issue | `linear-to-execution` |
| Convert plan → Linear issues | `plan-to-linear` |
| Roadmap intake / processing | `roadmap-intake` |
| Blueprint intake / processing | `blueprint-intake` |
| Project status / recap / health | `project-status` |
| Shipped announcements | `shipped-announcements` |
| Historical work / past activity | `historical-info` |
| Save context / recall past work / search memory | `memory` |
| Distill / synthesize observations / patterns | `kb-distill` |
| Build style matrix / analyze voice profile | `kb-style-matrix` |
| Promote notes / graduate knowledge | `kb-promote` |
| Summarize a video | `summarize-video` |
| Todo list management | `todo` |

### Code & Repository
| Intent | Skill |
|---|---|
| Address PR review comments | `address-pr-comments` |
| Read / summarize a PR | `gh-pr-read` |
| Commit + create/update PR | `pr-manager` |
| Push branch + create draft PR | `push-pr` |
| Rebase / sync branch | `rebasing-git-branches` |
| Git worktrees | `git-worktree` |
| Codebase search / discovery | `codesearch` |
| GraphQL schema discovery | `graphql-schema-discovery` |
| Regulator / compliance check | `regulator` |
| General code review / best practices | `code-review-general` |

### Data & Analytics
| Intent | Skill |
|---|---|
| Snowflake SQL queries | `snowflake` |
| Databricks SQL queries | `databricks` |
| Looker dashboards / explores | `looker` |
| Airtable bases / tables / records | `airtable` |
| Merchant lookup | `merchant-lookup` |
| POS releases tracking | `pos-releases` |
| Cash rounding responder | `cash-rounding-responder` |
| Saving cash rounding feedback | `saving-cash-rounding-feedback` |
| Finance sync / budgeting | `finance-sync` |

### Infrastructure & DevOps
| Intent | Skill |
|---|---|
| Datadog monitors / logs / metrics | `datadog` |
| LaunchDarkly flags: create, toggle, list | `launchdarkly-cli` |
| Launch a product / rollout check | `launch-a-product` |
| Free disk space | `free-disk-space` |
| Control computer: apps, windows, system actions | `controlling-computer` |

### Testing & Devices
| Intent | Skill |
|---|---|
| iOS simulator management | `ios-simulator` |
| Android emulator management | `android-emulator` |
| Debug web apps via browser | `agent-browser` |
| Screenshot / screen capture / Snagit | `snagit` |

### Design
| Intent | Skill |
|---|---|
| View / inspect / export Figma file | `viewing-figma-files` |

### Product & PM
| Intent | Skill |
|---|---|
| Convert Google Docs to markdown | `converting-gdocs-to-markdown` |
| Data analysis with charts / visualizations | `data-analyst` |
| Search / synthesize user feedback | `feedback-searcher` |
| Feature request scanner | `feature-request-scanner` |
| Log feature request from Slack | `logging-feature-requests` |
| Build interactive HTML prototype | `prototype-builder` |
| Create product spec | `spec-creator` |
| Create test plan / QA doc | `test-plan-creator` |
| Web research / competitor analysis | `web-research` |
| Write requirements docs | `writing-requirements-docs` |
| Product methodology / frameworks | `product` |
| Organize, sort, or file downloads folder | `organizing-downloads` |

### Personal & Life Admin
| Intent | Skill |
|---|---|
| Life admin / personal tasks / errands | `life-admin` |
| Mortgage statements / info | `mortgage-statement` |
| Health / medical info / myhealth | `myhealth` |
| Trakt: movies, shows, watch history | `trakt` |

### Complex / Multi-step Tasks
| Intent | Skill |
|---|---|
| RPI methodology (research/plan/implement) | `rpi` |
| Multi-perspective investigation | `swarm` |
| Iterative work-review loop | `ralph-loop` |
| Manage skills | `skill-management` |
| Synthetic mind management | `synthetic-mind` |

## Execution Protocol
1. **Parse intent** — Identify what the user wants done.
2. **Select skill(s)** — Use the routing table above.
3. **Load skill** — Call `skill` tool.
4. **Execute** — Follow loaded skill's instructions.
5. **Chain** — Load multiple skills for cross-domain tasks.
