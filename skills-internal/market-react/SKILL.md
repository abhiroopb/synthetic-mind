---
name: market-react
roles:
  - frontend
description: >-
  Reference docs for Market React UI components (@squareup/market-react).
  Use when building, implementing, debugging, styling, migrating, testing,
  or reviewing React components that use Market design system components
  (MarketButton, MarketRow, MarketSelect, MarketModal, MarketTable,
  MarketInput, etc.) in square-web.
---

# Market React

Market is Block's design system UI library. This skill covers the **React components** from `@squareup/market-react`.

## Package selection

| Package | Status | Use when |
|---------|--------|----------|
| `@squareup/market-react` | **React-native** (this skill) | New development, preferred |
| `@market/react` | Web component wrappers | Legacy code, migration needed |

This skill documents `@squareup/market-react`. For converting from `@market/react`, see the `migrating-market-to-react` skill.

## Component references

Load `references/component-index.md` to find the right reference file for any component. Key references:

- `references/pitfalls.md` — Common mistakes and wrong→correct patterns
- `references/market-button.md`, `market-input.md`, `market-select.md`, `market-modal.md` — Most-used components
- 39 reference docs total covering all Market React components

## Quick reference

### Import source

```tsx
// Stable components
import { MarketButton, MarketRow, MarketInput, ... } from '@squareup/market-react';

// Trial components (may have breaking API changes)
import { MarketModal, MarketTable, MarketSelect, ... } from '@squareup/market-react/trial';
```

### Stable vs trial

Stable components are exported from `@squareup/market-react`. Trial components are exported from `@squareup/market-react/trial` and may have breaking API changes.

**Stable**: MarketAccessory, MarketBanner, MarketButton, MarketCheckbox, MarketDivider, MarketField, MarketInlineStatus, MarketInput, MarketLink, MarketLinkGroup, MarketPill, MarketRadio, MarketRow, MarketSkeletonLoader, MarketSpinner, MarketTag, MarketTheme, MarketToggle

**Trial**: MarketAccordion, MarketButtonGroup, MarketCard, MarketChoiceButton, MarketCodeDisplay, MarketCodeInput, MarketCollection, MarketColorPicker, MarketCombobox, MarketDatePicker, MarketDropdown, MarketEmptyState, MarketFilter, MarketGrid, MarketHeader, MarketFooter, MarketList, MarketModal, MarketPagingTabs, MarketPopover, MarketProgressMeter, MarketQrCode, MarketScrollArea, MarketSegmentedControl, MarketSelect, MarketSlider, MarketStepper, MarketTable, MarketText, MarketToast, MarketToggletip, MarketTooltip

### Critical gotchas

See `references/pitfalls.md` for the full list of common mistakes and wrong→correct patterns.
