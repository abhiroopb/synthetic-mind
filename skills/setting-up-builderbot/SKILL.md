---
Skill name: setting-up-builderbot
Skill description: Guides users through a CLI tool setup for an AI task orchestration system. Use when someone needs to install/configure the CLI or prepare for CLI-based workflows.
---

# Setting Up the Task Orchestration CLI

A task orchestration system for AI agents. It routes work to executors based on task labels, status, and attached artifacts. This skill focuses on getting the CLI installed and ready.

## When To Use

- User needs the CLI installed or configured
- User wants CLI automation or subscriber workflows
- User needs to run tasks from the terminal

## Key Links (Give Up Front)

- Getting started guide: Check your organization's developer docs
- Support: Check the relevant Slack channel

## Prerequisites (Ask First)

- Do you already have access?
  - Engineering teams usually have it by default
  - Otherwise request the appropriate role from your service registry

## CLI Setup Path (Minimal)

1. Clone the repository.
2. Build the CLIs.
   - `just build-all` or `just build-cli`
3. Add to your PATH (recommended):
   - `export PATH="$HOME/Development/builderbot/build:$PATH"`
4. (Optional) Add alias: `alias bb="builderbot"`
5. Reload shell: `source ~/.zshrc`
6. (Optional) Add agent instructions: `builderbot instructions >> ~/.config/agent/AGENTS.md`
7. For CLI usage and task operations, use the `creating-builderbot-tasks` skill.

## Common Pitfalls

- CLI not on PATH after build
- Missing access permissions
- Using the CLI before a repo artifact is attached for executors
