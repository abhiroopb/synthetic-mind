# Decision Trees: Form Inputs

## Form Input Content Decision Tree

```
Writing form input content? → What type of input and content?

├── Input field labels (≤25 chars, 1-3 words)
│   Don't phrase as questions; mark optional fields: "[Label] (optional)"; don't mark required (default)
│   Brand B: "Email", "$cashtag", "Phone number"
│   Brand A: "Business name", "Tax ID", "Store address"
│   Brand C: "Purchase amount", "Billing address"
│
├── Placeholder text (~25 chars) → Simple formatting examples only
│   Don't use for instructions; don't use "Required"
│   Examples: "you@example.com", "123-456-7890", "(555) 123-4567"
│
├── Helper text (~100 chars, 2 lines max) → Supporting info that persists
│   Explain field purpose, why field is disabled, character counts if relevant
│   "We'll send updates to this email" | "This appears on your business card"
│
└── Error messages → Problem + Context + Solution
    Be specific; provide format example when helpful; focus on solutions, not blame
    "Invalid email format. Use: you@example.com"
    "Phone number must include area code. Use: (555) 123-4567"
    "Business name is required to continue"
```

### Form Content by Product Context

```
├── Brand B (financial, personal)
│   Labels: "Email", "Phone", "$cashtag", "Routing number"
│   Helper: "We'll never share your information"
│   Errors: "Check your bank account details"
│
├── Brand A (business, professional)
│   Labels: "Business name", "Tax ID", "Employee email"
│   Helper: "This appears on customer receipts"
│   Errors: "Business license number is required"
│
├── Brand C (shopping, payment plans)
│   Labels: "Purchase amount", "Payment schedule"
│   Helper: "Your first payment is due today"
│   Errors: "Minimum purchase amount is $35"
│
└── Other products → Adapt patterns to product context and terminology
```
