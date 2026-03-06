# State File

Create the `~/Development/create-permission/` directory if it doesn't exist.

Save the confirmed snapshot and plan to `~/Development/create-permission/PERMISSION_NAME_state.md`. Use the following structure. Include only the sections relevant to the plan's operations.

```markdown
# State: PERMISSION_NAME

## Created
ISO-8601 timestamp

## Context and Motivation
(User's full verbatim response, including any links they provided)

## Proto Phase PRs
- **Java monorepo**: PR URL (or: n/a)
- **Go monorepo**: PR URL (or: n/a)

## Plan
(List of operations in the plan with their status: complete / pending-config-phase)

## Snapshot

### Developer Permission
- **Name**: DEVELOPER_PERMISSION_NAME
- **Description**: Description text

### Developer Permission — OAuth
- **Display group**: DISPLAY_GROUP_NAME
- **HTTP methods**: GET
- **Status**: ALPHA/BETA/PUBLIC
- **Version**: 2025-01-01

### Developer Permission — SAFE Mapping
- **Employee enum**: EMPLOYEE_PERM_NAME (new or existing)
- **Level**: MERCHANT/UNIT/SELF

### Employee Permission
(repeat block for each enum)
- **Name**: EMPLOYEE_PERMISSION_NAME
- **Description**: Description text

### Display Permission
- **Permission ID**: lowercase_snake_case
- **Group**: reports
- **New group**: yes/no
- **New group icon**: chart-bar (only if new group)
- **New group position**: 5 (only if new group)
- **Access points**: all_access_points (or: spos, mpos, dashboard)
- **Parent permission**: none (or parent permission id)
- **Type**: regular
- **Feature flag**: none (or flag key)
- **Display name**: Human-readable name
- **Description text**: Optional description (or: none)
- **Permission set templates**: standard, enhanced (or: none)
- **Backing**: employee_enum / employee_enum_per_access_point / ui_only

### Display Permission — Employee Permission Mapping
(only if backing is employee_enum_per_access_point)
- **spos**: employee_enum_name
- **mpos**: employee_enum_name
- **dashboard**: employee_enum_name

### Backfill
- **Needed**: yes/no
- **Type**: all/conditional/none
- **Prerequisite permission**: none (or permission id, for conditional)
```

Tell the user:

> I've saved the state file at **`~/Development/create-permission/PERMISSION_NAME_state.md`** so I can pick up the Config Phase without asking you anything again. Don't edit this file.
>
> **You're responsible for getting your PRs approved and merged.** I created them and tagged the Permissions team for review, but you'll need to follow up, address any review comments, and merge them yourself.
>
> Once your proto PR(s) merge and all-protos republishes, come back and say **"Config Phase for PERMISSION_NAME"**.

## Single-Pass Flow (No Proto Phase Operations)

If the plan has no Proto Phase operations (e.g., display-only, mapping update to existing enums), there are no proto changes and no all-protos dependency. In this case:

1. Skip Proto Phase Execution and the Proto Phase PRs step entirely.
2. After Targeted Q&A, proceed directly to the Config Phase, but skip the BumpAllProtos operation (there are no proto changes to bump).
3. Follow the **Git Hygiene** procedure for `~/Development/permissions-config` before executing.
4. Save state as usual, noting that there are no Proto Phase PRs and no Config Phase re-invocation needed.
5. Replace the closing message with: "No proto changes were needed, so there's no Config Phase to come back for. Your permissions-config PR is ready for review and can be merged once CI passes and the Permissions team approves."
