# Test plan creator

> Create test plans and acceptance criteria for product features by analyzing the feature spec and generating structured test scenarios.

## What it does

Reads a feature's spec document and generates a comprehensive test plan with prioritized scenarios (P0/P1/P2), specific test steps, expected results, and acceptance criteria. It identifies happy paths, edge cases, compliance requirements, integration points, and UI touchpoints. It asks clarifying questions about target platforms and risk areas before drafting.

## Usage

Point it at a feature spec and it generates either a full test plan or lightweight acceptance criteria.

- "Create a test plan for [feature]"
- "Generate acceptance criteria for [feature]"
- "Write test scenarios for [feature area]"

## Examples

- `"Create a test plan for the cash rounding feature"`
- `"Generate acceptance criteria for offline payments — focus on compliance and payment flows"`
- `"Write test scenarios for the new tipping flow on iOS and Android"`

## Why it was created

Writing thorough test plans is tedious but critical — vague criteria like "works correctly" miss edge cases, and skipping compliance scenarios creates launch risk. This skill produces structured, unambiguous test scenarios directly from the spec so nothing gets missed.
