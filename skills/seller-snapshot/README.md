# Seller Snapshot

> Generate a comprehensive 360° customer snapshot with account details, financial metrics, support history, and a timeline of key events.

## What it does

Seller Snapshot queries a data warehouse to compile a complete view of a customer account. It pulls account profile and revenue data, GPV metrics, device inventory, SaaS subscriptions, risk events, recent support interactions, account manager calls, and contact frequency — then presents everything in a structured report with tables and a chronological timeline of significant events.

## Usage

Invoke when you need to understand a customer's full relationship with the platform. You'll be asked for an account token, and the skill runs 8 SQL queries to build the snapshot.

**Trigger phrases:**
- "Look up this seller"
- "Create a merchant snapshot"
- "Get a 360° view of this account"
- "Generate a seller report"

## Examples

- `"Generate a seller snapshot for account token ABC123DEF456"`
- `"Give me a 360 view of this merchant"`
- `"Look up the full profile for this seller"`

## Why it was created

Understanding a customer's full picture requires querying multiple data tables across support, revenue, hardware, subscriptions, and risk. This skill automates all those queries and presents a unified view, saving significant time when preparing for customer conversations or investigating issues.
