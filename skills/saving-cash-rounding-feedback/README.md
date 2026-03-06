# Saving Cash Rounding Feedback

> Save customer feedback to a tracking table in Google Docs with automatic account lookup.

## What it does

This skill appends customer feedback to a tracking table in a Google Doc. It accepts feedback from two sources — email or Slack messages — looks up the customer's account token from the internal account lookup tool, and inserts a new row with the verbatim feedback, account token, and source information. The feedback text is always preserved word-for-word without summarization.

## Usage

Invoke when you need to log customer feedback about a feature. Provide either the feedback text and customer email, or a Slack message link containing the feedback.

**Trigger phrases:**
- "Save this feedback"
- "Log this customer feedback"
- "Record this seller's feedback"

## Examples

- `"Save this cash rounding feedback from seller@example.com: 'I love the new rounding feature'"`
- `"Log the feedback from this Slack thread: [slack link]"`
- `"Record this seller's feedback about penny elimination"`

## Why it was created

Customer feedback arrives through multiple channels (email, Slack) and needs to be centralized in a single tracking document for product analysis. This skill automates the lookup-and-log workflow so feedback doesn't get lost.
