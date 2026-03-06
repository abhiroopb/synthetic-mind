# Git worktree

> Manage git worktrees for working on multiple branches simultaneously in separate directories.

## What it does

This skill manages git worktrees — creating new worktrees for existing or new branches, listing active worktrees, removing finished ones, and locking/unlocking worktrees. It follows a naming convention that places worktrees as sibling directories of the main repo for easy navigation.

## Usage

Use when you need to work on multiple branches in parallel without stashing or switching. Common patterns include reviewing a PR in a separate worktree, creating a hotfix while working on a feature, or isolating experimental work.

## Examples

- "Create a worktree for the feature-x branch"
- "List all active worktrees for this repo"
- "Remove the worktree for the hotfix branch"

## Why it was created

Switching branches disrupts your working state — you lose build caches, have to stash changes, and lose context. Git worktrees let you work on multiple branches simultaneously in separate directories, and this skill manages the lifecycle cleanly.
