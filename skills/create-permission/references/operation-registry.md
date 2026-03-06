# Operation Registry

Each operation represents a discrete unit of work. The plan derived from the intake form is a list of these operations. Operations declare which phase they belong to and what fields they require from the snapshot.

## Proto Phase Operations

These operations change proto files or files in the same repo/PR. They must be completed and merged before Config Phase operations can run.

**AddDeveloperEnum**
- Adds a new enum to `RequestPermissionFlags` in the auth proto.
- Required: `developer_permission.name`, `developer_permission.description`
- Repo: `~/Development/java`
- File: `auth/auth-protos/src/main/proto/permissions.proto`

**AddEmployeeEnum**
- Adds one or more new enums to `EmployeePermissionFlags` in the Employee proto. Supports creating multiple enums in one pass (e.g., for per-access-point mappings that need separate enums per surface).
- Required: `employee_permission.enums[]` (each with name, description)
- Repo: `~/Development/java`
- File: `shared-protos/employees/src/main/proto/employees/employees.proto`

**UpdateCertificationJSON**
- A required mechanical side-effect of adding an employee enum. The auth certification test file contains example users that must have every employee permission bit set, so adding a new enum means updating byte arrays in that file. This is not something the user did wrong — it's expected every time an employee enum is added. Always co-occurs with AddEmployeeEnum.
- Required: employee enum values (derived from AddEmployeeEnum execution)
- Repo: `~/Development/java`
- File: `auth/client/src/test/resources/certification/logged_in_user_certification.json`

**AddOAuthPermission**
- Adds a new enum to `OAuthPermission` in the OAuth proto.
- Required: `developer_permission.name`, `developer_permission.oauth.*`
- Repo: `~/Development/go/src/app/up`
- File: `oauth/protos/oauth/v1/oauth-permission.proto`

**AddOrUpdateSafeMapping**
- Adds or modifies an entry in the API gateway authorization permissions map.
- Required: `developer_permission.safe_mapping.*`
- Repo: `~/Development/java`
- File: `auth/common/src/main/resources/permissions-map.yaml`

## Config Phase Operations

These operations depend on new proto enums being available in `all-protos`. If the plan has no Proto Phase operations, Config Phase operations run immediately in a single pass.

**BumpAllProtos**
- Bumps the `all-protos` dependency in consumer repos to pick up new proto enum values.
- Prerequisites: Proto Phase PRs merged, all-protos republished
- Repos: `~/Development/java`, `~/Development/go/src/app/up`, `~/Development/roster-rails`, `~/Development/dashboard`

**AddOrUpdateDisplayPermission**
- Adds or modifies a display permission config in permissions config YAML, including locale entries. Handles all three backing modes: `employee_permission: true` (simple shorthand), `employee_permission_mapping` (per-access-point enums), and UI-only (no employee backing).
- Required: `display_permission.id`, `display_permission.group`, `display_permission.access_points`, `display_permission.display_name`, `display_permission.backing`
- Repo: `~/Development/permissions-config`
- Files: `config/permissions/GROUP.yml`, `config/locales/permissions.en.yml`

**UpdatePermissionSetTemplates**
- Adds the display permission to standard and/or enhanced permission set templates.
- Required: `display_permission.id`, `display_permission.permission_set_templates`
- Repo: `~/Development/permissions-config`
- File: `config/permissions/permission_set_templates.yml`

**BackfillGuidance**
- Provides guidance on backfill scripts. Non-code — only explains options and commands.
- Required: `backfill.*`

## Plan Derivation Rules

From the confirmed snapshot, derive the list of operations needed:

- If a new developer permission name is specified → queue `AddDeveloperEnum`
- If a new employee permission name (or names) is specified → queue `AddEmployeeEnum` + `UpdateCertificationJSON`
- If OAuth is needed → queue `AddOAuthPermission`
- If a SAFE mapping is needed → queue `AddOrUpdateSafeMapping`
- If a display permission is specified → queue `AddOrUpdateDisplayPermission`
- If permission set templates are specified → queue `UpdatePermissionSetTemplates`
- If backfill is needed → queue `BackfillGuidance`
- If any Proto Phase operations are in the plan → queue `BumpAllProtos` (for Config Phase)

Apply guardrails:

- If the plan includes a display permission with `backing: employee_enum` or `backing: employee_enum_per_access_point` AND a SAFE mapping, but no employee permission enums: warn the user that the permissions map requires an employee enum as the join key between display and developer permissions. Ask if they should add employee enum creation to the plan.
- If the plan includes `AddOrUpdateDisplayPermission` with `backing: employee_enum_per_access_point` but only one employee enum is listed: ask whether all access points use the same enum or whether additional enums need to be created.
- If the plan includes modifications to existing permissions/mappings (intake form references an existing permission ID that already exists in the codebase): confirm with the user whether this is an update to an existing permission or a naming conflict.

Present the plan to the user:

> Here's what I plan to do:
>
> **Proto Phase** (requires all-protos publish before Config Phase):
> - [list each Proto Phase operation with a one-line summary]
>
> **Config Phase:**
> - [list each Config Phase operation with a one-line summary]
>
> Does this look right? Anything missing or wrong?

If the plan has no Proto Phase operations, say:

> Here's what I plan to do (single pass, no proto dependency):
>
> - [list operations]
>
> Does this look right?

Wait for the user to confirm before proceeding.
