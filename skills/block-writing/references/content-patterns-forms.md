# Content Patterns: Forms

## Input Field Labels
Template: `[Clear descriptor]` + `(optional)` if needed — ~25 chars, 1-3 words

```
✅ "Email", "Phone number", "Full name", "Business name", "$cashtag"
✅ Optional: "Phone (optional)", "Middle name (optional)"
❌ "What's your email?", "Enter your name", "Your email address"

Brand B: "Email address", "Phone number", "$cashtag", "Date of birth", "SSN (last 4 digits)"
Brand A: "Business name", "Tax ID number", "Employee email", "Store phone"
Brand C: "Purchase amount", "Billing address", "Phone number"
```

## Placeholder Text
Template: `[Simple example format]` — ~25 chars — non-critical formatting guidance only

```
✅ "you@example.com", "(555) 123-4567", "yourstore.com", "$0.00", "MM/DD/YYYY"
❌ "Enter your email address", "Required field", "firstname.lastname@company.com"

Brand B: "you@example.com", "$cashtag", "(555) 123-4567"
Brand A: "yourstore.com", "store@business.com", "123 Main St"
```

## Helper Text
Template: `[Purpose/Context]` + `[Why needed]` (optional) — ~100 chars, 2 lines max

```
✅ "We'll send updates to this email"
✅ "This appears on customer receipts"
✅ "Used for tax reporting purposes"
✅ "Must be at least 8 characters"
❌ "Enter your email in this field" (obvious), too long (>100 chars)

Brand B: "We'll send payment confirmations here" | "This is how friends can find and pay you"
Brand A: "Appears on customer receipts and invoices" | "Required for tax reporting"
Brand C: "Your first payment is due today" | "We'll send payment reminders here"
```

## Form Error Messages
Template: `[Problem]` + `[Context/Solution]`

```
✅ "Invalid email format. Use: you@example.com"
✅ "[Field] is required to continue"
✅ "Password must be at least 8 characters"
✅ "Amount must be greater than $0"
❌ "You entered an invalid email" (blame), "Error in this field" (vague)

Brand B: "Invalid $cashtag. Use letters, numbers, and underscores only"
Brand A: "Business name is required for verification" | "Invalid tax ID format. Use: XX-XXXXXXX"
Brand C: "Minimum purchase amount is $35" | "Billing address must match your payment method"
```
