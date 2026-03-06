# Auto-Pilot

> Orchestrates all installed skills automatically — routes any request to the right skill(s) without asking.

## What it does

Acts as a universal skill router. When you give it a task, it parses your intent, matches it against a comprehensive routing table spanning communication, code, data, infrastructure, testing, and PM workflows, then loads and executes the appropriate skill(s). For cross-domain tasks, it chains multiple skills in sequence. It never asks which skill to use — it decides and acts.

## Usage

This is the default skill that runs on every prompt. It matches any actionable request and dispatches to the correct skill. You don't need to invoke it explicitly — just describe what you want done.

Trigger phrases:
- Any actionable request (it routes automatically)
- "Search Slack for...", "Create a Linear ticket...", "Deploy to staging...", etc.

## Examples

- "Find the Linear ticket for cash rounding and post a summary to Slack"
- "Check my calendar for tomorrow and draft a decline for the 2pm meeting"
- "Search code for the payment processor interface across all repos"

## Why it was created

With dozens of specialized skills installed, manually choosing which one to load adds friction. Auto-pilot eliminates that overhead by routing automatically based on intent, making the agent feel like a single unified tool.
