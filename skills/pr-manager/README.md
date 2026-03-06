# PR Manager

> Commit changes, create PRs, and manage pull requests with support for stacked workflows.

## What it does

PR Manager automates the Git/GitHub pull request workflow from branch creation to PR submission. It auto-detects whether to use Graphite (for stacked PRs) or standard Git, handles branch naming conventions, generates PR descriptions from templates, and always creates PRs in draft mode. It also preserves human edits when updating existing PR descriptions.

## Usage

Invoke when you need to commit code, create a pull request, update an existing PR, or push changes for review. The skill auto-detects the best workflow — pass `"use standard git"` to skip Graphite.

**Trigger phrases:**
- "Commit and create a PR"
- "Push this as a draft PR"
- "Update the PR description"
- "Submit this stack"

## Examples

- `"Create a PR for this change with ticket LINEAR-123"`
- `"Push and create a draft PR, use standard git"`
- `"Update the existing PR description to reflect the new changes"`

## Why it was created

Managing PRs manually — especially stacked PRs with Graphite — involves many steps and easy-to-make mistakes like rebasing stacked branches from master. This skill automates the safe path and enforces draft mode to prevent accidental review requests.
