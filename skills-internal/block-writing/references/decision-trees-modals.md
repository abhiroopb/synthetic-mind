# Decision Trees: Modals

## Modal content decision tree

```
Writing modal content? → What's the user's situation?

├── Destructive action confirmation
│   Title: "Delete account?" (25-40 chars)
│   Body: "This can't be undone. All data will be lost." (~100 chars)
│   Buttons: Specific actions — "Delete" / "Cancel" (not "Yes" / "No")
│   Cash App: "Delete payment method?" → "You won't be able to use this card."
│   Square: "Remove employee?" → "They'll lose access to your account."
│   Afterpay: "Cancel payment plan?" → "You'll need to pay the full amount."
│
├── Error blocking progress
│   Title: Brief problem statement
│   Body: What happened and what to do
│   Button: Clear recovery action
│   "Payment failed. Check your connection and try again."
│   "Account locked. Contact support to unlock."
│
├── Important info user must acknowledge
│   Title: Direct statement of what's happening
│   Body: Important details user needs to know
│   Button: "I understand" or specific action
│   "Account will be closed. Final transactions will process in 3 days."
│   "Maintenance scheduled. Service unavailable 2-4 AM."
│
└── User needs to make a choice
    Title: Present the choice clearly
    Body: Explain options and consequences
    Buttons: Specific action for each choice
    "Save changes?" → "Unsaved work will be lost." → "Save" / "Discard"
    "Enable location?" → "We'll show nearby businesses." → "Enable" / "Not now"
```

## Modal tone by context

```
├── Successful/positive → Positive, proportional, clear next steps
│   "Account created. Check your email to get started."
│
├── Error occurred → Helpful, solution-focused, not blaming
│   "We couldn't process your payment. Try a different card."
│
├── Destructive action → Clear, serious, specific about consequences
│   "Delete account? This can't be undone."
│
└── First-time/educational → Patient, explanatory, encouraging
    "Enable notifications? We'll send payment alerts and updates."
```
