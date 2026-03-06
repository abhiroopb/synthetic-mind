# Creating Builderbot Tasks

> Create and manage tasks via a CLI with labels, status tracking, and artifact attachments.

## What it does

Creates tasks programmatically using a task management CLI. Supports attaching artifacts (repos, PRs, messages, URLs), updating task status, creating subtasks, and configuring executor labels for different automation backends (headless agents, workflow engines, workstations). Previews each task before creation and provides a consistent description format for scanability.

## Usage

Use when you need to create tasks from the command line, attach artifacts, or manage task status without using the web UI.

Trigger phrases:
- "Create a task"
- "Create a Builderbot task"
- "File a task for this issue"

## Examples

- "Create a headless task to clean up unused feature flags in the dashboard repo"
- "Create a task for ISSUE-123 and attach the repo artifact"
- "List my current tasks and update TSK-456 to complete"

## Why it was created

Creating tasks through the web UI is slow for batch operations. This skill enables quick task creation, labeling, and artifact attachment from the terminal, especially useful for filing automated work items.
