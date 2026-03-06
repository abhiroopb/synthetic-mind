# Decision Trees: Error Messages

## Error message decision tree

```
Writing error message? → What type of error?

├── Field validation → Specific problem + format example + action
│   "Invalid email format. Use: you@example.com"
│   "Phone number must include area code. Use: (555) 123-4567"
│   "Password must be at least 8 characters"
│
├── System or connection error → What happened + likely cause + what to try
│   "Payment failed. Check your connection and try again."
│   "Upload failed. Try a smaller file or check your internet."
│   "Service temporarily unavailable. Try again in a few minutes."
│
├── User action blocked → What's blocked + why + what they can do
│   "Transfer limit reached. Try a smaller amount or wait 24 hours."
│   "Account verification needed. Upload ID to continue."
│   "Payment method declined. Try a different card."
│
├── Missing information → What's missing + why needed + how to provide it
│   "Email required for account recovery"
│   "Business address needed for tax reporting"
│
└── Critical error requiring support → What happened + our response + how to get help
    "Account temporarily locked for security. Contact support for help."
    "Unusual activity detected. We've secured your account. Call us at..."
```

## Error tone by severity

```
├── Minor validation → Helpful, instructional, matter-of-fact
│   "Email format incorrect. Use: you@example.com"
│
├── Moderate system issue → Understanding, solution-focused, reassuring
│   "Connection lost. Check your internet and try again."
│
├── Serious/security issue → Clear, authoritative, supportive
│   "Account locked for security. Contact support to unlock."
│
└── Critical failure → Transparent, apologetic, action-oriented
    "Service unavailable due to technical issues. Our team is working to restore it."
```
