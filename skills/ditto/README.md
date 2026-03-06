# Ditto

> Create and manage staging test accounts for mobile app testing.

## What it does

This skill interfaces with a staging test account management system to create, configure, and manage test accounts. It can generate accounts with various configurations (debit cards, addresses, business accounts), simulate transactions, manage tags for organizing accounts, and configure feature flag targeting. All data is synthetic staging data.

## Usage

Use when you need to generate, provision, look up, delete, or tag staging test accounts, simulate transactions, or configure feature flags for testing. All operations are staging-only.

## Examples

- "Create a new US test account with a debit card and address"
- "Add $50 to test account C_XXXXXXXXXX"
- "Target my test account for the new-checkout feature flag"

## Why it was created

Setting up staging test accounts manually is tedious and error-prone. This skill automates the entire lifecycle — from account creation to transaction simulation to feature flag targeting — so engineers can focus on testing rather than setup.
