# Create Permission

> Create or modify permissions end-to-end across proto files, config, and authorization mappings.

## What it does

Guides engineers through the full lifecycle of creating or modifying permissions. This spans multiple repositories and can involve developer permissions (proto enums for API authorization), employee permissions (team-level access control), display permissions (UI configuration), and authorization mappings between them. The skill parses an approved intake form, derives a change plan, asks targeted questions about missing fields, and executes the changes across repos — opening PRs in each.

## Usage

Use when you need to create a new permission, modify a permission mapping, or update authorization config. The skill is driven by an approved intake form and operates in two phases: Proto Phase (enum changes) and Config Phase (YAML/config changes).

Trigger phrases:
- "Create a permission"
- "Add a new permission"
- "Modify the permission mapping"
- "Set up a new permission from this intake form"

## Examples

- "Create a permission from this intake form URL"
- "Config Phase for MANAGE_INVENTORY"
- "Add a new developer permission and map it to an employee permission"

## Why it was created

Creating permissions requires coordinated changes across 3-5 repositories with specific ordering constraints. This skill automates the multi-repo workflow, reducing a multi-hour manual process to a guided, mostly-automated flow.
