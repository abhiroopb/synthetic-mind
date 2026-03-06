# MarketPopover

## Import

```tsx
import { MarketPopover } from '@your-org/market-react/trial';
```

## Props

### MarketPopover

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `boolean` | — | Controlled open state |
| `defaultOpen` | `boolean` | `false` | Uncontrolled initial open state |
| `interaction` | `{ click?: boolean; hover?: boolean; focus?: boolean }` | `{ click: true }` | Which interactions trigger the popover |
| `placement` | Floating UI placement (e.g., `'bottom'`, `'top-start'`, `'right-end'`) | `'bottom'` | Where the popover appears relative to trigger |
| `offset` | `number` | `8` | Pixel distance from trigger |
| `viewportMargin` | `number` | `24` | Minimum pixel distance from viewport edge |
| `matchTriggerWidth` | `boolean` | `false` | Makes popover match the trigger's width |
| `role` | `'dialog'` \| `'tooltip'` \| `'menu'` \| `'listbox'` \| etc. | `'dialog'` | ARIA role for the popover content |
| `maxHeight` | `number` \| `'auto'` | — | Maximum height of the popover content |
| `layerMode` | `'portal'` \| `'native'` | `'portal'` | Rendering strategy (portal renders outside DOM tree) |
| `disabled` | `boolean` | `false` | Prevents opening |
| `onOpenChange` | `(open: boolean, event: Event, reason: string) => void` | — | Fires when open state changes |
| `onOpenStart` | `() => void` | — | Fires when open animation starts |
| `onOpenEnd` | `() => void` | — | Fires when open animation completes |
| `onCloseStart` | `() => void` | — | Fires when close animation starts |
| `onCloseEnd` | `() => void` | — | Fires when close animation completes |

### MarketPopover.Trigger

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | — | The element that triggers the popover |

### MarketPopover.Content

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | — | Popover body content |
| `initialFocus` | `number` \| `React.RefObject` | `0` | Element to focus when popover opens (index or ref) |

## Gotchas

- **Compound component pattern**: Must use `MarketPopover.Trigger` and `MarketPopover.Content` — not standalone imports.
- **`interaction` is an object, not a string**: Pass `{ hover: true }` or `{ click: true, focus: true }`, not `"hover"`.
- **`role` affects accessibility behavior**: Use `'tooltip'` for hover-only info, `'menu'` for action lists, `'dialog'` for interactive content.
- **Portal rendering by default**: Content renders in a portal. Use `layerMode="native"` if you need it in the DOM tree (e.g., for CSS containment).
- **`onOpenChange` signature**: Receives `(open, event, reason)` — the reason string tells you why it opened/closed (e.g., `'click'`, `'escape'`, `'outside-click'`).
- **Prefer MarketDropdown or MarketTooltip**: If you want a click-only dropdown or hover-only tooltip, use the specialized wrappers instead of configuring MarketPopover directly.
