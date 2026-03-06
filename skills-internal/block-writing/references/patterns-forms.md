# Form Field Patterns

## Labels
Clear, sentence case, no periods.

**Examples**:
- "Email address"
- "Phone number"
- "Full name"
- "Card number"
- "Billing address"

## Helper Text
Explain requirements or format before the user acts.

**Examples**:
- "We'll send a 6-digit code to this number"
- "Must be at least 8 characters"
- "This appears on your statements"
- "We'll never share this with anyone"

## Placeholder Text (Optional)
Show format examples only. Don't use as a substitute for labels.

**Examples**:
- "name@example.com"
- "(555) 123-4567"
- "1234 5678 9012 3456"

## Validation Messages

**Success states**:
```
"Email verified"
"Phone number added"
```

**Error states** (use Problem → Context → Solution):
```
"We need a valid email address. Check for typos and try again."
"Phone number must be 10 digits. Try again."
```
