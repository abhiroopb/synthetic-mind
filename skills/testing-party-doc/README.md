# Testing party doc generator

> Generate a structured, multi-tab Google Doc for feature testing parties from PRDs, eng docs, and PRs.

## What it does

Creates a comprehensive testing party document with four tabs — Overview, Testing Party, Environment Setup, and Bugs — by reading source documents (PRDs, eng docs, pull requests, Slack threads). It generates test scenarios organized by feature flag state, cross-mode behavior, persistence, UI, and network conditions. The output is written directly into a Google Doc ready for team collaboration.

## Usage

Provide a destination Google Doc URL and a PRD link. Optionally include eng docs, PR links, and Slack channels for richer context.

- "Create a testing party doc for [feature]"
- "Build a QA doc from this PRD: [url]"
- "Generate a test sign-off document"

## Examples

- `"Create a testing party doc — destination: [gdoc url], PRD: [prd url], eng doc: [eng url]"`
- `"Build a testing party doc for offline payments using PRD [url] and PRs #123, #456"`
- `"Generate a QA plan from this PRD: [url] — platform is iOS only"`

## Why it was created

Setting up testing party documents is time-consuming — you need to read multiple sources, create structured test scenarios, set up matrices for devices and modes, and format everything into a collaborative doc. This skill automates the entire process, generating dozens of test scenarios in minutes instead of hours.
