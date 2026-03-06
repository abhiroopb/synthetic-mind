# MarketAccordion

## Import

```tsx
import { MarketAccordion, MarketAccordionGroup } from '@squareup/market-react/trial';
```

## Props

### MarketAccordion

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `header` | `ReactNode` | — | Trigger content shown when collapsed |
| `children` | `ReactNode` | — | Panel content revealed on expand |
| `size` | `'large'` \| `'medium'` \| `'small'` | `'medium'` | Controls header text size and spacing |
| `expanded` | `boolean` | — | Controlled expanded state |
| `defaultExpanded` | `boolean` | `false` | Uncontrolled initial expanded state |
| `disabled` | `boolean` | `false` | Disables expand/collapse interaction |
| `id` | `string` | — | Identifier used by MarketAccordionGroup |
| `onExpandedChange` | `(id: string, expanded: boolean) => void` | — | Fires when expanded state changes |

### MarketAccordionGroup

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | — | MarketAccordion items |
| `expandedItems` | `string[]` | — | Controlled list of expanded accordion IDs |
| `defaultExpandedItems` | `string[]` | `[]` | Uncontrolled initial expanded IDs |
| `onExpandedItemsChange` | `(expandedItems: string[]) => void` | — | Fires when expanded items change |

## Gotchas

- **`id` is required for group coordination**: Every MarketAccordion inside a MarketAccordionGroup must have a unique `id`, or expansion tracking won't work.
- **Don't mix controlled and uncontrolled**: Use either `expanded` + `onExpandedChange` or `defaultExpanded` on a single accordion, not both.
- **Group does not enforce single-expand**: MarketAccordionGroup allows multiple items open simultaneously by default. To get "only one open at a time" behavior, manage `expandedItems` yourself.
- **`onExpandedChange` signature**: Receives `(id, expanded)` — not an event object.
