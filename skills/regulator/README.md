# Regulator

> Search and query the internal account lookup tool for accounts, cases, payments, and actions.

## What it does

Regulator provides access to the primary operational dashboard for viewing and managing customer accounts. It supports lookups by account token via a legacy JSON API and richer queries via a GraphQL gateway. You can look up account details, query cases, search actions, and generate clickable links to the account dashboard UI for further investigation.

## Usage

Invoke when you need to look up a seller, find account details by token, query risk/compliance cases, or search for actions on an account.

**Trigger phrases:**
- "Look up this merchant"
- "Find account details for this token"
- "Query cases for this seller"
- "Search for this account"

## Examples

- `"Look up account token ABC123DEF456"`
- `"Find all cases for this merchant token"`
- `"Search for accounts matching this email address"`

## Why it was created

Looking up account and merchant data is a frequent operational task that involves navigating multiple APIs and UI pages. This skill streamlines the process by providing structured access to both the legacy API and GraphQL gateway, with direct links to the dashboard UI.
