---
name: linear
description: Interact with Linear for issue tracking, project management, and team workflows. Search, create, update, and manage issues, projects, cycles, and initiatives.
metadata:
  author: square
  version: "1.0"
  status: experimental
---

# Linear Skill

Interact with Linear using MCP tools powered by the `@tacticlaunch/mcp-linear` package.

## Prerequisites

### API Key

You need a Linear Personal API Key:

1. Go to **Linear → Settings → Account → Security & Access**
2. Under **Personal API keys**, click **New API key**
3. Give it a label (e.g., "Amp Agent") and select **Full Access**
4. Copy the key and set it as the `LINEAR_API_TOKEN` environment variable

If tools fail with authentication errors, verify the key is set:

```bash
echo $LINEAR_API_TOKEN
```

---

## Quick Reference

All interactions use MCP tools directly. No CLI wrapper needed.

### Common Workflows

**Find your issues:**
Use `linear_searchIssues` with your user as assignee, or `linear_getIssues` for recent issues.

**Create an issue:**
1. Use `linear_getTeams` to find the team ID
2. Use `linear_getLabels` to find label IDs (optional)
3. Use `linear_createIssue` with title, description, teamId, and optional properties

**Update an issue:**
Use `linear_updateIssue` with the issue ID and fields to change (title, description, status, priority, assignee).

**Change issue status:**
1. Use `linear_getWorkflowStates` to find available statuses and their IDs
2. Use `linear_updateIssue` with the status ID

**Add a comment:**
Use `linear_createComment` with the issue ID and comment body (markdown supported).

**Work with projects:**
- `linear_getProjects` — list projects
- `linear_getProjectIssues` — get issues in a project
- `linear_addIssueToProject` — add an issue to a project

**Work with cycles:**
- `linear_getActiveCycle` — get current sprint/cycle
- `linear_addIssueToCycle` — add issue to a cycle

---

## Available Tools

### Core
| Tool | Description |
|------|-------------|
| `linear_getViewer` | Get info about the authenticated user |
| `linear_getOrganization` | Get org info |
| `linear_getUsers` | List users in the organization |
| `linear_getTeams` | List teams |
| `linear_getLabels` | List issue labels |
| `linear_getWorkflowStates` | List workflow states (statuses) |

### Issues
| Tool | Description |
|------|-------------|
| `linear_getIssues` | List recent issues |
| `linear_getIssueById` | Get issue by ID (e.g., `ABC-123`) |
| `linear_searchIssues` | Search/filter issues |
| `linear_createIssue` | Create a new issue |
| `linear_updateIssue` | Update an issue |
| `linear_assignIssue` | Assign issue to a user |
| `linear_setIssuePriority` | Set issue priority (0=none, 1=urgent, 2=high, 3=medium, 4=low) |
| `linear_archiveIssue` | Archive an issue |
| `linear_transferIssue` | Move issue to another team |
| `linear_duplicateIssue` | Duplicate an issue |
| `linear_convertIssueToSubtask` | Convert to subtask |
| `linear_getIssueHistory` | View issue change history |
| `linear_addIssueLabel` | Add label to issue |
| `linear_removeIssueLabel` | Remove label from issue |

### Comments
| Tool | Description |
|------|-------------|
| `linear_createComment` | Add comment (markdown) |
| `linear_getComments` | Get comments on an issue |

### Projects
| Tool | Description |
|------|-------------|
| `linear_getProjects` | List projects |
| `linear_createProject` | Create a project |
| `linear_updateProject` | Update a project |
| `linear_getProjectIssues` | Get issues in a project |
| `linear_addIssueToProject` | Add issue to project |

### Cycles
| Tool | Description |
|------|-------------|
| `linear_getCycles` | List cycles |
| `linear_getActiveCycle` | Get active cycle for a team |
| `linear_addIssueToCycle` | Add issue to cycle |

### Initiatives
| Tool | Description |
|------|-------------|
| `linear_getInitiatives` | List initiatives |
| `linear_getInitiativeById` | Get initiative details |
| `linear_createInitiative` | Create initiative |
| `linear_updateInitiative` | Update initiative |
| `linear_archiveInitiative` | Archive initiative |
| `linear_getInitiativeProjects` | Get projects in initiative |
| `linear_addProjectToInitiative` | Add project to initiative |
| `linear_removeProjectFromInitiative` | Remove project from initiative |

---

## Troubleshooting

| Error | Solution |
|-------|----------|
| Auth/token errors | Ensure `LINEAR_API_TOKEN` env var is set with a valid API key |
| "team not found" | Use `linear_getTeams` to find valid team IDs |
| "state not found" | Use `linear_getWorkflowStates` to find valid status IDs |
| Permission errors | Ensure API key has Full Access and access to all teams |
