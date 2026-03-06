# Skill Management

> List, add, remove, inspect, and edit Amp agent skills from the terminal.

## What it does

Skill Management provides a complete workflow for managing Amp agent skills installed globally (`~/.agents/skills/`) or locally (`.agents/skills/`). You can list all installed skills with descriptions, scaffold new skills with proper frontmatter structure, remove skills, inspect a skill's full contents and directory structure, and edit existing skill definitions. It enforces naming conventions and frontmatter validation rules.

## Usage

Invoke when you need to manage your skill library — listing what's installed, creating new skills, removing old ones, or editing existing skill definitions.

**Trigger phrases:**
- "List my skills"
- "Create a new skill"
- "Remove this skill"
- "Show me the details of this skill"
- "Edit the description of this skill"

## Examples

- `"List all installed skills"`
- `"Create a new skill called 'deploy-checker' that verifies deployments"`
- `"Inspect the slack skill"`

## Why it was created

Managing skills involves multiple file system operations and knowing the correct frontmatter format. This skill centralizes those operations and enforces conventions so new skills are created correctly the first time.
