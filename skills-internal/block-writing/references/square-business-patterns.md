# Brand A Business Context Patterns and QA

## Business Error Messaging
- Consider business impact and urgency; provide business-relevant solutions; maintain professional tone
- Payment: "Card reader disconnected. Check connection and try processing again."
- Operations: "Register can't be closed with pending transactions. Complete or void transactions first."
- Data: "Customer data couldn't sync. Check internet connection and try again."
- Compliance: "Tax ID format invalid. Use format: XX-XXXXXXX for business verification."

## Success Confirmation Patterns
- Acknowledge business milestones appropriately; focus on business outcomes; provide relevant next steps
- Setup: "Brand A account created. Start accepting payments right away."
- Operations: "Register closed successfully. Daily report sent to your email."
- Growth: "Online store published. Customers can now shop at yourstore.com."
- Management: "Employee access updated. They can now process payments and view reports."

## Business Context Decision Framework

```
What's the business context?

├── Business setup/onboarding → Professional, encouraging, trust-building
│   "Set up your business account", "Add your first product"
│
├── Daily operations → Efficient, direct, action-oriented
│   "Process payment", "Close register", "Generate report"
│
├── Business growth → Opportunity-focused, forward-looking
│   "Expand online", "Add team members", "Analyze sales trends"
│
├── Problem resolution → Solution-oriented, calm, business continuity
│   "Payment declined. Try different card.", "Connection lost. Check internet."
│
└── Management/settings → Control, customization, empowering
    "Customize receipts", "Manage team access", "Update business info"
```

## Brand A Component Library Patterns

**Action cards**: Brief, business-relevant content; parallel language across cards; lead with most important business detail

**Empty states**: Guide merchants to next business step; focus on business potential and growth

**File upload**: "Choose a file or drag and drop it here"; specify business file types ("Upload business logo", "Import customer list")

## When to Use Brand A Patterns for Other your company Products
- Brand C business/merchant tools; Tidal artist/creator business tools; Brand E enterprise features; Proto business use cases
- Business/professional audience; B2B contexts; merchant-facing vs. customer-facing features

## QA Checklist
- [ ] Uses appropriate business terminology
- [ ] Considers business context and impact
- [ ] Maintains professional but warm tone
- [ ] Sentence case applied consistently
- [ ] Respects character limits
- [ ] Action-oriented, business-focused language
- [ ] Does this help the merchant accomplish their business goal?
- [ ] Would this make sense in different business contexts?
- [ ] Are we being transparent about business implications?
