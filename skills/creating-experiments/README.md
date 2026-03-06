# Creating Experiments

> Set up A/B experiments with dual-flag patterns, traffic allocation, and analytics integration.

## What it does

Automates the creation of A/B experiments using a dual-flag pattern: a traffic allocation flag (boolean, controls who enters the experiment) and a bucketing flag (string, assigns users to control/treatment/ineligible variants). Handles LaunchDarkly flag creation, holdout prerequisites, and optional GrowthBook experiment linking for analytics. Follows a structured runbook for experiment setup.

## Usage

Use when creating, launching, or configuring A/B experiments. Also useful for debugging experiment flag configurations or ramping traffic.

Trigger phrases:
- "Create an experiment"
- "Set up an A/B test"
- "Launch a new experiment with a holdout"
- "Link this experiment to GrowthBook"

## Examples

- "Create an experiment called 'checkout-redesign' with a Q1 holdout"
- "Set up a dual-flag experiment for the new onboarding flow"
- "Create a GrowthBook experiment for the dashboard-web area"

## Why it was created

Setting up experiments requires coordinated configuration across LaunchDarkly (flags, targeting, prerequisites) and GrowthBook (analytics). This skill codifies the dual-flag pattern and runbook into a repeatable, error-free workflow.
