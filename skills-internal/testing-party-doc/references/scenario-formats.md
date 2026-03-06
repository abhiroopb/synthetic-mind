# Scenario Formats and Sign-off Tables

## Scenario Format

Each test scenario follows this structure (concrete example from the Enhanced Manual Discounts testing party):

```markdown
## Scenario 4: Manual Discount with Item Inclusions - Some Items Eligible
**Setup**: Manual discount with item inclusion rules, cart has mix of eligible and ineligible items
**Steps**:
1. Add items to cart (some in inclusion list, some not)
2. Apply the manual discount
3. Verify discount ONLY applies to eligible items
4. Verify ineligible items remain at full price
5. Verify cart UI clearly shows which items are discounted vs full price
6. Verify receipt correctly reflects per-item discount amounts

| Tester | Platform | Device | Result | Notes |
|--------|----------|--------|--------|-------|
| | iOS | iPhone | | |
| | iOS | iPad | | |
| | Android | T2 | | |
| | Android | X2 | | |
| | Android | Consumer | | |
```

**Result column**: Leave Result cells empty. After generating the doc, the author should manually add a Google Docs dropdown to each Result cell (Insert > Dropdown > New dropdown) with options: **Pass** and **Fail**. The dropdown cannot be inserted programmatically via the API. Once one dropdown is created, it can be copy-pasted to all other Result cells.

## Sign-off Table Format

Sign-off tables go at the top of the Testing Party tab. Create one per platform, with rows covering device and mode combinations relevant to the feature.

```markdown
## iOS Sign-off

| Device | Tester | Mode | Date | Status | Notes |
|--------|--------|------|------|--------|-------|
| iPhone | | SPOS | | | |
| iPhone | | SPOS | | | |
| iPad | | SPOS | | | |
| iPad | | F&B | | | |
| iPad | | RTL | | | |

## Android Sign-off

| Device | Tester | Mode | Date | Status | Notes |
|--------|--------|------|------|--------|-------|
| T2 (Terminal) | | SPOS | | | |
| T2 (Terminal) | | F&B | | | |
| T2 (Terminal) | | RTL | | | |
| X2 (Squid) | | SPOS | | | |
| X2 (Squid) | | RTL | | | |
| Consumer | | SPOS | | | |
```

## Generating Scenarios from Edge Cases

User-provided edge cases and known limitations are a rich source for specific test scenarios. Map them to scenario types:

| Input | Scenario Type | Example |
|-------|---------------|---------|
| Known bug / regression | Regression test | "Saved orders were losing discounts" -> "Save and reopen order with manual discount" |
| UI state change | Visual verification | "Disabled state at 38% alpha" -> "Verify disabled discounts in item details" |
| Known limitation | Expected behavior doc | "RST has no itemized view" -> "RST cart - verify total is correct (no per-item breakdown)" |
| Feature flag gate | Flag ON + OFF pair | Any flagged change -> "Scenario N: Flag OFF" + "Scenario N+1: Flag ON" |
| Multi-mode support | Per-mode scenario | Feature supports RTL/RST -> separate SPOS, RTL, RST scenarios |
