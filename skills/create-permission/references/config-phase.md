# Config Phase

The Config Phase is only needed when proto changes were made in the Proto Phase. If the state file shows no proto changes, there is no Config Phase — the permissions-config work was already completed in the single-pass flow.

Read saved state from `~/Development/create-permission/PERMISSION_NAME_state.md`. If the file doesn't exist, tell the user to run the Proto Phase first.

**Suppress noisy output**: The Config Phase runs many git, bundle, and build commands. Use quiet flags (`-q`, `--quiet`) and redirect stdout to `/dev/null` wherever possible so the user only sees meaningful output (PR URLs, errors). All commands below already include these flags — do not remove them.

## Step 0: Confirm State and Validate

After reading the state file, echo back the key values to the user and ask them to confirm before proceeding. Display: which operations are planned, permission names, Proto Phase PR URLs, and for display permissions the permissions-config details (group, access points, parent, display name, backing mode, per-access-point mapping if applicable). Do NOT proceed until the user confirms. This catches any accidental edits or file corruption between phases.

Then verify that the saved state is still valid against the current codebase. Check ALL of the following:

- **Permission group exists** (if display permission in plan): confirm the group still exists in `~/Development/permissions-config/config/permissions/permission_group_ordering.yml` (unless it's a new group).
- **Parent permission exists** (if display permission has a parent): confirm that permission ID still exists in the relevant group's YAML file under `permissions:`.
- **Permission set templates are valid** (if templates are specified): confirm those template IDs exist in `~/Development/permissions-config/config/permissions/permission_set_templates.yml`.
- **No naming conflicts**: confirm the permission names/IDs don't already appear in the relevant protos or permissions-config YAML configs (another change may have landed between phases).
- **Proto Phase PRs merged**: check the PR URLs from the state file and confirm they are merged. If not, warn the user that the Config Phase depends on those PRs being merged and all-protos having republished.

If any check fails, stop and tell the user exactly what's wrong and how to fix it. Do not proceed with the Config Phase.

## Step 1: Environment Pre-Flight

Before running any bump commands, verify the environment is ready. Check ALL of the following and report all failures at once (don't stop at the first one):

- **VPN**: Run `dig +short internal.dns.example.com` and check that it returns an IP address. If it returns nothing, tell the user: "VPN doesn't appear to be connected. The all-protos bump commands need access to internal package registries. Please connect to VPN and tell me when you're ready."
- **Ruby repos** (roster-rails, dashboard, permissions-config): Non-interactive shells don't load Ruby version managers automatically. Before ANY Ruby or Bundler command in the Config Phase, initialize the user's Ruby version manager. Detect which one is available by checking in this order:
  1. **rbenv**: `eval "$(rbenv init - 2>/dev/null)"`
  2. **rvm**: `source ~/.rvm/scripts/rvm 2>/dev/null`
  3. **mise**: `eval "$(mise activate bash 2>/dev/null)"`
  4. **asdf**: `source "$(brew --prefix asdf 2>/dev/null)/libexec/asdf.sh" 2>/dev/null`

  For the pre-flight check, run the appropriate init command, then `cd REPO_PATH && ruby -v && bundler -v` for each repo. If Ruby or Bundler isn't available after initialization, tell the user which repo has the issue and suggest they set up the Ruby environment.

**Do not proceed until all pre-flight checks pass.** If any check fails, wait for the user to fix it and tell you to continue. Then re-run ALL checks to confirm. Never skip a failing check and never tell the user to run bump commands manually — the skill handles all commands.

## Step 2: BumpAllProtos

Run these commands in sequence. Each one updates the all-protos dependency to pick up the new proto enum values. Create a branch and PR for each repo.

**IMPORTANT: Check Test Mode before creating any PR.** If test mode is active, add `--draft` and remove `--reviewer` from every `gh pr create` command.

**PR bodies**: Always write the PR body to a temp file and use `--body-file` instead of inline `--body`. This avoids shell interpolation issues with user-provided text. This applies to ALL `gh pr create` commands in the Config Phase.

After running the bump command for each repo, check whether there are actually any changes with `git diff --quiet`. If there are no changes, the all-protos update may not have picked up the new proto yet. Skip the commit/PR for that repo and record it as "no changes detected."

If a bump command fails despite pre-flight checks passing, tell the user what went wrong and wait for them to fix the underlying issue. Then retry the command yourself — never tell the user to run it.

**Java monorepo** (only if employee permission was added):
```bash
cd ~/Development/java
git checkout -q -b bump-all-protos-PERMISSION_NAME
./script/update-external-protos > /dev/null
git add -A
git diff --quiet --cached && echo "NO_CHANGES" || (git commit -q -m "Bump all-protos for PERMISSION_NAME" && gh pr create --title "Bump all-protos for PERMISSION_NAME" --body-file /tmp/pr-body.txt --reviewer "<org>/permissions-team")
```

**Go monorepo**: Skip the Go proto bump in this step. It is handled separately in Step 8 because `make update` takes 10-15 minutes, which exceeds the agent's fixed Bash execution timeout.

**Roster-Rails** (initialize the user's Ruby version manager before running bundle):
```bash
cd ~/Development/roster-rails
git checkout -q -b bump-all-protos-PERMISSION_NAME
bundle update all-protos --quiet
git add -A
git diff --quiet --cached && echo "NO_CHANGES" || (git commit -q -m "Bump all-protos for PERMISSION_NAME" && gh pr create --title "Bump all-protos for PERMISSION_NAME" --body-file /tmp/pr-body.txt --reviewer "<org>/permissions-team")
```

**Dashboard** (initialize the user's Ruby version manager before running bundle):
```bash
cd ~/Development/dashboard
git checkout -q -b bump-all-protos-PERMISSION_NAME
bundle update all-protos --quiet
git add -A
git diff --quiet --cached && echo "NO_CHANGES" || (git commit -q -m "Bump all-protos for PERMISSION_NAME" && gh pr create --title "Bump all-protos for PERMISSION_NAME" --body-file /tmp/pr-body.txt --reviewer "<org>/permissions-team")
```

After all repos are attempted, give the user a summary:
> **All-protos bump results:**
> - Java: [PR link / no changes detected / skipped (no employee permission)]
> - Go: deferred to Step 8
> - Roster-Rails: [PR link / no changes detected]
> - Dashboard: [PR link / no changes detected]
>
> [If any had no changes]: "Some repos had no changes — all-protos may not have republished yet. You can re-run the Config Phase later to retry those."

## Step 3: AddOrUpdateDisplayPermission

If the plan does not include this operation, skip to Step 5.

This goes in the SAME branch/PR as the permissions-config all-protos bump (if applicable).

Initialize the user's Ruby version manager, then:
```bash
cd ~/Development/permissions-config
git checkout -q -b add-permission-PERMISSION_NAME
bundle update all-protos --quiet
```

If there are no proto changes to bump (single-pass flow), skip the `bundle update all-protos` command and just create the branch.

### Find a Similar Permission

Before writing any YAML, search for an existing permission that's closest to what the user needs:

```bash
rg "employee_permission: true" ~/Development/permissions-config/config/permissions/ -l
rg "employee_permission_mapping:" ~/Development/permissions-config/config/permissions/ -l
rg "access_points: all_access_points" ~/Development/permissions-config/config/permissions/
```

Read the closest match and use it as a template. This is the most reliable way to get the format right.

### Add Permission Config

Edit the appropriate group file in `~/Development/permissions-config/config/permissions/GROUP.yml`:

1. Under `permission_groups.GROUP.subgroups`, add the permission ID to the relevant header's `permissions` list (or create a new subgroup header).

2. Under `permissions:`, add the permission config. Use the simplest form that works:

   **Backed by employee enum, name matches** (display permission ID matches lowercased employee enum name, all access points):
   ```yaml
   permission_id:
     employee_permission: true
     access_points: all_access_points
   ```
   `employee_permission: true` is a shorthand: it uses the permission id as the Employee proto enum name. e.g., permission id `run_shift_report` resolves to `EmployeePermissionFlags::RUN_SHIFT_REPORT` at boot time. This requires `access_points` to be set. This is the preferred approach for new unified permissions.

   **Backed by employee enum, name differs** (single enum but display ID doesn't match):
   ```yaml
   permission_id:
     employee_permission_mapping:
       spos: employee_enum_name
       mpos: employee_enum_name
       dashboard: employee_enum_name
   ```

   **Backed by different employee enums per access point**:
   ```yaml
   permission_id:
     employee_permission_mapping:
       spos: employee_enum_name
       mpos: mobile_employee_enum_name
       dashboard: employee_dashboard_enum_name
   ```
   Enum names are lowercase in YAML and resolved to uppercase proto enums via `Protos.enum_from_name` (which calls `.to_s.upcase`).

   **UI-only display permission (no employee enum backing)**:
   ```yaml
   permission_id:
     access_points: all_access_points
   ```
   Omit `employee_permission` and `employee_permission_mapping` entirely. The display permission exists purely as a UI element. If it should not be persistable (e.g., a structural grouping node), set `flag: false`.

   **With optional fields** (add only what's needed):
   ```yaml
   permission_id:
     employee_permission: true
     access_points: all_access_points
     description: true          # only if description text exists in locale file
     visible_if:
       feature_flag: team/flag  # only if feature-flagged
     children:                  # only if has children
       - child_permission_id
   ```

   **Key fields reference** (only include fields you need, everything has sensible defaults):
   - `flag:` - defaults to the permission id. Set to `false` to make the permission non-persistable (display-only, e.g., internal child nodes like `_view_history`). Set to a string to override the flag name. Never set to `true`.
   - `type:` - defaults to `regular`. Other values: `inherit_parent` (auto-enabled with parent), `full_access_only` (only for Full Access sets).
   - `es2_id:` - defaults to the permission id. Set to `false` for no ES2 mapping.
   - `translation_key:` - defaults to `permissions.name.PERMISSION_ID`. Override only if the display name locale key differs from the permission id.
   - `double_write:` - a permission id or list of ids to also enable when this permission is enabled. Used for legacy compatibility.
   - `visible_if:` / `hidden_if:` - mutually exclusive. Can contain `feature_flag:`, `computed:`, `legacy_user_permission:`, or `always: true`.

### Add Locale Entries

Edit `~/Development/permissions-config/config/locales/permissions.en.yml`:

Under `en.permissions.name`, add:
```yaml
      permission_id: "Display Name"
```

If description text was provided, under `en.permissions.description`, add:
```yaml
      permission_id: "Description text"
```

Keep entries in the same general area as other permissions in the same group.

## Step 4: UpdatePermissionSetTemplates

If the plan does not include this operation, skip to Step 5.

If the user chose Standard or Enhanced, edit `~/Development/permissions-config/config/permissions/permission_set_templates.yml`:

Add `- id: permission_id` under the appropriate template's `permissions` list, grouped with related permissions (add a comment with the group name).

## Step 5: Commit Em-Permissions PR

If no permissions-config changes were made (no display permission or template operations in the plan), skip this step.

**IMPORTANT: Check Test Mode before creating this PR.** If test mode is active, add `--draft` and remove `--reviewer` from the `gh pr create` command.

```bash
cd ~/Development/permissions-config
git add -A
git commit -q -m "Add PERMISSION_NAME permission config + bump all-protos"
gh pr create --title "Add PERMISSION_NAME permission to permissions-config" --body-file /tmp/pr-body.txt --reviewer "<org>/permissions-team"
```

PR body should cross-reference the Proto Phase PRs.

## Step 6: BackfillGuidance

If the plan does not include this operation, skip to Step 7.

If the user indicated a backfill is needed, explain the options. **DO NOT execute any backfill scripts** — only provide guidance. These scripts modify production merchant data and must be run manually by the user.

All backfill scripts live in `~/Development/permissions-config/script/` and take a token file in the format `ENTITY_TOKEN PERMISSION_SET_TOKEN1,PERMISSION_SET_TOKEN2,...` (one line per merchant). The entity token is used for lookup, but updates happen at the permission set level. Token files can be generated with `generate_tokens_for_backfill.rb`.

**Enable on ALL permission sets** (most common for new permissions):
- Script: `backfill_any_permission.rb`
- Enables the permission on every permission set in the token file, unconditionally
- Usage: `be script/backfill_any_permission.rb --max-qps 100 --tokens-file FILENAME --permissions-to-update PERMISSION_ID`

**Conditional backfill** (only permission sets with a prerequisite permission):
- Script: `backfill_default_permission.rb`
- Only updates permission sets that already have a specific prerequisite permission enabled
- Useful when the new permission is a sub-permission of an existing one
- Usage: `be script/backfill_default_permission.rb --max-qps 100 --tokens-file FILENAME --with-permissions PREREQUISITE_PERMISSION --permissions-to-update PERMISSION_ID`

**Sync legacy permissions**:
- Script: `backfill_synchronize_permission.rb`
- Re-syncs legacy and display permissions on permission sets to be consistent

Tell the user: "Backfill scripts need to be run after your permissions-config PR merges and deploys. You'll need to generate a token file with `generate_tokens_for_backfill.rb` and coordinate with your team on rate limiting. Reach out in the permissions support channel if you need help with the backfill."

## Step 7: Output Summary

> **Config Phase progress.** Here are the PRs created so far:
>
> - All-protos bumps: [links to each PR created]
> - Em-permissions config: [link] (if display permission in plan)
>
> These PRs can be merged in any order once CI passes. The permissions-config PR includes both the all-protos bump and the config changes, so there's no ordering dependency there.
>
> **The Go proto bump still needs to be done.** See below.

Then immediately proceed to Step 8.

## Step 8: Go Proto Bump

Tell the user:

> I can't run the Go proto bump because `make update` takes 10-15 minutes, which exceeds my fixed Bash execution timeout. Please run the following commands yourself:
>
> 1. `cd ~/Development/go/src/app/up`
> 2. `git checkout master`
> 3. `git pull`
> 4. Verify you have no working changes: `git status`
> 5. `cd go-protos`
> 6. `make update`
>
> This will take 10-15 minutes. The resulting diff will be large (typically 300-900 changed files) — this is normal. Let me know when it's done and I'll handle the branch, commit, and PR.

Wait for the user to confirm `make update` is complete. Then:

1. If an employee permission was added, copy the updated certification JSON from the Java monorepo to the Go monorepo:
   ```bash
   cp ~/Development/java/auth/client/src/test/resources/certification/logged_in_user_certification.json ~/Development/go/src/app/up/client/auth/resources/certification/logged_in_user_certification.json
   ```

2. Create the branch and stage all changes from the repo root:
   ```bash
   cd ~/Development/go/src/app/up
   git checkout -q -b bump-all-protos-PERMISSION_NAME
   git add -A
   ```

3. If an employee permission was added, verify the Go certification test passes:
   ```bash
   cd ~/Development/go/src/app/up
   go test ./client/auth/ -run TestExampleUsersWithAllEmployeePermissions
   ```
   If the test fails, read the output to see the expected vs actual byte arrays, correct the JSON file, and re-run until it passes.

4. Commit and open the PR:

   **IMPORTANT: Check Test Mode before creating this PR.** If test mode is active, add `--draft` and remove `--reviewer` from the `gh pr create` command.

   ```bash
   cd ~/Development/go/src/app/up
   git commit -q -m "Bump all-protos for PERMISSION_NAME"
   gh pr create --title "Bump all-protos for PERMISSION_NAME" --body-file /tmp/pr-body.txt --reviewer "<org>/permissions-team"
   ```

Then give the final summary:

> **All done.** Here are all your PRs:
>
> - All-protos bumps: [links to Java, Go, Roster-Rails, Dashboard PRs]
> - Em-permissions config: [link] (if display permission in plan)
>
> **You're responsible for getting these PRs approved and merged.** I created them and tagged the Permissions team for review, but you'll need to follow up, address any review comments, and merge them yourself.
>
> **After everything merges:**
> - Run backfill scripts if needed (see guidance above)
> - Verify the display permission appears correctly in the team permissions UI (if display permission was created)
> - Test API gateway authorization with the new permission (if developer permission with auth mapping was created)
