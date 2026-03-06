# Market React

> Reference documentation for a design system's React UI components.

## What it does

Market React provides comprehensive reference documentation for React components in a design system library. It covers stable and trial components, import paths, API signatures, and common pitfalls. The skill includes 39 component reference docs and a pitfalls guide documenting wrong-vs-correct patterns. It distinguishes between stable components (production-ready) and trial components (may have breaking API changes).

## Usage

Use this skill when building, debugging, styling, migrating, or reviewing React components that use the design system. Load the component index to find the right reference file, and check the pitfalls guide to avoid common mistakes.

**Trigger phrases:**
- "How do I use the Modal component?"
- "What's the API for Button?"
- "Show me the Select component props"
- "What are the common pitfalls with design system components?"
- "Is Table stable or trial?"

## Examples

- `"How do I use the Modal component?"` — Loads the Modal reference doc with props, usage examples, and known gotchas.
- `"What are the common mistakes with these components?"` — Loads `references/pitfalls.md` showing wrong→correct patterns.
- `"Is Combobox stable or trial?"` — Checks the component classification and confirms it's trial (imported from `/trial`).

## Why it was created

Design system components have specific APIs, import conventions, and common mistakes that are hard to remember. This skill puts all component documentation at your fingertips, reducing bugs from incorrect usage and speeding up frontend development.
