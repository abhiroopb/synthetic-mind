# Troubleshooting

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Flag already exists" | Experiment name taken | Choose unique name or check if recreating existing experiment |
| "Invalid API token" | Token expired or wrong | Set env vars (`LAUNCHDARKLY_ACCESS_TOKEN`, `GROWTHBOOK_ACCESS_TOKEN`) or store in `./.env`, or run CLI interactively to enter tokens; check expiration and write permissions |
| "Holdout not found" | Holdout doesn't exist | Check available holdouts or use default |

## Users Not Entering Experiment

Checklist:
- [ ] Allocation flag is **enabled** in target environment
- [ ] User meets prerequisite conditions (not in holdout)
- [ ] Traffic percentage is > 0%
- [ ] User key is being passed to LaunchDarkly
- [ ] Bucketing flag default is `ineligible`, not `control`

## Wrong Variant Assignment

Checklist:
- [ ] Bucketing flag rules are configured correctly
- [ ] User key is passed **consistently** (same key = same bucket)
- [ ] No targeting rules override the percentage rollout
- [ ] Check LaunchDarkly flag evaluation debugger
- [ ] Code checks compare against exact string variants (`treatment`, `control`, `ineligible`)

## Exposure Logging Issues

- If logging looks imbalanced or missing, use `skills/scanning-experiment-health/SKILL.md` for targeted checks.

## API Reference

| Service | Detail |
|---------|--------|
| **LaunchDarkly API** | `https://app.launchdarkly.com/api/v2` |
| **Project Key** | `pie` |
| **Environments** | `staging`, `production` |
| **GrowthBook App** | https://growthbook-app.sqprod.co |
| **GrowthBook Tokens** | https://growthbook-app.sqprod.co/account/personal-access-tokens |
