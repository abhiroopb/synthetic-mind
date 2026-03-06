# Targeted Q&A

For each operation in the plan, check whether all required fields are present in the snapshot. Only ask about fields that are missing or ambiguous. Ask one question at a time, grouped by operation.

## Missing fields for AddDeveloperEnum
- Name (validate: `^[A-Z][A-Z0-9_]+$`, must not already exist in `~/Development/java/multipass/multipass-protos/src/main/proto/squareup/multipass/permissions.proto`)
- Description

## Missing fields for AddEmployeeEnum
- Enum name(s) (validate: `^[A-Z][A-Z0-9_]+$` for each, must not already exist in `~/Development/java/shared-protos/employees/src/main/proto/squareup/employees/employees.proto`)
- Description(s) for each enum

## Missing fields for AddOAuthPermission
- OAuth display group: show existing `DisplayGroup` enum values from the OAuth proto (these are unrelated to em-permissions permission groups)
- HTTP methods
- Status (ALPHA/BETA/PUBLIC)
- API version (`enum_value_version`): read the OAuth proto and show the most recent `enum_value_version` date as a reference. Tell the user: "The `enum_value_version` must be a Square API release train date. You can find upcoming release train dates here: https://www.notion.so/2a970293beed806d8896f0e48dbae04e — pick the train you're targeting. If you're not sure which train to target, ask in #square-dev-releases."

## Missing fields for AddOrUpdateSafeMapping
- Employee enum to map under: if an employee permission is being created in this run, default to the new enum and tell the user ("The developer permission will be mapped under the new employee permission you're creating."). If NOT creating an employee permission, show the alphabetical list from `multipass-permissions-map.yaml` and ask.
- Authorization level: "What authorization level? MERCHANT (merchant-wide access), UNIT (location-scoped access), or SELF (user's own data only). The level doesn't currently affect enforcement, so if you're at all unsure, just go with MERCHANT."

## Missing fields for AddOrUpdateDisplayPermission
- Display permission ID (validate: `^[a-z][a-z0-9_]*$`, must not already exist in `~/Development/em-permissions/config/permissions/` unless this is an update). If backed by a single employee enum being created in this run, default to the lowercased enum name and confirm.
- Permission group: read `~/Development/em-permissions/config/permissions/permission_group_ordering.yml` and show the list. If none fit, ask for new group details (name, icon from the Market icon set, ordering position).
- Access points: "Where should this display permission be available? Options: `spos` (Square POS on iPad/Square Register), `mpos` (mobile POS on phones), `dashboard` (Square Dashboard web app), or `all_access_points` (all of them)."
- Parent permission: read the chosen group YAML file and list existing top-level permissions. "Should this be a child of an existing permission in this group?" Let the user pick one or say no.
- Permission type: if the permission has a parent, ask: "What type? `regular` (default, independently toggled), `inherit_parent` (auto-enabled with parent), or `full_access_only` (only for Full Access sets)." If no parent, ask: "Should this permission be available to all permission sets, or restricted to Full Access only?" Default to `regular`.
- Feature flag: "Should this display permission be gated behind a feature flag? If yes, what's the flag key? Note: this skill only handles simple feature flags. For more complex visibility logic (`computed`, `legacy_user_permission`), you can manually configure `visible_if` after the PR is created."
- Display name: "What should the seller-facing name be in the Dashboard permissions UI?"
- Description text: "Optional: a longer description shown below the permission name in the UI. Say 'none' if the name is self-explanatory."
- Backing mode (if not already clear): "How should this display permission connect to employee permissions?"
  - `employee_enum` — single employee enum, same for all access points (uses `employee_permission: true` shorthand if name matches, or `employee_permission_mapping` with same enum for all if name differs)
  - `employee_enum_per_access_point` — different employee enums per access point (uses `employee_permission_mapping` with different enums)
  - `ui_only` — no employee enum backing
- Per-access-point mapping (if backing is `employee_enum_per_access_point`): "Which employee enum should be used for each access point?" Ask for spos, mpos, and dashboard enum names (lowercase in YAML, resolved to uppercase via `Protos.enum_from_name`). These may be new enums being created in this run or existing enums already in the proto.

## Missing fields for UpdatePermissionSetTemplates
- Which templates: "Should this display permission be included in any default permission set templates? Standard (basic permissions for cashiers, baristas), Enhanced (advanced permissions for managers, shift leads), or both? Full Access gets everything automatically."

## Missing fields for BackfillGuidance
- Backfill type: "After deployment, do existing permission sets need to be updated? All sets (unconditional), only sets with a prerequisite permission (conditional), or none (sellers opt-in themselves)?"
- Prerequisite permission (if conditional): "Which existing permission should a set already have enabled in order to receive this new permission?"

## Context and motivation

If the intake form didn't include context/motivation, or the extracted context is sparse, ask: "The Permissions team will review this change, so it helps to give them context. Why is this permission being created? What feature or project is driving it? Please be thorough — include any relevant details like the team requesting it, the product area, and any links to design docs, PRDs, Jira tickets, or Slack threads, even if I can't access them directly. The reviewers will be able to."

Save the user's full response verbatim. It will be included in PR bodies and the state file.
