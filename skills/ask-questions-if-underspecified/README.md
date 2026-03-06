# Ask Questions If Underspecified

> Clarify ambiguous requirements before starting implementation.

## What it does

Analyzes a task request for ambiguity and missing details, then asks the minimum set of clarifying questions needed to avoid wrong work. It identifies gaps in objectives, acceptance criteria, scope, constraints, and environment — presenting concise multiple-choice questions with sensible defaults. The skill pauses implementation until must-have answers arrive.

## Usage

Invoke explicitly when a task feels underspecified or has multiple plausible interpretations. This skill is not used automatically — only when deliberately triggered.

Trigger phrases:
- "Clarify this before I start"
- "Ask questions if underspecified"
- "What do I need to know before implementing this?"

## Examples

- "This ticket is vague — clarify the requirements before I start"
- "Ask me the right questions so we can scope this properly"
- "I'm not sure what 'done' looks like here — help me clarify"

## Why it was created

Starting implementation on an ambiguous request wastes time and leads to rework. This skill forces a structured pause to resolve unknowns before committing to a direction.
