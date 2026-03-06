# UI State Patterns

## Empty states

**Structure**: Heading (what would be here) → brief explanation (optional) → CTA

```
No items: "No payment history yet" / "Your past payments will appear here." / "Send money"
No results: "No results found" / "Try a different search term." / "Clear search"
Not set up: "Set up direct deposit" / "Get paid up to 2 days early." / "Get started"
```

## Success states

**Major success** — significant completions, multi-step flows
- Clear success indicator (checkmark, "Complete")
- Specific confirmation of what was accomplished
- Next step or action (optional)

```
✓ "Account created" / "You're ready to send and receive money." / "Add money"
```

**Routine success** — everyday actions; brief and proportional
```
Toast: "Money sent to Alex"
Inline: "Settings saved"
Small: "Card added"
```

## Loading states

Show progress when possible.
```
With progress: "Uploading... 60%" / "Processing payment... 2 of 3 steps"
Without: "Processing payment..." / "Connecting to your bank..." / "Verifying your ID..."
```

Avoid "Please wait..." (obvious) and bare "Loading..." for long operations.

## Help text

**Contextual help** — brief practical explanation in the UI
```
"We use this to verify your identity"
"This appears on your bank statements"
"Your $cashtag is how people send you money"
```

**Tooltips** — 1 sentence max
```
"This includes fees and taxes"
"Funds arrive in 1-3 business days"
"Required for verification"
```
