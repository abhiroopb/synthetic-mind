# Early feature access

> Add new features to the Early Feature Access page in the merchant dashboard.

## What it does

This skill automates the full workflow of adding a feature to an Early Feature Access (EFA) system. It collects feature identity, UI content, media, and ordering through interactive prompts, then creates the config directory, TypeScript config file, translation strings, and feature registration. It runs typecheck, lint, and tests to verify everything works, then commits and creates a PR.

## Usage

Use when adding a new feature to the Early Feature Access page. The skill walks you through collecting all required inputs (feature slug, scopes, UI copy, images) before generating the code changes.

## Examples

- "Add penny-round-up to Early Feature Access"
- "Set up a new EFA feature for checkout convergence"
- "Register a new early access feature with localized images"

## Why it was created

Adding a feature to EFA requires touching multiple files (config, translations, registration, images) with specific conventions. This skill eliminates manual boilerplate and ensures all files stay in sync.
