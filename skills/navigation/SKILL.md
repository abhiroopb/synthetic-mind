---
Skill name: navigation
Skill description: Add or update links in a Dashboard navigation menu. Use when the user wants to add a new nav link, rename a nav link, reorder nav items, or modify the sidebar navigation in a web dashboard. Requires changes in both the dashboard and header repositories.
---

# Dashboard Navigation Skill

This skill guides you through adding or updating navigation links in a web dashboard sidebar. Navigation changes require coordinated modifications across two separate repositories: **dashboard** and **ecosystem-header**.

## Prerequisites: Locate Both Repositories

**Before making any changes, you must ask the user where both repositories are on their local filesystem.** Both must be cloned and accessible for you to complete this work.

Ask the user:
> I need access to both the `dashboard` and `ecosystem-header` repositories to make navigation changes. Can you tell me the paths to each on your filesystem?

If either repository is not cloned, inform the user they need to clone it before proceeding:

- `dashboard`: `https://github.com/your-org/dashboard`
- `ecosystem-header`: `https://github.com/your-org/ecosystem-header`

Do not attempt any navigation changes until you have confirmed paths to both repositories.

## How Navigation Works

Navigation uses a double allow-list system:

1. **dashboard** defines which nav items exist, their URLs, entitlements, and translations. It serves these via the `/dashboard/header` API response.
2. **ecosystem-header** determines how those nav items are structured and rendered in the sidebar UI (which items are grouped under which top-level categories).

A nav link will only appear if it is defined in **both** places.

## Step 1: Update the Dashboard Repository

You need to touch up to 5 files in the dashboard repo. Use the existing entries as a pattern to follow.

### 1a. `config/navigation/flat.yaml`

Define the new nav item. Each entry specifies its id, route, link URL, translation keys, tracking path, and entitlement rules (`include_for` / `exclude_for`).

Example — adding `banking.transfers` under `banking`:

```yaml
banking.transfers:
  route_name: banking.activity.transfers
  translation_key: nav.banking.transfers
  link: "/dashboard/banking/activity/transfers"
  title: title.nav.banking.transfers
  description: description.nav.banking.transfers
  tracking_path: banking.nav.transfers
  include_for:
    general:
      - can_see_deposits
    employee:
      - can_employee_dashboard_view_deposits
```

Key fields:

- **id**: Use dot notation to indicate hierarchy (e.g., `banking.transfers` means "transfers" nested under "banking").
- **route_name**: The route name for this page.
- **link**: The URL path the nav item points to.
- **translation_key**: Used to look up the display label in translations.
- **title / description**: Translation keys for the nav item's title and description.
- **tracking_path**: Used for analytics tracking.
- **include_for / exclude_for**: Entitlement rules controlling who sees this item. Ask the user which entitlements apply if not specified.

### 1b. `config/navigation/structure.yaml`

Add the nav item's id to the flat list that determines ordering. Place it near its parent/siblings:

```yaml
- id: banking
- id: banking_overview
- id: balances
- id: banking.transfers   # <-- add here, near siblings
```

### 1c. `config/navigation/tracking.yaml`

Add a tracking entry under the appropriate parent section:

```yaml
banking:
  nav:
    transfers: "transfers"
```

### 1d. `frontend/dashboard/config/translations/en.module.js`

Add three translation strings (maintain alphabetical order within each section):

- `'description.nav.banking.transfers': 'View your transfers'` — the description
- `'nav.banking.transfers': 'Transfers'` — the display label
- `'title.nav.banking.transfers': 'Transfers'` — the title

### 1e. `spec/lib/header/navigation_loader_spec.rb`

If the link URL already appears in the test's duplicate-link map, increment its count. If it's a new URL, no change is needed here.

## Step 2: Update the Ecosystem-Header Repository

You need to touch up to 3 source files plus related tests.

### 2a. `src/types/navigation.ts`

Add the new nav id to the `NavId` type union:

```typescript
export type NavId =
  | 'bitcoin'
  | 'savings'
  | 'credit_card'
  | 'banking.transfers'   // <-- add here
  | 'team-communication'
```

### 2b. `src/constants/leveled-nav-structure.ts`

Add the nav id to the appropriate parent's sub-level array in `DEFAULT_TOP_LEVEL_TO_SUB_LEVEL_MAP`. This controls which top-level category the item appears under:

```typescript
// Inside the banking top-level entry:
'banking_overview',
'balances',
'balances_employee',
'banking.transfers',   // <-- add here, among siblings
'checking',
```

### 2c. `src/fixtures/header-response.ts`

Add a fixture entry for the new nav item so tests can reference it. Follow the pattern of existing entries:

```typescript
{
  id: 'banking.transfers',
  link: '/dashboard/banking/activity/transfers',
  label: 'Transfers',
  title: 'Transfers',
  description: 'View your card transfers and activity',
  tracking_value: 'Global Navigation: Transfers',
  is_enabled: true,
  is_entitled: true,
},
```

### 2d. Update tests

Run existing tests and update any that break due to the new nav item (e.g., snapshot changes, array length assertions, or strict equality checks on nav structures). Tests are in `test/tests/`.

## Step 3: Test Changes (Requires Human)

**IMPORTANT: You MUST inform the user about these manual testing steps before finishing your work.** You (the agent) cannot test these changes end-to-end — the user must perform the verification themselves using staging environments and request redirectors. Do not skip or abbreviate this section.

### Locale string caveat

New translation strings added to `en.module.js` will **not** load on the staging environment until they have been deployed. Even if your local changes include the new strings, staging fetches translations from the deployed build — not from your branch.

There are two ways to handle this:

1. **Deploy locale strings first (recommended):** Open a separate dashboard PR containing _only_ your `en.module.js` changes. Merge it so the strings get deployed to staging. Once deployed, you can test the rest of your navigation changes with the real locale strings.
2. **Use existing locale strings temporarily:** For validation purposes, temporarily point your nav item's `translation_key`, `title`, and `description` at existing locale strings. Once you've confirmed the nav structure works, swap in your new locale strings before merging your final PR.

### 3a. Verify the dashboard header response

1. Deploy the dashboard branch to your staging environment.
2. Authenticate as a user that has the relevant entitlements.
3. Call `/dashboard/header` and inspect the response.
4. Confirm the new nav node is present with `is_entitled` and `is_enabled` set to `true`.

### 3b. Verify the nav renders correctly

1. Use a request redirector (like Requestly) to redirect the production header bundle to your local dev server.
2. Run ecosystem-header locally with `pnpm dev`.
3. Load staging — it will fetch the header response from your deployed dashboard and render nav using your local ecosystem-header.
4. Confirm the new nav link appears in the correct position under the correct parent.

## Step 4: Open PRs and Deploy

After testing confirms everything works:

1. Create a PR in each repository. Cross-link them in the PR descriptions so reviewers understand the full scope.
2. The **dashboard PR should be merged first** — it needs to be live so that the `/dashboard/header` response includes the new item before ecosystem-header tries to render it.
3. After the dashboard PR is merged, confirm the new nav item appears in the `/dashboard/header` response on production.
4. Merge the ecosystem-header PR.
5. Verify end-to-end after ecosystem-header is promoted to production.

## Important Context

There is ongoing work to simplify navigation development and consolidate it into a single repository. Until that work is ready, the two-repository approach described above is the correct process.
