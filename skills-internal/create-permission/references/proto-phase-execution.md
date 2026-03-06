# Proto Phase Execution

If the plan has no Proto Phase operations, skip this entire file and proceed directly to the Config Phase.

Follow the **Git Hygiene** procedure (see `references/git-hygiene.md`) for each repo before editing any files.

## AddDeveloperEnum

File: `~/Development/java/multipass/multipass-protos/src/main/proto/squareup/multipass/permissions.proto`

- Find the last enum value in `RequestPermissionFlags`
- Append the new permission at the bottom, using the next sequential integer
- Format: `/** Description */ PERMISSION_NAME = N;`
- NEVER insert in the middle or reorder — this is a bitfield-packed enum

## AddEmployeeEnum

File: `~/Development/java/shared-protos/employees/src/main/proto/squareup/employees/employees.proto`

- Find the "Unified permissions" section (search for `// ## Unified permissions`)
- Find the `// Next enum: NNN` comment at the bottom of `EmployeePermissionFlags`
- For each enum to add: add the permission just above the comment using the next sequential value, then update the comment
- Format: `/** Description */ PERMISSION_NAME = NNN;`
- After adding all enums, the `// Next enum:` comment should reflect NNN + (number of enums added)
- Do NOT add to the legacy Register or Mobile sections at the top

## UpdateCertificationJSON

Before making any changes, tell the user:

> I'm about to update the Multipass certification test file (`logged_in_user_certification.json`). This is expected and not something you did wrong — every time a new employee enum is added, this file's byte arrays need to be updated to include the new permission bit. I'll run the certification test afterward to verify the update is correct.

When new employee permission enums are added, the Multipass certification test file must be updated. The file contains example users with byte-array-encoded permissions, and some users are expected to have ALL employee permissions set.

File: `~/Development/java/multipass/client/src/test/resources/certification/logged_in_user_certification.json`

The permissions are encoded as a bitset: enum value N sets bit N, stored as a byte array. Each byte holds 8 bits. When you add enum value N:
- Byte index = N / 8 (integer division)
- Bit position = N % 8
- The byte at that index needs bit (bit position) set

Find every `"permissions"` array in the JSON file that represents "all employee permissions" — these are the arrays that are all `255` values (every bit set) with a partial final byte. There are multiple occurrences (for example users `MultiunitOwner`, `MultiunitOwnerUnitView`, `DeviceCredential`, and their unit-view variants). Update the last byte of each one, or append a new byte if the new enum crosses a byte boundary (i.e., N % 8 == 0).

If multiple employee enums are being added, update the bitset for each one.

After updating the JSON, run the certification test to verify:
```bash
bazel test //multipass/client/src/test/java/com/squareup/multipass/client:all_tests_all_shards --test_filter=com.squareup.multipass.client.MultipassUserTest#exampleUsersWithAllEmployeePermissions
```

If the test still fails, read the test output to see what byte array the test expects vs what the JSON has, and correct the JSON file to match. Re-run the test until it passes.

## AddOAuthPermission

File: `~/Development/go/src/square/up/oauth/protos/squareup/oauth/v1/oauth-permission.proto`

- Add to the `OAuthPermission` enum
- Values are non-sequential — pick a value that doesn't conflict (check existing values)
- Include `enum_value_display_group`, `enum_value_status`, `enum_value_version` annotations
- The `enum_value_version` must be a valid Square API release train date (gathered in Stage 2), not the current date or commit date
- Add doc comment with HTTP methods

After editing the proto, the generated Go code (`go-protos/squareup/oauth/v1/oauth-permission.pb.go`) must be regenerated. The generation script can take several minutes on a cold machine (building protoc plugins, running `go mod vendor`), so hand it off to the user:

> I've updated the OAuth proto file. Now the generated Go code needs to be regenerated. Please run:
>
> ```
> cd ~/Development/go/src/square/up
> ./script/generate-proto ./oauth/protos/squareup/oauth/v1/oauth-permission.proto
> ```
>
> This regenerates the `.pb.go` file and runs `go mod vendor`. Let me know when it's done and I'll continue with the branch and PR.

Wait for the user to confirm before proceeding.

## AddOrUpdateSafeMapping

File: `~/Development/java/multipass/common/src/main/resources/multipass-permissions-map.yaml`

- Under `multipass.permissions.MAP`, find the correct alphabetical position
- If adding a new entry: add with the employee permission name, mapping to the developer permission
- If updating an existing entry: add the developer permission under the existing employee permission entry
- Format:
  ```yaml
  EMPLOYEE_PERMISSION_NAME:
    - permission: DEVELOPER_PERMISSION_NAME
      level: MERCHANT
  ```
- Keep alphabetical order within the MAP section

## Open Proto Phase PRs

Create branches and PRs using `gh`.

**IMPORTANT: Check Test Mode before creating any PR.** If test mode is active, add `--draft` and remove `--reviewer` from every `gh pr create` command.

**PR bodies**: Always write the PR body to a temp file and use `--body-file` instead of inline `--body`. This avoids shell interpolation issues with user-provided text (e.g., context/motivation that may contain special characters). This applies to ALL `gh pr create` commands across both phases.

You should already be on latest main from the Git Hygiene step. Create branches and PRs:

For the Java monorepo (Multipass proto and/or Employee proto and/or permissions map and/or certification JSON):
```bash
cd ~/Development/java
git checkout -b add-permission-PERMISSION_NAME
git add -A
git commit -m "Add PERMISSION_NAME permission"
gh pr create --title "Add PERMISSION_NAME permission" --body-file /tmp/pr-body.txt --reviewer "squareup/permissions-team"
```

For the Go monorepo (OAuth proto, if applicable):
```bash
cd ~/Development/go/src/square/up
git checkout -b add-permission-PERMISSION_NAME
git add -A
git commit -m "Add PERMISSION_NAME OAuth permission"
gh pr create --title "Add PERMISSION_NAME OAuth permission" --body-file /tmp/pr-body.txt --reviewer "squareup/permissions-team"
```

PR body should include:
- What the permission does and why it's needed
- Which operations were performed (added enums, updated mappings, etc.)
- Cross-references to related PRs (if multiple)
- Link to the ticket/task driving this work
