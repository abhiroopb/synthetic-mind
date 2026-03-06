# MarketField

Load when building a validated input with error messages, helper text, or character limits in market-react.

## Import

```tsx
import { MarketField } from '@your-org/market-react';
import type { MarketFieldProps } from '@your-org/market-react';
```

## Props

MarketField extends all MarketInput props and adds:

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `charLimit` | `number` | — | Shows a character counter (e.g., "5/100"). Auto-invalidates when exceeded |
| `errorMessage` | `string` | — | Error message displayed below input. Auto-sets `invalid` state |
| `helperText` | `string` | — | Helper text displayed below input |

Plus **all MarketInput props** — see [MarketInput](./market-input.md) for the full list:

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `type` | `'text' \| 'number' \| 'email' \| 'password' \| 'tel' \| 'url' \| 'multiline' \| 'search'` | `'text'` | Input type |
| `label` | `string` | — | Floating label |
| `size` | `'small' \| 'medium'` | `'medium'` | Input size |
| `invalid` | `boolean` | auto | Overrides auto-invalid from `errorMessage` or `charLimit` if explicitly set |
| `disabled` | `boolean` | `false` | Disables the input |
| `readOnly` | `boolean` | — | Read-only input |
| `value` | `string` | — | Controlled value |
| `defaultValue` | `string` | — | Initial value for uncontrolled |
| `leadingAccessory` | `ReactNode` | — | Content at input start |
| `trailingAccessory` | `ReactNode` | — | Content at input end |
| `onChange` | `ChangeEventHandler<HTMLInputElement \| HTMLTextAreaElement>` | — | Change handler |

## Gotchas

1. `MarketField` is NOT a wrapper around a slot-based error pattern — it extends `MarketInputProps` directly and renders a `MarketInput` internally.
2. `invalid` is auto-computed: `true` when `errorMessage` is set or `charLimit` is exceeded. You can override by explicitly passing `invalid={false}` or `invalid={true}`.
3. `charLimit` works with both controlled (`value`) and uncontrolled (`defaultValue`) inputs. It tracks length internally for uncontrolled mode.
4. Messages render using `MarketInlineStatus` — they are semantic status elements, not plain text.
5. The ref type is `MarketInputElement` (`HTMLInputElement | HTMLTextAreaElement`), same as `MarketInput`.
6. All MarketInput props pass through — `type`, `label`, `size`, `leadingAccessory`, `trailingAccessory`, search-specific props, etc. all work.
7. `errorMessage` takes visual precedence (shown first), but all messages are always visible when set. They don't replace each other.
8. `onChange` fires before character count updates in uncontrolled mode. If you call `preventDefault()`, the internal length tracker won't update.
