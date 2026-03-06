# Button Patterns

## Primary Actions
Use active imperative verbs. Be specific about the action.

**Pattern**: `[Verb] + [object]`

**Examples**:
- "Save changes"
- "Send money"
- "Delete account"
- "Create invoice"
- "Download statement"
- "Add bank account"

**Avoid**:
- "Submit" (too generic)
- "OK" (not descriptive)
- "Continue" (unless truly continuing a multi-step flow)

## Secondary Actions
Often paired with primary actions.

**Examples**:
- "Cancel"
- "Go back"
- "Skip for now"
- "Not now"
- "Remind me later"

## Destructive Actions
Be explicit about what will be deleted or removed.

**Pattern**: `Delete [specific item]` or `Remove [specific item]`

**Examples**:
- "Delete account" (not just "Delete")
- "Remove card" (not just "Remove")
- "Cancel payment" (not just "Cancel")

## Confirmation Dialogs

**Destructive action confirmation**:
- Title: "Delete [item]?"
- Body: Brief explanation of consequences
- Primary button: "Delete [item]" (matches title)
- Secondary button: "Cancel" or "Keep [item]"

**Example**:
```
Title: "Delete payment method?"
Body: "We'll remove this card from your account. You can add it again later."
Primary: "Delete card"
Secondary: "Cancel"
```
