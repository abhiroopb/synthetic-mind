# MarketTooltip and MarketToggletip

## Import

```tsx
import { MarketTooltip, MarketToggletip } from '@squareup/market-react/trial';
```

## Props

### MarketTooltip

Styled MarketPopover with enforced hover/focus interaction. Inherits MarketPopover props except `interaction` (always hover + focus) and `role` (always tooltip).

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `boolean` | — | Controlled open state |
| `defaultOpen` | `boolean` | `false` | Uncontrolled initial open state |
| `placement` | Floating UI placement | `'top'` | Position relative to trigger |
| `offset` | `number` | `8` | Pixel distance from trigger |
| `disabled` | `boolean` | `false` | Prevents showing |
| `onOpenChange` | `(open: boolean, event: Event, reason: string) => void` | — | Fires when open state changes |

#### MarketTooltip.Trigger / MarketTooltip.Content

Same API as `MarketPopover.Trigger` / `MarketPopover.Content`.

### MarketToggletip

Styled MarketPopover with enforced click interaction. Designed for richer contextual help that requires interaction.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `boolean` | — | Controlled open state |
| `defaultOpen` | `boolean` | `false` | Uncontrolled initial open state |
| `placement` | Floating UI placement | `'bottom'` | Position relative to trigger |
| `actions` | `ReactNode` | — | Action links (MarketLink components) shown in the toggletip |
| `disabled` | `boolean` | `false` | Prevents showing |
| `onOpenChange` | `(open: boolean, event: Event, reason: string) => void` | — | Fires when open state changes |

#### MarketToggletip.Trigger

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `string` \| `MarketPill` \| — (empty) | — | Trigger content. No children renders an info icon automatically. |
| `ariaLabel` | `string` | — | Accessible label for icon-only trigger (no children) |

#### MarketToggletip.Content

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | — | Toggletip body content |

## Gotchas

- **MarketTooltip is hover/focus only**: You cannot make it click-triggered. Use MarketToggletip for click-to-open contextual help.
- **MarketToggletip is click only**: You cannot make it hover-triggered. Use MarketTooltip for hover help.
- **Empty trigger = info icon**: A `<MarketToggletip.Trigger />` with no children automatically renders an info (ⓘ) icon. Provide `ariaLabel` for accessibility.
- **Trigger children types**: MarketToggletip.Trigger accepts only a string or MarketPill as children — not arbitrary ReactNode.
- **`actions` prop goes on MarketToggletip**: Not on the content. Use MarketLink components for actions.
- **Don't use MarketPopover directly**: For tooltip and toggletip patterns, always prefer these specialized wrappers over configuring MarketPopover manually.
