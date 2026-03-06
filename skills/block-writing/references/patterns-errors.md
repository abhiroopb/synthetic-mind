# Error Message Patterns

## Structure
**Problem → Context → Solution**

## Common Patterns

**Network/connectivity errors**:
```
"We couldn't connect to the server. Check your internet connection and try again."
```

**Invalid input - form fields**:
```
"We need a valid email address. Check for typos and try again."
"Phone number must be 10 digits. Try again."
"Password must be at least 8 characters."
```

**Payment failures**:
```
"We couldn't process your payment. Your card was declined. Try another card or add money to your Brand B balance."

"Payment failed. Your card may have expired. Update your payment info or try a different card."
```

**Authentication errors**:
```
"We couldn't sign you in. Check your email and password and try again."

"Too many attempts. Wait 5 minutes and try again."
```

**Verification failures**:
```
"We couldn't verify your identity with the information you provided. We need a clear photo of your ID."

"This code expired. Request a new one."
```

**Permissions/access errors**:
```
"You don't have permission to view this page. Contact your admin for access."

"This feature isn't available for your account yet. We'll let you know when it is."
```

## What Not to Do
- ❌ "Error 404" (not meaningful)
- ❌ "Invalid input" (not specific)
- ❌ "Something went wrong" (not helpful)
- ❌ "You entered the wrong password" (blaming)
- ❌ "Failed to authenticate user" (technical jargon)
