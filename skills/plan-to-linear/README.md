# Plan to Linear

> Convert structured plans into well-formed Linear issues that an agent can execute.

## What it does

Plan to Linear takes a plan — from a task list, a planning document, or a conversation thread — and converts it into structured Linear issues optimized for agent execution. Each issue includes full context, objectives, acceptance criteria, relevant code paths, and dependency links. It can optionally create a Linear project to group related issues and cross-reference them with source materials. This is the planning half of the planning-to-execution loop with `linear-to-execution`.

## Usage

Use this skill when you have a plan ready to be broken down into trackable Linear issues. Requires the `linear` skill and a Linear API key.

**Status:** Experimental

**Trigger phrases:**
- "File this plan as Linear issues"
- "Create Linear tickets from this task list"
- "Break this down into Linear issues"
- "Convert this plan to Linear"
- "Bulk-create issues from this document"

## Examples

- `"Create Linear issues from my current task list"` — Reads the active task list, structures each item with context and acceptance criteria, and creates issues in the specified team.
- `"Break this plan down into Linear issues for the checkout team"` — Parses the plan, resolves the team, creates a project, and files individual issues with dependency links.

## Why it was created

Writing good Linear issues that another person (or agent) can pick up and execute takes time. This skill automates the conversion of high-level plans into self-contained, execution-ready issues — bridging the gap between planning and doing.
