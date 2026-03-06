# Tab Content Examples

Load when populating any tab. Concrete examples from the Enhanced Manual Discounts testing party showing the key sections for each tab.

## Overview Tab

Sections in order: title, metadata block, overview narrative, What's New table, feature decision flow, device matrix, permutation matrix, mode-specific behavior, network states, special conditions.

Example metadata block:

```markdown
# Enhanced Manual Discounts Testing Party
**Author** – Saurabh Singh
**PRD** – [Orders] Advanced Manual Discount Rules PRD
**Eng Doc** – Manual Discount Rules
**Designs** - [Figma](https://figma.com/design/abc123/manual-discounts)
**Linear Project** – RTLMOB-458
**Feature Flags** - `EnableManualDiscountPricingRules`
**iOS**: Jane Smith | **Android**: Saurabh Singh | **PM**: Alex Johnson
```

Example device matrix:

| Platform | Device | Form Factor | Supported Modes |
|----------|--------|-------------|-----------------|
| iOS | iPhone | Compact | SPOS |
| iOS | iPad | Regular | SPOS, F&B, RTL |
| Android | T2 (Terminal) | Compact | SPOS, F&B, RTL |
| Android | X2 (Squid) | Compact | SPOS, RTL |
| Android | Consumer | Varies | SPOS |

Example permutation matrix:

| Discount Type | Pricing Rules | Cart Contents | Expected Behavior |
|---------------|---------------|---------------|-------------------|
| Percentage | None | Any items | Discount applies to all items |
| Percentage | Item inclusions | Mix eligible/ineligible | Only eligible items discounted |
| Fixed amount | Item exclusions | Mix eligible/ineligible | Excluded items at full price |

## Testing Party Tab

Sign-off tables first, then scenarios in Parts 1-7. See [scenario-formats.md](scenario-formats.md) for scenario structure and sign-off table format.

## Bugs Tab

Simple table for testers to log bugs. Columns: Bug, Platform, Device, Mode, Severity, Reporter, Linear Ticket. Pre-populate with ~10 empty rows. The "Linear Ticket" column starts empty and gets populated if tickets are created later.

## Environment Setup Tab

Sections: prerequisites, account (go/rsttesting, go/merchantfactory), test data checklist, iOS setup (Simba + go/mr + flag toggle via Internal Settings), Android setup (Emulator Runner + go/mr + flag toggle + mode switching), Dashboard setup.

Example test data checklist:

1. At least 5 catalog items across different categories
2. A manual percentage discount with item inclusion rules
3. A manual fixed-amount discount with item exclusion rules
4. A manual discount with no pricing rules (for comparison)
5. A saved order with a pricing-rule discount applied
