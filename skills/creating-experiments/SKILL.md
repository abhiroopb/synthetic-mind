---
Skill name: creating-experiments
Skill description: Use when creating, launching, setting up, configuring, building, implementing, or debugging A/B experiments, dual-flag patterns, traffic allocation flags, bucketing flags, holdout prerequisites, or ramping experiment traffic. Also use when following the experiments runbook or linking experiments to GrowthBook.
---

# Creating Experiments

## Prerequisites

- Pass `LAUNCHDARKLY_ACCESS_TOKEN` and `GROWTHBOOK_ACCESS_TOKEN` as environment variables, or run the CLI in interactive mode to enter tokens (they will be persisted for future requests).
- No holdout is used by default. Pass `--holdout <flag-key>` to use one.

**If tokens are missing or invalid**, the CLI will detect this and provide links. Relay these to the user:
- **LaunchDarkly token**: https://app.launchdarkly.com/settings/authorization
- **GrowthBook token**: `https://<growthbook-instance-url>/account/personal-access-tokens`

**STOP** if unclear whether holdout should be used (confirm with stakeholder).

## Runbook

Follow the experiments runbook phases. For detailed phase information, fetch the runbook from internal docs (see References section).

## Launch CLI (Non-Interactive)

```bash
# Create a dual-flag experiment (no holdout by default)
experiments-cli create-experiment \
  --name "my-experiment" \
  --description "Test experiment"

# Create with a holdout
experiments-cli create-experiment \
  --name "my-experiment" \
  --description "Test experiment" \
  --holdout "growth-2026-q1-holdout"
```

Other commands:

```bash
# View experiments created by you
experiments-cli view-experiments

# Create a GrowthBook experiment for an existing bucketing flag
# Valid areas: onboarding-web, dashboard-web, mobile
experiments-cli create-growthbook-experiment \
  --flag "my-experiment-bucketing" \
  --area "onboarding-web"

# Open the runbook in a browser (may fail in headless envs)
experiments-cli view-docs
```

## Workflow

When a user requests to create an experiment:

1. **Gather experiment details** - Get the experiment name, description, and whether a holdout is needed
2. **Create the experiment** - Run `create-experiment` immediately with the provided details
3. **Prompt about GrowthBook** - After successful creation, use `AskUserQuestion` to ask:
   - "Do you want to create a GrowthBook experiment for this flag?"
   - If yes, ask which area: onboarding-web, dashboard-web, or mobile
4. **Create GrowthBook experiment** (if requested) - Run `create-growthbook-experiment` with the bucketing flag (derived from experiment name as `<experiment-name>-bucketing`) and selected area

## Flag Configuration Essentials

- **Bucketing flag** (`<experiment>-bucketing`): string/JSON/number with variants `ineligible`, `control`, `treatment`.
- The `ineligible` variant name must be exact; it represents users not in the experiment and holdout users.
- **Traffic allocation flag** (`<experiment>-traffic-allocation`): boolean used as a prerequisite for the bucketing flag.
- Put audience filtering on the traffic allocation flag (e.g., country, eligibility rules).
- If using a holdout, add it as a prerequisite flag for the bucketing flag.
- Default flag values in code should be `ineligible` (not `control`).

## Verification

After creation, the CLI outputs direct links to verify the flags/experiments:

- **LaunchDarkly flags**: Links to each flag's targeting page (allocation, bucketing, and holdout if used)
- **GrowthBook experiments**: Link to the experiment detail page

Use these CLI-provided links to verify configuration rather than searching through list views.

## References

When you need detailed guidance beyond this skill, use the `internal-docs` skill to fetch documentation:

```
/internal-docs fetch https://<internal-docs-url>/docs/develop/web/general-development/experiments/experiments-runbook
/internal-docs fetch https://<internal-docs-url>/docs/develop/web/general-development/experiments/exposure-logging
```

Local references (CLI-specific content not in internal docs):
- [Dual-Flag Pattern](references/dual-flag-pattern.md) - Architecture diagram for the two-flag system
- [Troubleshooting](references/troubleshooting.md) - CLI errors and debugging checklists

## Related Skills

- [internal-docs](../dev-guides/SKILL.md) - Fetch experiments runbook and other documentation from internal docs
- [launchdarkly](../launchdarkly/SKILL.md) - Query existing flag status (read-only operations)
- [scanning-experiment-health](../scanning-experiment-health/SKILL.md) - Exposure logging and health checks
