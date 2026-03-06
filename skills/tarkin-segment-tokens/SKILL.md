---
name: tarkin-segment-tokens
description: Add or remove tokens (serial numbers, UUIDs) from audience segments. Use when asked to modify segment membership, add devices to a segment, or remove devices from a segment.
allowed-tools:
  - Bash(scripts/get-segment.sh:*)
  - Bash(scripts/update-segment-tokens.sh:*)
metadata:
  status: beta
---

# Segment Token Manager

Add or remove tokens from audience segments while preserving segment metadata.

## Workflow

1. **Ask the user for required information:**
   - Environment: staging or production?
   - Segment ID or name
   - Action: add or remove tokens?
   - List of tokens (serial numbers, UUIDs, etc.)

2. **Fetch the segment** using `scripts/get-segment.sh` to retrieve its details

3. **MANDATORY: Ask the user to confirm before modifying.** Display the segment details (ID, name, type, description, item count) and the planned action (tokens to add/remove). **Do NOT proceed until the user explicitly confirms.** This step must never be skipped.

4. **Update the segment** using `scripts/update-segment-tokens.sh` only after user confirmation

## Scripts

### Get a Segment

```bash
scripts/get-segment.sh <environment> --id <segment_id>
scripts/get-segment.sh <environment> --name <segment_name>
```
- `environment`: `staging` or `production`
- `--id`: Look up by numeric segment ID
- `--name`: Look up by segment name (supports spaces)
- Returns: JSON with segment details (name, type, description, item count)

### Add or Remove Tokens

```bash
scripts/update-segment-tokens.sh <environment> <segment_id> <action> <tokens> [--dry-run]
```
- `environment`: `staging` or `production`
- `segment_id`: Numeric segment ID
- `action`: `add` or `remove`
- `tokens`: Comma-separated list of tokens (e.g. `408CS14407400341,526CX2AM01400119`)
- `--dry-run`: Show the payload that would be sent without making any changes
- The script automatically fetches the segment first to preserve its name, description, and type
- Handles authentication automatically

## Example Sessions

### Single token modification

```
User: Remove serial number 408CS14407400341 from segment 50 on staging

Agent: I'll first fetch the segment to confirm.

[runs get-segment.sh staging --id 50]
Segment 50: "test segment" (SerialNumberSegment), 1 item

Agent: Please confirm:
- Environment: staging
- Segment: #50 "test segment" (1 current item)
- Action: Remove token 408CS14407400341

User: yes

[runs update-segment-tokens.sh staging 50 remove 408CS14407400341]
Success — token removed, segment updated.
```

### Bulk add from a CSV/list grouped by product type

For bulk operations with multiple product types, read `scripts/BULK-WORKFLOW.md` for the full workflow and naming conventions.

## Notes

- Segment name, description, and type are preserved automatically on updates
- API-automated segments cannot be modified (the API will reject the request)
- You must be an owner or audience manager of connected audiences to modify a segment
- Staging uses the staging URL, production uses the production URL
- Authentication is handled via your authenticated CLI
