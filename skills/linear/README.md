# Linear

> Interact with Linear for issue tracking, project management, and team workflows.

## What it does

The Linear skill provides full access to Linear's issue tracking system via MCP tools. You can search, create, update, and manage issues, projects, cycles, and initiatives. It covers the complete Linear API surface including issue assignment, status changes, labels, comments, workflow states, and team management — all without leaving the command line.

## Usage

Use this skill for any Linear interaction. Requires a Linear Personal API Key set as `LINEAR_API_TOKEN`.

**Trigger phrases:**
- "Find my open issues"
- "Create a new issue for the checkout team"
- "Update ENG-123 to In Progress"
- "Add a comment to this issue"
- "What's in the current sprint?"
- "List all projects"

## Examples

- `"Create an issue titled 'Fix receipt rendering bug' for the checkout team"` — Resolves the team ID, creates the issue with the given title, and returns the issue identifier.
- `"What issues are assigned to me?"` — Searches for issues with you as the assignee and presents them in a list.
- `"Move ENG-456 to Done"` — Looks up the workflow state ID for "Done" and updates the issue status.

## Why it was created

Context-switching to a web UI for issue tracking breaks flow. This skill brings full Linear functionality into the agent workflow, enabling seamless issue management alongside code and documentation work.
