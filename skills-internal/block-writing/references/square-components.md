# Square Component Content Guidelines

## Buttons
- **Structure**: Verb or Verb+noun phrasing; sentence case; no end punctuation
- **Character limits**: ~20 chars standard; ~15 chars compact contexts
- **Flow terms**: "Next" (multi-step), "Done" (final action in series with saved steps), "Cancel" (ends without changes), "Not now" (delay), "Skip" (avoid)
- **Creation vs addition**: "Create" (from scratch), "Add" (existing items); "Delete" (removed permanently), "Remove" (still exists elsewhere)
- ✅ "Create invoice", "Add customer", "Process payment", "Save report"
- ❌ "Submit", "OK", "Click here"

**Product examples**:
- Square POS: "Process payment", "Add item", "Close register", "Print receipt"
- Square Dashboard: "Generate report", "Export data", "Update settings"
- Square Online: "Publish site", "Add product", "Manage orders"

## Form Inputs

**Labels** (~25 chars, 1-3 words): Clear, business-focused descriptors; include format requirements at end; mark optional with "(optional)"
- Examples: "Business name", "Tax ID", "Store address", "Employee email"

**Placeholders** (~25 chars): Provide examples, not instructions
- Examples: "Acme Coffee Shop", "123-45-6789", "you@business.com"

**Helper text** (~100 chars, 2 lines max): Explain field purpose and business implications; reassure about data handling when appropriate
- Examples: "This appears on customer receipts", "Required for tax reporting"

**Errors**: Problem + Solution; helpful and business-focused
- "Business name is required for verification", "Invalid tax ID format. Use: XX-XXXXXXX"

## Selection Controls

**Checkboxes**: Describe what happens when selected; use first person for legal agreements ("I agree to..."); parallel phrasing in groups
- Examples: "Email receipts to customers", "Automatic tax calculation", "Inventory tracking alerts"

**Radio buttons**: Clear, scannable options; parallel structure; logical business order (most common first)
- Examples: "Retail store", "Restaurant", "Service business", "Online only"

**Toggles**: Describe what's enabled when "on"; avoid "enable/disable" — use "activate", "allow", "show"
- Examples: "Automatic receipts", "Inventory tracking", "Employee notifications"

## Dialogs
- **Title** (25-40 chars): Brief, business-focused statement
- **Body** (~100 chars): Business context and consequences
- **Buttons** (~20 chars): Specific business actions

Confirmation pattern:
- Title: "Close register?" → Body: "Unsaved transactions will be lost." → Buttons: "Close" / "Continue"

Destructive pattern:
- Title: "Delete customer data?" → Body: "This will remove all transaction history and cannot be undone." → Buttons: "Delete" / "Keep data"

## Toasts
- Brief business confirmations that auto-dismiss; past tense; 75 chars max; end with period; no exclamation marks
- ✅ "Sale processed.", "Report generated.", "Customer added.", "Inventory updated."
- ❌ "Success!", "Transaction completed successfully."

## Banners
- 1-2 short sentences with periods; focus on business implications; clear next steps
- Types: Info (announcements), Success (milestones), Warning (issues requiring attention), Critical (urgent action)
