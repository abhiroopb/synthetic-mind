---
name: swarm
description: Use when exploring, investigating, researching, analyzing, validating, verifying, auditing, or examining complex topics that benefit from multiple perspectives. Covers redundant parallel exploration with adversarial challenge phases to build high-confidence findings through consensus.
---

# Swarm

Fan out agents with **mandatory redundancy** to independently explore tasks, then challenge findings through adversarial follow-up, then consolidate through consensus.

**Formula:** Total agents = (Number of Tasks) × 6 (3 exploration + 3 adversarial per task)

## Prerequisites

**STOP** and ask the user if:
- The task is simple enough that a single agent would suffice
- The task cannot be broken into independent units
- Output directory preference is unclear (default: `./swarm-output`)

## Phases

### Phase 1: Task Breakdown

1. Analyze the task description and break into independent task units
2. Create output directory if needed
3. Create a checklist to track: each task × 2 phases (exploration, adversarial)
4. Calculate agent count: N tasks × 6 agents

### Phase 2: Exploration (PARALLEL)

For each task, spawn 3 subagents in parallel:

- `{task}-A`, `{task}-B`, `{task}-C`

Each agent prompt:
- Assign the specific task
- Instruct to work independently and form own conclusions
- Request findings with file:line references, conclusions, and uncertainties
- Direct output to `{output_dir}/{task}-{instance}.md`

Wait for all Phase 2 agents to complete before proceeding.

### Phase 3: Adversarial Challenge (PARALLEL)

For each task, spawn 3 adversarial subagents in parallel:

- `{task}-adv-A`, `{task}-adv-B`, `{task}-adv-C`

Each agent prompt:
- Point to Phase 2 outputs: `{output_dir}/{task}-A.md`, `-B.md`, `-C.md`
- Instruct to DISPROVE or challenge Phase 2 findings
- Request: claims confirmed, claims refuted (with counter-evidence), claims unverified, gaps identified
- Direct output to `{output_dir}/{task}-adv-{instance}.md`

Wait for all Phase 3 agents to complete before proceeding.

### Phase 4: Consolidation

For each task, compare all 6 agent outputs and classify findings:

| Consensus Level | Meaning |
|-----------------|---------|
| Strong | All agents agree, adversarial agents confirm |
| Weak | Exploration agrees but adversarial found gaps |
| Disputed | Adversarial refuted with counter-evidence |
| Uncertain | Mixed results, needs investigation |

Report to user:
- Claims that survived adversarial challenge (high confidence)
- Claims refuted with counter-evidence (likely wrong)
- Gaps identified by adversarial agents
- Cross-task patterns (findings appearing/refuted across multiple tasks)

## Rules

- Never skip the adversarial phase—that's where errors get caught
- Phase 3 cannot start until Phase 2 completes (adversarial agents need exploration outputs)
- All agents in a phase launch in parallel
- Wait for all agents to complete before moving to next phase
- If an agent fails, note the failure and continue with remaining agents
- Update the checklist as each phase completes
