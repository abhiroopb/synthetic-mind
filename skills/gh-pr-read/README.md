# GitHub PR reader

> Read and summarize GitHub pull requests using the gh CLI.

## What it does

This skill reads and inspects GitHub pull requests — viewing details (title, description, status, reviewers, labels), reading diffs and changed files, inspecting comments and review threads, and summarizing changes. It uses the `gh` CLI for all operations, supporting both PR numbers and full URLs.

## Usage

Use when asked to read, review, summarize, or inspect a pull request. Supports structured JSON output for programmatic access and human-readable output for quick review.

## Examples

- "Summarize PR #1234 in the checkout repo"
- "Show me the diff for this PR: https://github.com/org/repo/pull/567"
- "List all open PRs by me in the dashboard repo"

## Why it was created

Reviewing PRs often requires switching to a browser and clicking through multiple tabs. This skill brings PR reading directly into the agent workflow, making it easy to inspect changes, read review comments, and understand PR scope without context-switching.
