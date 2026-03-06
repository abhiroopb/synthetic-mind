---
Skill name: push-pr
Skill description: Pushes current branch and creates a draft PR with AI-generated description. Use when asked to "push pr", "create pr", or "push and create pr".
---

# Push and Create Draft PR

Pushes the current branch to origin and creates a draft PR with an AI-generated description.

## Prerequisites

Before starting, verify:
1. You're in a git repository: `git rev-parse --git-dir`
2. GitHub CLI is available: `which gh`
3. There are commits to push: `git log origin/HEAD..HEAD --oneline`

## Workflow

### 1. Get Branch Info

```bash
CURRENT_BRANCH=$(git branch --show-current)
BASE_BRANCH=$(git rev-parse --abbrev-ref origin/HEAD 2>/dev/null | sed 's|origin/||' || echo "main")
```

### 2. Push to Origin

```bash
git push -u origin "$CURRENT_BRANCH"
```

### 3. Find PR Template

Check these locations in order:
1. `.github/pull_request_template.md`
2. `pull_request_template.md`
3. `docs/pull_request_template.md`

### 4. Analyze Changes

1. Run `git diff origin/$BASE_BRANCH..HEAD` to see what changed
2. Read the actual changed files to understand context
3. Run `git log origin/$BASE_BRANCH..HEAD --oneline` to see commit messages

### 5. Generate PR Description

- Use bulletpoint form when necessary for readability
- Emphasize maximum readability

If a PR template exists:
- Follow the template structure exactly
- Answer each section in readable, human-friendly sentences

If no template:
- Write a clear summary of what changed and why
- Include any breaking changes or migration notes

### 6. Create Draft PR

```bash
gh pr create --draft --title "<conventional-commit-style-title>" --body "<generated-description>"
```

Title format: `feat(scope): TICKET-123 description` or `fix(scope): description`

### 7. Confirm Creation

```bash
gh pr view --json url -q .url
```

Report the PR URL to the user.
