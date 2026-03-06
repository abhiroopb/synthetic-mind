---
name: rebasing-git-branches
description: Rebases git branches onto their upstream target. Use when asked to rebase, update a branch, resolve rebase conflicts, or sync a branch with main/master.
---

# Rebasing Git Branches

Rebases the current or specified branch onto its upstream target branch, handling conflicts interactively.

## Capabilities

- Rebase current branch onto main/master or any target branch
- Interactive rebase (squash, reorder, edit commits)
- Resolve merge conflicts during rebase
- Abort or continue in-progress rebases
- Rebase onto upstream after fetching latest changes

## Workflows

### Standard Rebase onto Main

1. Run `git fetch origin` to get the latest remote state
2. Identify the target branch (default: `main`, fallback: `master`)
3. Run `git rebase origin/<target>` to rebase the current branch
4. If conflicts occur, follow the conflict resolution workflow below

### Interactive Rebase

1. Determine how many commits to include: `git log --oneline origin/main..HEAD`
2. Run `git rebase -i origin/main` (or specify commit count with `HEAD~N`)
3. Edit the rebase todo list as requested (squash, reword, reorder, drop)
4. Resolve any conflicts that arise

### Conflict Resolution

When a rebase pauses due to conflicts:

1. Run `git status` to identify conflicted files
2. Read each conflicted file to understand both sides
3. Edit files to resolve conflicts (remove conflict markers)
4. Stage resolved files with `git add <file>`
5. Continue with `git rebase --continue`
6. Repeat if more conflicts arise

### Abort a Rebase

If the rebase cannot be completed or the user wants to cancel:

1. Run `git rebase --abort` to return to the pre-rebase state

## Important Notes

- Always `git fetch origin` before rebasing to ensure up-to-date refs
- Never force-push (`git push --force-with-lease`) without explicit user consent
- When resolving conflicts, preserve the intent of both the current branch and the target branch changes
- If unsure about a conflict resolution, show both versions to the user and ask
