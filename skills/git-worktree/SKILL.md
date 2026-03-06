---
name: git-worktree
description: "Manages git worktrees for working on multiple branches simultaneously. Use when asked to create, list, remove, or switch between git worktrees, or when needing to work on multiple branches in parallel."
---

# Git Worktree Management

Manages git worktrees to enable working on multiple branches of a repository simultaneously in separate directories.

## Capabilities

- **Create worktrees**: Add new worktrees for existing or new branches
- **List worktrees**: Show all active worktrees for a repository
- **Remove worktrees**: Clean up worktrees that are no longer needed
- **Switch context**: Help navigate between worktrees

## Workflows

### Create a new worktree

1. Ensure you're inside a git repository
2. Run `git worktree add <path> <branch>` to create a worktree for an existing branch
3. Or run `git worktree add -b <new-branch> <path> [base]` to create a new branch and worktree simultaneously
4. Confirm the worktree was created with `git worktree list`

**Convention**: Place worktrees as siblings of the main repo directory using the pattern `../<repo>-<branch>`:

```bash
# From /Development/my-repo (main worktree)
git worktree add ../my-repo-feature-x feature-x
git worktree add -b bugfix/issue-42 ../my-repo-bugfix-42 origin/main
```

### List all worktrees

```bash
git worktree list
```

Shows each worktree path, HEAD commit, and branch name.

### Remove a worktree

1. Run `git worktree remove <path>` to remove a worktree
2. If the worktree has uncommitted changes, use `--force` (only after confirming with the user)
3. Run `git worktree prune` to clean up stale worktree references

```bash
git worktree remove ../my-repo-feature-x
git worktree prune
```

### Lock/unlock a worktree

Lock a worktree to prevent accidental removal (useful for worktrees on removable media):

```bash
git worktree lock <path> --reason "Work in progress"
git worktree unlock <path>
```

## Best Practices

- Always `git fetch origin` before creating a worktree to ensure branches are up to date
- Use descriptive directory names that include the branch context
- Remove worktrees when done to avoid clutter and stale references
- Never manually delete a worktree directory — always use `git worktree remove`
- Run `git worktree prune` periodically to clean up stale entries

## Common Patterns

### Work on a PR review in a separate worktree

```bash
git fetch origin
git worktree add ../my-repo-pr-123 origin/pr-branch
# Review/test in the new worktree, then clean up
git worktree remove ../my-repo-pr-123
```

### Hotfix while working on a feature

```bash
git fetch origin
git worktree add -b hotfix/urgent ../my-repo-hotfix origin/main
# Fix, commit, push from the hotfix worktree
git worktree remove ../my-repo-hotfix
```
