# Project Status

> Synthesize a comprehensive project status report by pulling context from six data sources in parallel.

## What it does

Project Status gathers signals from Slack messages, Google Drive documents, GitHub pull requests, a company directory, LaunchDarkly feature flags, and a project tracker (roadmap). It runs all six data-gathering steps in parallel, then synthesizes findings into a structured status report covering active work, rollouts, blockers, key people, tech debt, and more. It also cross-references contributors against the company directory to flag departed team members.

## Usage

Invoke when you need to summarize project status, generate a progress report, recap recent activity, assess project health, or review rollout and feature flag state. Provide a project name or keyword.

**Trigger phrases:**
- "What's the status of project X?"
- "Generate a status update for the checkout feature"
- "Recap recent activity on the payments project"

## Examples

- `"Get me a status report on the checkout redesign"`
- `"Summarize what's happened on offline-payments in the last 7 days"`
- `"Check the rollout state for project-x repo:org/repo"`

## Why it was created

Project status is scattered across many tools — Slack, Google Docs, GitHub, feature flags, and roadmap trackers. Manually gathering context from all these sources is time-consuming. This skill automates the cross-source synthesis into a single, structured report.
