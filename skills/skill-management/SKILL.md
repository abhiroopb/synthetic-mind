---
Skill name: skill-management
Skill description: Manage Amp agent skills: list, add, remove, inspect, and edit skills. Use when asked to manage skills, create new skills, or work with the skills directory.
---

# Skill Management

Manage Amp agent skills installed in `~/.agents/skills/` (user-global) and `.agents/skills/` (project-local).

## Capabilities

- **List skills**: Show all installed skills with their descriptions
- **Add/create skills**: Scaffold a new skill with proper structure (SKILL.md, scripts/, etc.)
- **Remove skills**: Delete a skill directory
- **Inspect skills**: Show full details of a skill (SKILL.md contents, scripts, directory structure)
- **Edit skills**: Modify an existing skill's SKILL.md or associated files

## Workflows

### List all installed skills

1. List directories in `~/.agents/skills/` (global) and `.agents/skills/` (project-local)
2. Read each `SKILL.md` frontmatter to extract name and description
3. Display a summary table

### Add a new skill

1. Ask the user for:
   - **name**: lowercase, hyphenated (e.g., `my-new-skill`)
   - **description**: what the skill does and when to use it
   - **type**: simple (SKILL.md only), with scripts, or with MCP
2. Create the directory at `~/.agents/skills/<name>/`
3. Generate `SKILL.md` with proper frontmatter following the building-skills conventions:
   - Name uses gerund form when possible
   - Description is third-person, includes what + when
   - Content is under 500 lines
4. Create `scripts/` subdirectory if needed
5. Validate the structure

### Remove a skill

1. Confirm the skill exists
2. Confirm with the user before deleting
3. Remove the skill directory

### Inspect a skill

1. Read the full `SKILL.md`
2. List all files in the skill directory
3. Display the skill's structure and contents

### Edit a skill

1. Read the current `SKILL.md`
2. Apply the requested changes using `edit_file`
3. Validate frontmatter remains correct

## Paths

| Scope | Path |
|-------|------|
| Global (user) | `~/.agents/skills/` → `/Users/abhiroop/.agents/skills/` |
| Project-local | `.agents/skills/` in workspace root |

## Frontmatter Validation Rules

When creating or editing skills, enforce:
- `name`: max 64 chars, lowercase + numbers + hyphens, no leading/trailing/consecutive hyphens, must match directory name
- `description`: max 1024 chars, third person, includes what + when to use
- SKILL.md body under 500 lines
- If MCP is bundled, `mcp.json` must use `includeTools` to filter exposed tools
