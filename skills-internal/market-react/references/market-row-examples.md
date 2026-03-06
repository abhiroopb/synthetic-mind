# MarketRow — examples and patterns

## Example

```tsx
import { MarketRow, MarketPill, MarketInlineStatus } from '@squareup/market-react';

// Readonly row with side text
<MarketRow title="Order #1234" secondaryText="Placed on Jan 15, 2026" sideText="$42.00" secondarySideText="Paid" />

// Selectable row (mode: "checkbox" | "toggle" | "radio")
<MarketRow
  mode="checkbox"
  selected={isSelected}
  title="Enable notifications"
  secondaryText="Receive alerts for new orders"
  value="notifications"
  controlPosition="trailing"
  onSelectedChange={(e) => setIsSelected(e.detail.selected)}
/>

// Transient (action) / destructive rows
<MarketRow mode="transient" title="Add new item" leadingAccessory={<PlusIcon />} onClick={handleAdd} />
<MarketRow mode="destructive" title="Delete item" leadingAccessory={<TrashIcon />} onClick={handleDelete} />

// Row with pill, inline status, and link
<MarketRow
  title="Premium plan"
  titlePill={<MarketPill label="Active" status="success" />}
  inlineStatus={<MarketInlineStatus status="success">Paid through March</MarketInlineStatus>}
  sideText="$29/mo"
/>
<MarketRow href="/items/123" title="Widget A" sideText="$9.99" trailingAccessory={<ChevronIcon />} />

// Small row, top-aligned for multi-line content
<MarketRow size="small" title="Tax rate" sideText="8.5%" />
<MarketRow title="Meeting notes" secondaryText="Long description..." tertiaryText="Updated 2h ago" verticalAlignment="top" />
```
