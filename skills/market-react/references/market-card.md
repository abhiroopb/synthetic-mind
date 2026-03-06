# MarketCard

## Import

```tsx
import { MarketCard } from '@squareup/market-react/trial';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `ReactNode` | — | Card title; acts as accessible name for interactive cards |
| `children` | `ReactNode` | — | Custom card content |
| `mode` | `'transient'` \| `'checkbox'` \| `'radio'` \| `'toggle'` \| `'selectable'` \| `'toggleable'` | — | Card interaction mode. Omit for readonly. |
| `appearance` | `'default'` \| `'emphasis'` | `'default'` | Visual appearance (readonly mode only) |
| `selected` | `boolean` | — | Controlled selected state (selectable modes) |
| `defaultSelected` | `boolean` | — | Uncontrolled initial selected state |
| `value` | `string` | — | Value emitted in selection events |
| `disabled` | `boolean` | `false` | Disables interaction |
| `controlPosition` | `'leading'` \| `'trailing'` | `'trailing'` | Position of the selection control |
| `href` | `string` | — | Renders as a link card |
| `secondaryText` | `ReactNode` | — | Secondary text below the title |
| `leadingAccessory` | `ReactNode` | — | Content before the title (icon, image) |
| `trailingAccessory` | `ReactNode` | — | Content after the title |
| `aria-label` | `string` | — | Accessible name (required if no `title`) |
| `aria-labelledby` | `string` | — | Accessible name reference (required if no `title`) |
| `onSelectedChange` | `(e: CustomEvent<{ selected: boolean; value: string }>) => void` | — | Fires when selection changes |

## Gotchas

- **Interactive cards need accessible names**: Cards with `mode` or `href` must have one of `title`, `aria-label`, or `aria-labelledby`.
- **`appearance` is readonly-only**: Setting `appearance="emphasis"` on a selectable card has no effect.
- **Selection event shape**: The event detail is `{ selected, value }`, not a standard React `onChange` — destructure from `e.detail`.
- **Inherits MarketRow props**: `leadingAccessory`, `trailingAccessory`, `secondaryText`, etc. all work the same as on MarketRow.
- **Don't nest interactive elements**: Avoid placing buttons or links inside a selectable/link card.
