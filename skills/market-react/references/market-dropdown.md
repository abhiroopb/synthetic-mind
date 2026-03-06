# MarketDropdown

## Import

```tsx
import { MarketDropdown } from '@squareup/market-react/trial';
```

## Props

MarketDropdown is a styled MarketPopover with enforced click-only interaction. It inherits all MarketPopover props **except**: `interaction`, `offset`, `viewportMargin`, `role`, `container`, `disableFocusManager`.

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `open` | `boolean` | — | Controlled open state |
| `defaultOpen` | `boolean` | `false` | Uncontrolled initial open state |
| `placement` | Floating UI placement | `'bottom'` | Position relative to trigger |
| `matchTriggerWidth` | `boolean` | `false` | Makes dropdown match the trigger's width |
| `maxHeight` | `number` \| `'auto'` | — | Maximum height of the dropdown content |
| `layerMode` | `'portal'` \| `'native'` | `'portal'` | Rendering strategy |
| `disabled` | `boolean` | `false` | Prevents opening |
| `onOpenChange` | `(open: boolean, event: Event, reason: string) => void` | — | Fires when open state changes |
| `onOpenStart` | `() => void` | — | Fires when open animation starts |
| `onOpenEnd` | `() => void` | — | Fires when open animation completes |
| `onCloseStart` | `() => void` | — | Fires when close animation starts |
| `onCloseEnd` | `() => void` | — | Fires when close animation completes |

### MarketDropdown.Trigger / MarketDropdown.Content

Same API as `MarketPopover.Trigger` / `MarketPopover.Content`.

## Example

```tsx
import { MarketDropdown } from '@squareup/market-react/trial';
import { MarketButton, MarketRow } from '@squareup/market-react';

// Basic dropdown menu
<MarketDropdown placement="bottom-start">
  <MarketDropdown.Trigger>
    <MarketButton>Actions</MarketButton>
  </MarketDropdown.Trigger>
  <MarketDropdown.Content>
    <MarketRow onClick={() => handleEdit()}>Edit</MarketRow>
    <MarketRow onClick={() => handleDuplicate()}>Duplicate</MarketRow>
    <MarketRow onClick={() => handleDelete()}>Delete</MarketRow>
  </MarketDropdown.Content>
</MarketDropdown>

// Controlled dropdown
const [open, setOpen] = useState(false);

<MarketDropdown
  open={open}
  placement="bottom-end"
  onOpenChange={(isOpen) => setOpen(isOpen)}
>
  <MarketDropdown.Trigger>
    <MarketButton>More options</MarketButton>
  </MarketDropdown.Trigger>
  <MarketDropdown.Content>
    <MarketRow onClick={handleSettings}>Settings</MarketRow>
    <MarketRow onClick={handleLogout}>Log out</MarketRow>
  </MarketDropdown.Content>
</MarketDropdown>
```

## Gotchas

- **Always click-only**: You cannot configure `interaction` — it's always click. For hover/focus popovers, use MarketPopover or MarketTooltip.
- **Use for menus and action lists**: MarketDropdown is the right choice for context menus, overflow menus, and action lists. Don't use raw MarketPopover for these.
- **Compound component pattern**: Use `MarketDropdown.Trigger` and `MarketDropdown.Content`, not standalone imports.
- **No `role` prop**: The role is managed internally. Don't try to set it.
