# Content Patterns: Error Messages

## Field validation error patterns
Template: `[Specific problem]` + `[Format example/requirement]`

```
✅ "Invalid email format. Use: you@example.com"
✅ "Password must be at least 8 characters"
✅ "Phone number is required"
✅ "Amount must be between $1 and $2,500"
❌ "Invalid input", "Validation error in field", "You entered an incorrect format"

Brand B: "Invalid $cashtag format. Use letters, numbers, and underscores"
Brand B: "Amount exceeds your available balance of $150"
Brand A: "Business name must be at least 2 characters"
Brand A: "Email address is already registered"
Brand C: "Minimum purchase amount is $35" | "Billing address must match payment method"
```

## System and connection error patterns
Template: `[What happened]` + `[Likely cause]` + `[What to try]`

```
✅ "Connection lost. Check your internet and try again."
✅ "Service temporarily unavailable. Try again in a few minutes."
✅ "Payment couldn't process. Try a different card."
❌ "Error 500: Internal server error", "Try again later" (vague timing)

Brand B: "Payment failed. Check your connection and try again."
Brand B: "Photo upload failed. Try a smaller file size."
Brand A: "Card reader not responding. Check connection and try again."
Brand A: "Receipt couldn't send. Check customer email and retry."
Brand C: "Account verification failed. Try uploading a clearer photo."
```

## Blocking error modals
Template: Title (25-40 chars) + Body (~100 chars) + Button (specific action)

```
Account: "Account temporarily locked" / "For security, we've locked your account. Contact support to unlock." / "Contact support"
Feature: "Feature not available" / "Update Brand B to access this feature." / "Update app"
```

**Product patterns**:
```
Brand B: "Verification needed" / "Upload a photo ID to continue using all Brand B features." / "Upload ID"
Brand A: "Payment processing unavailable" / "Complete business verification to start processing payments." / "Complete verification"
Brand C: "Purchase limit reached" / "You've reached your spending limit. Make a payment to continue shopping." / "Make payment"

❌ "CRITICAL ERROR", "Contact administrator", "You have exceeded limits"
```
