# RPI Research

> Research and document how existing code works using parallel sub-agents before planning or implementing changes.

## What it does

RPI Research is the research phase of the RPI (Research, Plan, Implement) methodology. It creates comprehensive, documented understanding of relevant code by decomposing a research question, spawning parallel sub-agents to investigate different aspects concurrently, synthesizing findings with file:line references, and producing a structured research document. The skill strictly documents what exists — it does not suggest improvements or critique the implementation.

## Usage

Invoke when starting a new feature, investigating unfamiliar code, or needing comprehensive understanding of how something works before planning changes. Each research session should have a single focused goal.

**Trigger phrases:**
- "Research how the checkout flow works"
- "Investigate the payment processing architecture"
- "I need to understand the auth system before making changes"
- "RPI research on the notification pipeline"

## Examples

- `"Research how the offline payments feature is currently implemented"`
- `"Investigate the data flow from API to database for order creation"`
- `"Document how the feature flag system works in this codebase"`

## Why it was created

Complex codebases require thorough understanding before safe changes can be planned. Rushing into implementation without research leads to missed dependencies and broken assumptions. This skill provides a structured research process that produces documented artifacts which carry context forward to the planning and implementation phases.
