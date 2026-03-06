# MarketFilter

```tsx
import { MarketFilter, MarketFilterButton } from '@your-org/market-react/trial';
```

## MarketFilter Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `string` | **(required)** | Filter label text |
| `selectionMode` | `'single' \| 'multiple'` | `'single'` | Selection mode |
| `size` | `'medium' \| 'small'` | `'medium'` | Filter size |
| `disabled` | `boolean` | `false` | Disable the filter |
| `open` | `boolean` | — | Controlled open state |
| `selectionLabel` | `string` | — | Label showing current selection |
| `name` | `string` | — | Form field name |
| `onOpenChange` | `(e: CustomEvent) => void` | — | Called when open state changes |

### Single selection props

| Prop | Type | Description |
|------|------|-------------|
| `selectedValue` | `string` | Controlled selected value |
| `defaultSelectedValue` | `string` | Uncontrolled default value |
| `onSelectionChange` | `(e: CustomEvent<{ prevValue: string; value: string }>) => void` | Selection change handler |

### Multiple selection props

| Prop | Type | Description |
|------|------|-------------|
| `selectedValues` | `Set<string>` | Controlled selected values |
| `defaultSelectedValues` | `Set<string>` | Uncontrolled default values |
| `onSelectionChange` | `(e: CustomEvent<{ prevValues: Set<string>; values: Set<string> }>) => void` | Selection change handler |

## MarketFilter.Option Props

Extends MarketRow props with:

| Prop | Type | Description |
|------|------|-------------|
| `value` | `string` | Option value |
| `mode` | `string` | Override row mode |
| `controlPosition` | `string` | Position of the control element |

## MarketFilterButton Props (standalone)

| Prop | Type | Description |
|------|------|-------------|
| `label` | `string` | Button label |
| `selectionLabel` | `string` | Label showing current selection |
| `size` | `'medium' \| 'small'` | Button size |
| `disabled` | `boolean` | Disable the button |
| `onClick` | `MouseEventHandler` | Click handler |

## Gotchas

- **CustomEvent-based callbacks** — `onSelectionChange` receives a CustomEvent. Use `e.detail.value` (single) or `e.detail.values` (multiple).
- **Single vs multiple have different prop names**: `selectedValue` / `selectedValues`, `defaultSelectedValue` / `defaultSelectedValues`.
- **Multiple selection uses `Set<string>`**, not arrays.
- **`label` is required** — the filter will not render correctly without it.
- **MarketFilterButton** is a standalone button component for custom trigger UIs — it does NOT include dropdown behavior.
- **Trial export** — import from `@your-org/market-react/trial`.
