# MarketPopover — examples and patterns

## Example

```tsx
import { MarketPopover } from '@your-org/market-react/trial';
import { MarketButton } from '@your-org/market-react';

// Uncontrolled click popover
<MarketPopover placement="bottom-start">
  <MarketPopover.Trigger>
    <MarketButton>Open menu</MarketButton>
  </MarketPopover.Trigger>
  <MarketPopover.Content>
    <p>Popover content here</p>
  </MarketPopover.Content>
</MarketPopover>

// Controlled popover with hover interaction
const [open, setOpen] = useState(false);

<MarketPopover
  interaction={{ hover: true, focus: true }}
  open={open}
  placement="top"
  role="tooltip"
  onOpenChange={(isOpen) => setOpen(isOpen)}
>
  <MarketPopover.Trigger>
    <span>Hover me</span>
  </MarketPopover.Trigger>
  <MarketPopover.Content>
    <p>Helpful tooltip text</p>
  </MarketPopover.Content>
</MarketPopover>

// Popover matching trigger width (e.g., for a custom dropdown)
<MarketPopover
  matchTriggerWidth
  placement="bottom"
  role="listbox"
>
  <MarketPopover.Trigger>
    <MarketButton>Select option</MarketButton>
  </MarketPopover.Trigger>
  <MarketPopover.Content>
    <ul>
      <li>Option A</li>
      <li>Option B</li>
    </ul>
  </MarketPopover.Content>
</MarketPopover>
```

