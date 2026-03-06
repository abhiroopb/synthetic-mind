---
name: early-feature-access
description: "Adds new feature content to Early Feature Access (EFA) page in Dashboard. Creates square-web config, translations, images, and registration. Use when adding a feature to Early Feature Access or EFA."
allowed-tools:
  - Bash(git:*)
  - Bash(nx:*)
  - Bash(pnpm:*)
  - Bash(grep:*)
  - Bash(find:*)
  - Bash(gh:*)
  - Bash(source:*)
  - Read
  - Write
  - Grep
  - Glob
  - Task
---

# Adding a New Feature to Early Feature Access

This skill automates adding a new feature to the Early Feature Access (EFA) system in square-web.

## What This Skill Does

- Creates feature config directory and TypeScript config file
- Adds translation strings to `en.json`
- Imports and wires up localized images (if provided)
- Registers the feature in the content index
- Runs typecheck, lint, and tests to verify

## Prerequisites

### Repository Setup

**The agent MUST perform these steps before collecting inputs.** Do not skip any step.

1. **Ensure the square-web repo is available.** If it is not cloned locally, clone it:
   ```bash
   git clone git@github.com:squareup/square-web.git
   cd square-web
   ```
2. **Start from a clean, up-to-date main branch:**
   ```bash
   git checkout main
   git pull origin main
   ```
3. **Create a new feature branch** using the naming convention `efa/<feature-name>`:
   ```bash
   git checkout -b efa/<feature-name>
   ```
   If the feature name is not yet known, ask the user for it first, then create the branch.
4. **Activate hermit** (once per shell, if not already activated):
   ```bash
   source ./bin/activate-hermit
   ```
5. **Install dependencies** (if needed):
   ```bash
   pnpm install
   ```

### Required Information

Before starting, the user should know or be asked for:

1. **Feature name** (kebab-case, e.g. `penny-round-up`)
2. **CLS field enum value** (e.g. `ClsField.PENNY_ROUND_UP_TOGGLE`) — must already exist in the proto types
3. **Scopes** — which `EarlyFeatureAccessScope` and `Scope` values apply (MERCHANT, LOCATION, DEVICE). **NOTE**: Choosing MERCHANT scope is mutually exclusive with LOCATION/DEVICE scopes.
4. **UI content** — title, subtitle type, feature list bullets, details modal text
5. **Images** — whether localized images are needed, and for which locales

## Workflow

### Step 1: Collect Inputs

**IMPORTANT: Do NOT proceed to Step 2 until ALL required inputs have been collected.** Collect inputs interactively across multiple prompts, grouped by topic. Accept any information the user volunteers in their initial message and skip prompts for fields already provided.

#### Input Validation

**Before using any user-provided value in a shell command, file path, or code template, validate it:**

- **Feature slug**: Must match `^[a-z0-9]+(-[a-z0-9]+)*$`. Reject and re-prompt if it contains spaces, underscores, uppercase letters, or special characters.
- **CLS field enum**: Must match `^ClsField\.[A-Z0-9_]+$`. Reject if it contains anything other than uppercase letters, digits, and underscores after the prefix.
- **YouTube video ID**: Must match `^[a-zA-Z0-9_-]+$`. Reject if it contains special characters.
- **Image directory path**: Must be a valid filesystem path with no shell metacharacters (`;`, `&`, `|`, `$`, `` ` ``, etc.). Reject and re-prompt if suspect characters are found.

**Always quote all interpolated values in shell commands** (e.g., `git checkout -b "efa/${featureName}"`, `find "${imageDir}" -type f`).

If any value fails validation, inform the user what format is expected and ask them to provide a corrected value. Do not proceed until all inputs pass validation.

#### Prompt 1 — Feature identity

Ask for:
1. **Feature slug** (kebab-case, e.g. `penny-round-up`) — this becomes the direct URL path to the feature: `/dashboard/early-feature-access/<feature-slug>`
2. **CLS field enum** (e.g. `ClsField.PENNY_ROUND_UP_TOGGLE`)
3. **EFA scopes** — MERCHANT, LOCATION, and/or DEVICE? (Note: MERCHANT is mutually exclusive with LOCATION/DEVICE)

#### Prompt 2 — UI content

Ask for:
1. **Title** (English) — e.g. `"Penny Round Up"`
2. **Subtitle** (English) — e.g. `"Launching this spring"`
3. **Feature list bullets** — 1 or more key benefits
4. **Details modal description** — longer description shown in the details modal

#### Prompt 3 — Media (optional)

Ask if the feature needs any of the following (the user can skip all):
1. **YouTube video ID** — e.g. `b4-7l2oGmMY`
2. **Localized images** — list of locales + files
3. **squareOneFeature gating** — e.g. `Feature.RETAIL` (optional per bullet)

If the user provides localized images, check that each file is under 500KB:

```bash
find <image-directory> -type f -size +500k
```

If any images exceed 500KB, tell the user which files are too large and ask them to provide smaller versions before proceeding. Do not continue until all images are under 500KB.

#### Prompt 4 — Feature ordering

Read the file at `libs/rdm/routes-device-management/src/early-feature-access-content/index.ts` (relative to the square-web repo root) to get the current list of registered features. Use the **absolute path** based on the repo location (e.g. `~/Development/square-web/libs/rdm/routes-device-management/src/early-feature-access-content/index.ts`). Print the list to the user in order and ask where the new feature should appear. For example:

> Here are the current features in order:
> 1. checkout-convergence-item-details
> 2. penny-round-up
> 3. ...
>
> Where should the new feature appear in this list?

#### Summary confirmation

Before proceeding, print a summary of all collected inputs and ask the user to confirm they are correct.

#### Prompt 5 — Translation

Ask the user: **"Do you want to submit these strings for translation?"**

- **If yes**: No additional changes needed — the strings in `en.json` will be picked up by the translation pipeline.
- **If no**: In Step 3, also add the top-level feature translation key to `atlas_settings.yaml` to be ignored. Add the key `mfeEarlyFeatureAccess.featureContent.<camelCaseFeatureName>` to the ignore list so it is excluded from translation.

### Step 2: Verify CLS Field Exists in Protos

After collecting the CLS field enum value from the user, check that it exists in the repo:

```bash
grep -r "PENNY_ROUND_UP_TOGGLE" --include="*.ts" .
```

(Replace `PENNY_ROUND_UP_TOGGLE` with the actual enum value provided by the user.)

- **If the enum value is found**: Protos are up to date. Proceed to Step 3.
- **If the enum value is NOT found**: Run `nx protos:update` and commit the result as a separate commit before proceeding:
  ```bash
  nx protos:update
  git add .
  git commit -m "Update protos"
  ```
  Then re-verify the enum value exists before continuing.

### Step 3: Implement square-web Changes

**Use subagents (Task tool) to parallelize independent work.** The following groups edit different files and can be run concurrently as separate subagents:

- **Subagent 1**: A (Create Feature Content Directory) + B (Create Feature Config File)
- **Subagent 2**: C (Add Translation Strings to `en.json`)
- **Subagent 3**: D (Register the Feature in `index.ts`)

Provide each subagent with all collected inputs and the relevant reference file paths.

All paths are relative to `libs/rdm/routes-device-management/src/`.

#### A. Create Feature Content Directory

```
early-feature-access-content/<feature-name>/
├── <feature-name>.ts
└── images/          (only if images provided)
    ├── 1x/
    │   ├── <feature-name>-en-US.png
    │   └── ... (other locales)
    └── 2x/
        ├── <feature-name>-en-US.png
        └── ... (other locales)
```

#### B. Create Feature Config File

Follow the pattern in the existing features. Read these files for reference:
- `early-feature-access-content/penny-round-up/penny-round-up.ts` (simple, no images, uses YouTube video)
- `early-feature-access-content/checkout-convergence-item-details/checkout-convergence-item-details.ts` (with images)
- `early-feature-access-content/types.ts` (type definitions)

Key rules:
- Import `EarlyFeatureAccessScope`, `ClsField`, `Scope` from proto packages
- Import type `EarlyAccessFeature` from `../types`
- Translation keys are RELATIVE (e.g. `'title'`, `'earlyAccessFeatureCard.featureListItem1'`)
- The UI prefixes them with `mfeEarlyFeatureAccess.featureContent.<camelCaseFeatureName>.`
- `earlyFeatureAccessScopes` = scopes for CLS evaluation
- `scope` = scopes for writing to Settings Hub (must correspond to EFA scopes)
- If images exist, import each locale+size and build `localizedImageSet` map

**Without images:**
```typescript
import { EarlyFeatureAccessScope } from '@squareup/shared-types-protos/squareup/cls/fields/earlyfeatureaccess/early_feature_access.js';
import { ClsField } from '@squareup/shared-types-protos/squareup/cls/model/cls_field';
import { Scope } from '@squareup/shared-types-protos/squareup/settingshub/model/scope';
import type { EarlyAccessFeature } from '../types';

export const yourFeatureName: EarlyAccessFeature = {
  field: ClsField.YOUR_FIELD_TOGGLE,
  earlyFeatureAccessScopes: [EarlyFeatureAccessScope.EARLY_FEATURE_ACCESS_SCOPE_MERCHANT],
  scope: [Scope.SCOPE_MERCHANT],
  titleTranslationKey: 'title',
  featureCardSubtitleKey: 'earlyAccessFeatureCard.launchDate',
  featureList: [
    { translationKey: 'earlyAccessFeatureCard.featureListItem1' },
    { translationKey: 'earlyAccessFeatureCard.featureListItem2' },
  ],
  details: [
    {
      titleTranslationKey: 'title',
      descriptionTranslationKey: 'detailsModal.description',
    },
  ],
};
```

**With images:**
```typescript
// ... same imports plus image imports:
import enUS1x from './images/1x/your-feature-en-US.png';
import enUS2x from './images/2x/your-feature-en-US.png';
// ... repeat for each locale

// In details:
details: [
  {
    titleTranslationKey: 'title',
    descriptionTranslationKey: 'detailsModal.description',
    localizedImageSet: {
      'en-US': { '1x': enUS1x, '2x': enUS2x },
      // ... other locales
    },
  },
],
```

**With YouTube video:**
```typescript
details: [
  {
    titleTranslationKey: 'title',
    descriptionTranslationKey: 'detailsModal.description',
    youtubeVideoId: 'VIDEO_ID_HERE',
  },
],
```

#### C. Add Translation Strings

Add to `translations/en.json` under `mfeEarlyFeatureAccess.featureContent.<camelCaseFeatureName>`:

```json
{
  "title": "Your Feature Name",
  "detailsModal": {
    "description": "Detailed description of the feature."
  },
  "earlyAccessFeatureCard": {
    "launchDate": "Launching this spring",
    "featureListItem1": "First key benefit",
    "featureListItem2": "Second key benefit"
  },
  "installFeatureModal": {
    "confirmationDialog": {
      "customCopy": "You can make changes anytime until [date].",
      "featureName": "your feature display name"
    },
    "description": "Choose where you'd like to install this feature."
  }
}
```

**Validation**: Every `translationKey` referenced in the config TS file MUST have a corresponding entry in `en.json`.

#### D. Register the Feature

Update `early-feature-access-content/index.ts`:
1. Add import for the new feature
2. Add it to the `earlyFeatureAccessContent` record

#### E. Verify

**Run each verification command in its own subagent** to preserve context. These three subagents can run concurrently:

- **Subagent 4**: `nx typecheck routes-device-management`
- **Subagent 5**: `nx lint routes-device-management --fix`
- **Subagent 6**: `nx test routes-device-management --watch=false`

Each subagent should report back whether its command passed or failed, and include any error output. **If any subagent reports a failure, fix the errors and re-run the failing command(s) in new subagents.** Do not move to Step 4 until all three commands pass cleanly (0 typecheck errors, 0 lint errors, all tests passing).

### Step 4: Commit and Push

Once all verification passes, commit all changes:

```bash
git add .
git commit -m "feat(routes-device-management): Add <feature-name> to Early Feature Access"
```

**Before pushing, show the user a summary of the changes** (e.g., `git diff main --stat` and a brief description of what was added) **and ask for explicit approval** before proceeding. Do not push or create a PR until the user confirms.

Once the user approves, push the branch and create a pull request:

```bash
gh pr create --title "feat(routes-device-management): Add <feature-name> to Early Feature Access" --body "Adds EFA config, translations, and registration for <feature-name>." --base main
```

### Step 5: Output Summary

Provide the user with:
1. Confirmation that the PR was created and pushed
2. Link to the created PR
3. List of files changed/created in square-web
4. A checklist:
   - [ ] Tested in staging: `https://app.squareupstaging.com/dashboard/early-feature-access`

## Scope Mapping Reference

| EarlyFeatureAccessScope | Scope (SettingsHub) | Use Case |
|------------------------|---------------------|----------|
| `EARLY_FEATURE_ACCESS_SCOPE_MERCHANT` | `SCOPE_MERCHANT` | Feature applies to entire merchant |
| `EARLY_FEATURE_ACCESS_SCOPE_LOCATION` | `SCOPE_LOCATION` | Feature per-location |
| `EARLY_FEATURE_ACCESS_SCOPE_DEVICE` | `SCOPE_DEVICE` | Feature per-device |

DEVICE and LOCATION scopes can be combined. MERCHANT scope cannot be combined with other scopes.

## Supported Locales for Images

Based on existing features, the standard locale set is:
`en-US`, `es-US`, `en-CA`, `fr-CA`, `en-GB`, `en-IE`, `en-AU`, `fr-FR`, `es-ES`, `ca-ES`, `ja-JP`

## Additional Resources

- Slack: #early-feature-access
- Google Doc: https://docs.google.com/document/d/1e4fQebENXqCQIjlpNnAUiGczEeu2bUgEGkL7nbkL71Y/edit?tab=t.jgobnw5ri873
- Figma designs: Search "Early Feature Access" in Figma
