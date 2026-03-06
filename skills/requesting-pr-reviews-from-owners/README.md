# Requesting PR Reviews from Owners

> Parse code ownership bot comments to find pending team approvals and generate Slack review request messages.

## What it does

This skill extracts the list of required team approvals from a code ownership bot comment on a pull request. It identifies which teams have approved and which are still pending, summarizes the code changes relevant to each pending team, and generates copy-pasteable Slack messages you can send to the appropriate team channels to request reviews.

## Usage

Invoke when you want to check which teams still need to approve your PR, or when you want to generate Slack messages to request reviews from pending teams.

**Trigger phrases:**
- "Check PR review status"
- "Who still needs to approve my PR?"
- "Generate review request messages"
- "Follow up on PR reviews"

## Examples

- `"Check the review status of my current PR"`
- `"Which teams haven't approved PR #1234 yet?"`
- `"Generate Slack messages to request reviews for this PR"`

## Why it was created

Tracking which teams have approved a PR and manually writing Slack messages to request reviews is tedious, especially in large repos with many code owners. This skill automates the tracking and message generation so you can follow up on reviews quickly.
