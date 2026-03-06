# KB Distill

> Compress raw memory observations into structured knowledge notes and propose behavioral rules.

## What it does

KB Distill is the middle layer of a knowledge flywheel: it takes raw observations captured across sessions and clusters them into actionable, synthesized notes. It identifies repeated patterns, topic clusters, decision chains, and inferred preferences — then proposes rules to codify those behaviors permanently. It can run automatically on session start when a backlog accumulates, or on demand.

## Usage

Trigger this skill when you want to synthesize accumulated observations into structured knowledge. It runs automatically when pending observations exceed 50 or the last distillation was more than 7 days ago.

**Trigger phrases:**
- "Distill my recent work"
- "Synthesize my observations"
- "What patterns have you noticed?"
- "Compress memory"
- "Distill the last month"

## Examples

- `"Distill"` — Runs the full workflow: gathers observations, clusters them, produces notes, and proposes rules for approval.
- `"What patterns have you noticed?"` — Analyzes observations and presents findings without saving, so you can review before committing.
- `"Distill and auto-approve all rules"` — Runs the full workflow and adds all proposed rules without individual confirmation.

## Why it was created

Over time, an AI agent accumulates hundreds of raw observations that become noisy and hard to use. KB Distill solves this by periodically compressing that raw material into concise, actionable knowledge — and surfacing implicit behavioral patterns the user may not have explicitly stated.
