# Dual-Flag Pattern

Experiments use two LaunchDarkly flags working together.

## Why Two Flags?

```
User Request
    |
    v
+------------------------+
| Traffic Allocation     |  <- "Should this user enter the experiment?"
| Flag (boolean)         |
+------------------------+
    |
    +-- false -> User is not in the experiment
    |
    +-- true
         |
         v
    +--------------------+
    | Bucketing Flag     |  <- "Which variant should they see?"
    | (string/JSON/num)  |
    +--------------------+
         |
         +-- "ineligible" -> Not in experiment / holdout
         +-- "control"    -> Baseline experience
         +-- "treatment"  -> New experience
```

## Benefits of Separation

1. Clean statistical analysis: only users who entered are analyzed.
2. Flexible traffic ramp-up without reconfiguring bucketing splits.
3. Proper holdout management via prerequisites.

## Traffic Allocation Flag

- Boolean flag: `true` means eligible for the experiment, `false` means not in the experiment.
- Audience filtering belongs here (e.g., geography or eligibility rules).
- Used as a prerequisite for the bucketing flag.

## Bucketing Flag

- Must include `ineligible`, `control`, `treatment` variants.
- The `ineligible` name must be exact to ensure proper bucketing.
- Uses traffic allocation as a prerequisite. If using a holdout, add it as a second prerequisite.

## Ramp-Up Behavior

- Keep bucketing at 50/50 for `control` and `treatment` from the start.
- Ramp by adjusting traffic allocation percentage only.
- Avoid ramp-downs during the experiment to prevent re-bucketing.
