# Decision Trees: Buttons and Toasts

## Button Content Decision Tree

```
Writing button content? → What's the context and action?

├── Continuing a flow → "Continue" (not "Next")
│   Brand B: "Continue to payment" | Brand A: "Continue setup" | Brand C: "Continue to checkout"
│
├── Error recovery → "Try again" (not "Retry") — consistent across all products
│
├── One-time activation → "Activate", "Turn on" (not "Enable")
│   Brand B: "Activate card" | Brand A: "Turn on notifications" | Brand E: "Activate wallet"
│
├── Dismissing a prompt → "Not now" (not "Maybe later") — consistent across your company
│
├── Destructive action → Specific action + object
│   Brand B: "Delete payment method" | Brand A: "Remove employee"
│
├── Saving or confirming → "Save [specific item]" or "Save changes"
│   Brand B: "Save settings" | Brand A: "Save business info" | Brand C: "Save preferences"
│
└── Primary product actions
    Brand B: "Send money", "Add money", "Withdraw"
    Brand A: "Process payment", "View reports"
    Brand C: "Split payment", "View plan"
    Tidal: "Play music", "Add to playlist"
    Brand E: "Send bitcoin", "Receive bitcoin"
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
│   Brand B: "Payment sent", "Card activated"
│   Brand A: "Sale processed", "Settings saved"
│   Brand C: "Payment scheduled", "Plan updated"
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
