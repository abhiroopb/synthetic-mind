# Decision Trees: Buttons and Toasts

## Button Content Decision Tree

```
Writing button content? → What's the context and action?

├── Continuing a flow → "Continue" (not "Next")
│   Cash App: "Continue to payment" | Square: "Continue setup" | Afterpay: "Continue to checkout"
│
├── Error recovery → "Try again" (not "Retry") — consistent across all products
│
├── One-time activation → "Activate", "Turn on" (not "Enable")
│   Cash App: "Activate card" | Square: "Turn on notifications" | Bitkey: "Activate wallet"
│
├── Dismissing a prompt → "Not now" (not "Maybe later") — consistent across Block
│
├── Destructive action → Specific action + object
│   Cash App: "Delete payment method" | Square: "Remove employee"
│
├── Saving or confirming → "Save [specific item]" or "Save changes"
│   Cash App: "Save settings" | Square: "Save business info" | Afterpay: "Save preferences"
│
└── Primary product actions
    Cash App: "Send money", "Add money", "Withdraw"
    Square: "Process payment", "View reports"
    Afterpay: "Split payment", "View plan"
    Tidal: "Play music", "Add to playlist"
    Bitkey: "Send bitcoin", "Receive bitcoin"
```

## Button Character Limits

```
├── Compact button (inside containers) → ~15 chars
│   "Edit", "Save", "Delete"
│
├── Default button (standalone in screen) → ~20 chars
│   "Add payment method", "View details"
│
└── CTA button (bottom of screen/flow) → ~20 chars
    "Complete order", "Finish setup"
```

## Toast Content Decision Tree

```
Writing toast content? → What action was completed?

├── Simple action confirmation → Past tense verb phrase, no punctuation, ≤75 chars
│   Cash App: "Payment sent", "Card activated"
│   Square: "Sale processed", "Settings saved"
│   Afterpay: "Payment scheduled", "Plan updated"
│
├── Action with additional context → Header (50 chars) + Body (75 chars), no punctuation
│   "Payment sent" / "John will receive it soon"
│   "Card added" / "Ready to use for payments"
│   "Report ready" / "Check your email for the link"
│
├── Status change → "[Object] [new state]"
│   "Notifications enabled", "Account verified", "Two-factor authentication on"
│
└── Error recovery confirmation → Brief, positive, forward-looking
    "Connection restored", "Upload completed", "Issue resolved"
```
