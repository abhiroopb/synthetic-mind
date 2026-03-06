---
name: setting-up-builderbot
description: "Guides users through Builderbot CLI setup. Use when someone needs to install/configure the CLI or prepare for CLI-based workflows."
---

# Setting Up Builderbot (CLI)

Builderbot is a task orchestration system for AI agents. It routes work to executors (like G2, Headless Goose, or Blox) based on task labels, status, and attached artifacts. This skill focuses on getting the CLI installed and ready.

## When To Use

- User needs the Builderbot CLI installed or configured
- User wants CLI automation or subscriber workflows
- User needs to run tasks from the terminal

## Key Links (Give Up Front)

- Getting started guide: https://dev-guides.sqprod.co/docs/tools/builderbot/getting-started
- Builderbot repo: https://github.com/squareup/BuilderBot
- Support Slack: #builderbot-team
- Use the `dev-guides` skill to look up these docs when needed.

## Prerequisites (Ask First)

- Do you already have Builderbot access?
  - Cash/Square Eng usually have it by default
  - Otherwise request the `builderbot--users` role: https://registry.sqprod.co/groups/builderbot--users

## CLI Setup Path (Minimal)

1. Clone the Builderbot repo.
2. Build the CLIs.
   - `just build-all` or `just build-cli`
3. Add Builderbot to your PATH (recommended):
   - `export PATH="$HOME/Development/builderbot/build:$PATH"
4. (Optional) Add alias: `alias bb="builderbot"`
5. Reload shell: `source ~/.zshrc`
6. (Optional) Add agent instructions: `builderbot instructions >> ~/.config/goose/AGENTS.md`
7. For CLI usage and task operations, use the `creating-builderbot-tasks` skill.

## Common Pitfalls

- CLI not on PATH after build
- Missing `builderbot--users` access
- Using the CLI before a repo artifact is attached for executors
