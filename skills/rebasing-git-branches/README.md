# Rebasing Git Branches

> Rebase git branches onto their upstream target with interactive conflict resolution.

## What it does

This skill handles rebasing the current or specified branch onto its upstream target branch. It supports standard rebases onto main/master, interactive rebases for squashing or reordering commits, and guides you through conflict resolution when conflicts arise. It always fetches the latest remote state before rebasing and never force-pushes without explicit consent.

## Usage

Invoke when you need to rebase a branch, update a branch with the latest changes from main, resolve rebase conflicts, or perform an interactive rebase to clean up commits.

**Trigger phrases:**
- "Rebase my branch onto main"
- "Update this branch"
- "Resolve rebase conflicts"
- "Squash my last 3 commits"

## Examples

- `"Rebase this branch onto main"`
- `"Interactive rebase to squash my last 5 commits"`
- `"Help me resolve these rebase conflicts"`

## Why it was created

Rebasing can be risky — wrong commands can result in lost work or messy commit histories. This skill automates the safe rebasing workflow, handles conflict resolution interactively, and ensures you always fetch before rebasing.
