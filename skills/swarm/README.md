# Swarm

> Fan out multiple agents with mandatory redundancy to explore complex topics, then challenge findings through adversarial review and consolidate through consensus.

## What it does

Breaks a complex task into independent units, then assigns three parallel agents to each unit for independent exploration. After exploration completes, three adversarial agents per task attempt to disprove or challenge the findings. Results are consolidated into a confidence-rated report classifying claims as strong consensus, weak consensus, disputed, or uncertain. The formula is 6 agents per task (3 exploration + 3 adversarial).

## Usage

Use for complex investigations that benefit from multiple perspectives and high-confidence validation.

- "Swarm investigate [topic]"
- "Use swarm to explore [complex question]"
- "Run a swarm analysis on [codebase area]"

## Examples

- `"Swarm investigate why checkout latency spiked last week"`
- `"Use swarm to audit our payment error handling across all services"`
- `"Run a swarm analysis on the tradeoffs between approach A and approach B"`

## Why it was created

Single-agent exploration can miss edge cases or produce overconfident conclusions. The swarm pattern uses redundant exploration plus adversarial challenge to catch errors and build genuinely high-confidence findings through consensus.
