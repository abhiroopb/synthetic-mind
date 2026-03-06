# Navigation

> Add or update links in a web dashboard's sidebar navigation menu.

## What it does

This skill guides you through the multi-repository process of adding or modifying navigation items in a web dashboard sidebar. Navigation uses a double allow-list system: one repository defines which items exist (with URLs, entitlements, and translations), and a second repository controls how they're structured and rendered. The skill handles configuration, translations, type definitions, test fixtures, and provides a testing checklist for manual verification.

## Usage

Use this skill when you need to add, rename, reorder, or modify sidebar navigation items. Both the dashboard and header repositories must be cloned locally.

**Trigger phrases:**
- "Add a new nav link for transfers under banking"
- "Rename the nav item for deposits"
- "Reorder the sidebar navigation"
- "Add a navigation link to the dashboard"

## Examples

- `"Add a 'Transfers' link under the Banking section"` — Walks through all required changes: YAML config, translations, type definitions, test fixtures, and testing steps.
- `"Move the 'Balances' nav item above 'Checking'"` — Updates the structure configuration in both repositories to reflect the new ordering.

## Why it was created

Dashboard navigation changes span two repositories and five or more files, making them error-prone and easy to get wrong. This skill provides a guided, step-by-step process that ensures nothing is missed — from entitlement rules to translation strings to test updates.
