# MarketList and MarketCollection

```tsx
import { MarketList } from '@your-org/market-react/trial';
```

## Props

### Common props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `selectionMode` | `'single' \| 'multiple'` | — | Selection behavior (omit for non-selectable list) |
| `focusMode` | `'virtual' \| 'real'` | context-dependent | Keyboard focus management strategy |
| `showDividers` | `boolean` | `true` | Show dividers between rows (set `false` for card items) |

### Single selection props (when `selectionMode="single"`)

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `selectedValue` | `TValue \| null` | — | Controlled selected value |
| `onSelectionChange` | `(e: CustomEvent<{ prevValue: TValue \| null; value: TValue \| null }>) => void` | — | Selection change callback |

### Multiple selection props (when `selectionMode="multiple"`)

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `selectedValues` | `Set<TValue>` | — | Controlled set of selected values |
| `onSelectionChange` | `(e: CustomEvent<{ prevValues: Set<TValue>; values: Set<TValue> }>) => void` | — | Selection change callback |

Also accepts all standard HTML div attributes.

## Gotchas

| Wrong | Correct | Why |
|-------|---------|-----|
| `<MarketList>` with standalone `<MarketCheckbox>` | `<MarketRow mode="checkbox">` inside `<MarketList>` | Children should be MarketRow with appropriate `mode` |
| `selectedValue={[a, b]}` for multi-select | `selectedValues={new Set([a, b])}` | Multiple selection uses `Set<TValue>`, not arrays |
| `onChange` | `onSelectionChange` | Callback is `onSelectionChange` |
| `e.detail.value` in multi-select | `e.detail.values` (Set) | Multi-select detail uses `values`/`prevValues` (plural) |
| `e.detail.value` in single-select returns array | `e.detail.value` returns `TValue \| null` | Single-select returns a single value or null |
| Missing `value` prop on child MarketRow | Add `value="..."` to each MarketRow | Rows need `value` to participate in list selection |
| `selectionMode` without `mode` on rows | Add `mode="radio"` or `mode="checkbox"` to rows | Rows need a selection mode to render controls |
