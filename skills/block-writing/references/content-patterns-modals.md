# Content Patterns: Modals

## Confirmation modals
Template: Title (25-40 chars) + Body (~100 chars) + Buttons (~20 chars each)

```
Destructive:
Title: "Delete account?"
Body: "This can't be undone. All your data will be permanently removed."
Buttons: "Delete" / "Cancel"

Exit confirmation:
Title: "Exit without saving?"
Body: "Your changes will be lost if you leave now."
Buttons: "Exit" / "Continue editing"
```

**Product patterns**:
```
Cash App: "Delete payment method?" / "You won't be able to use this card." / "Delete" / "Keep"
Square: "Remove employee access?" / "They'll no longer be able to process payments." / "Remove" / "Cancel"
Afterpay: "Cancel payment plan?" / "You'll need to pay the remaining balance in full." / "Cancel plan" / "Keep plan"

❌ "Are you sure?", "Yes" / "No" buttons, "This action cannot be undone" (vague)
```

## Error modals
Template: Title (25-40 chars) + Body (~100 chars) + Button (recovery action)

```
Connection: "Connection lost" / "Check your internet connection and try again." / "Try again"
Payment: "Payment failed" / "Your card was declined. Try a different payment method." / "Choose different card"
```

**Product patterns**:
```
Cash App: "Payment couldn't send" / "Check your balance and connection, then try again." / "Try again"
Square: "Card reader disconnected" / "Check the connection and try processing the payment again." / "Retry payment"
Afterpay: "Payment method declined" / "Update your payment information to continue with your plan." / "Update payment method"

❌ "HTTP 500 error occurred", "Please try again later"
```

## Information modals
Template: Title (25-40 chars) + Body (~100 chars) + Button (acknowledgment or action)

```
Status: "Maintenance scheduled" / "Cash App will be unavailable tonight from 2-4 AM for updates." / "Got it"
Feature: "New feature available" / "You can now split payments with friends." / "Try it now"
```

**Product patterns**:
```
Cash App: "Account verified" / "You can now send up to $7,500 per week and access all features." / "Start using Cash App"
Square: "New tax features" / "Automatic tax calculation is now available in your Square dashboard." / "Set up taxes"

❌ "Exciting new features await!", unnecessary modals for inline info, too many button choices
```
