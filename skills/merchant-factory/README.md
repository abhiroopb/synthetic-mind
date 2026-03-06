# Merchant Factory

> Create and configure staging test accounts with subscriptions, catalogs, and customers.

## What it does

Merchant Factory automates the creation of staging test accounts via a test data factory API. It can create accounts with specific country codes and payment configurations, add subscriptions (restaurant, retail, appointments, marketing, etc.), generate product catalogs, create test customers, add locations, link bank accounts, and generate magic login links. It supports the full lifecycle of test data setup for QA and development.

## Usage

Use this skill when you need test accounts in a staging environment for development or QA purposes.

**Trigger phrases:**
- "Create a test account"
- "Create a staging merchant"
- "Set up a test restaurant with a catalog"
- "Add a restaurants-plus subscription to this account"
- "Generate a magic link for this test account"

## Examples

- `"Create a US test restaurant with payments activated"` — Creates a staging account with US country code and activated payments, returns the account token.
- `"Add restaurants-plus and marketing subscriptions to account XXXXX"` — Adds the specified plan subscriptions to the existing account.
- `"Generate a catalog for this POS account with 10 items per page"` — Creates a simple catalog with the specified grid configuration.

## Why it was created

Setting up test accounts manually through staging UIs is slow and error-prone. This skill automates the entire process — from account creation to subscription setup to catalog generation — in a single workflow, saving significant time during development and testing.
