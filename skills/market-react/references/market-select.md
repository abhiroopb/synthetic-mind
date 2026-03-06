# MarketSelect

Load when building any dropdown select, single-select, or multi-select in market-react.

## Import

```tsx
// MarketSelect is a TRIAL component
import { MarketSelect } from '@squareup/market-react/trial';
import type { MarketSelectProps } from '@squareup/market-react/trial';
```

## Props

### MarketSelect

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `selectionMode` | `'single' \| 'multiple'` | `'single'` | Determines single or multi-select behavior |
| `label` | `string` | — | Label for the select trigger |
| `placeholder` | `string` | — | Placeholder when no value is selected |
| `disabled` | `boolean` | — | Disables the select |
| `invalid` | `boolean` | — | Shows invalid state |
| `open` | `boolean` | — | Controlled open state. Omit for uncontrolled |
| `selectionLabel` | `string` | — | Override the displayed selection text |
| `onOpenEnd` | `() => void` | — | Called after popover fully opens and animations complete |
| `leadingAccessory` | `ReactNode` | — | Content at the start of the trigger |
| `trailingAccessory` | `ReactNode` | — | Content at the end of the trigger |
| `children` | `MarketSelect.Option` elements | — | Options to display in the dropdown |

#### Single select props

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `selectedValue` | `TValue \| null` | — | Controlled selected value. `undefined` = uncontrolled, `null` = no selection |
| `defaultSelectedValue` | `TValue` | — | Initial value for uncontrolled mode |
| `onSelectionChange` | `(event: CustomEvent<{ prevValue: TValue \| null; value: TValue \| null }>) => void` | — | Fires on selection change |

#### Multiple select props

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `selectedValues` | `Set<TValue>` | — | Controlled selected values |
| `defaultSelectedValues` | `Set<TValue>` | — | Initial values for uncontrolled mode |
| `onSelectionChange` | `(event: CustomEvent<{ prevValues: Set<TValue>; values: Set<TValue> }>) => void` | — | Fires on selection change |

### MarketSelect.Option

Options use MarketRow props. Key props:

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `value` | `TValue` | — | Unique value identifying this option |
| `title` | `ReactNode` | **required** | Primary content displayed in the option |
| `secondaryText` | `ReactNode` | — | Supporting text below the title |
| `leadingAccessory` | `ReactNode` | — | Content at the start of the option row |
| `trailingAccessory` | `ReactNode` | — | Content at the end of the option row |
| `disabled` | `boolean` | — | Disables the option |
| `mode` | `MarketRowSelectableMode` | auto | Auto-set: `'selectable'` for single, `'checkbox'` for multiple |
| `controlPosition` | `'leading' \| 'trailing'` | `'leading'` | Position of the selection control |
| `selected` | `boolean` | — | Controlled selection state |
| `defaultSelected` | `boolean` | — | Uncontrolled initial selection |

## Gotchas

1. `MarketSelect` is a **trial** component — import from `@squareup/market-react/trial`, not the main export.
2. `onSelectionChange` receives a `CustomEvent`, not a plain React event. Access values via `e.detail.value` (single) or `e.detail.values` (multiple).
3. For single select, `selectedValue: undefined` means uncontrolled, `selectedValue: null` means controlled with no selection. These are different.
4. For multiple select, `selectedValues` is a `Set<TValue>`, not an array.
5. `MarketSelect.Option` mode is auto-determined: `'selectable'` for single select, `'checkbox'` for multiple. You can override with the `mode` prop but typically shouldn't.
6. Single select auto-closes the popover after selection. Multiple select stays open.
7. The `title` prop on `MarketSelect.Option` is **required** — it comes from MarketRow's base props.
8. This is NOT the old `onValueChange` with a direct string callback — it's `onSelectionChange` with a `CustomEvent`.
