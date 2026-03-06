# MarketList and MarketCollection — examples and patterns

## Example

```tsx
import { MarketList } from '@your-org/market-react/trial';
import { MarketRow } from '@your-org/market-react';

// Single-select list (radio)
const [selected, setSelected] = useState<string>('medium');
<MarketList selectionMode="single" selectedValue={selected} onSelectionChange={(e) => setSelected(e.detail.value)}>
  <MarketRow mode="radio" title="Small" value="small" />
  <MarketRow mode="radio" title="Medium" value="medium" />
  <MarketRow mode="radio" title="Large" value="large" />
</MarketList>

// Multi-select list (checkbox)
<MarketList selectionMode="multiple" selectedValues={perms} onSelectionChange={(e) => setPerms(e.detail.values)}>
  <MarketRow mode="checkbox" title="View reports" value="reports:read" />
  <MarketRow mode="checkbox" title="Edit items" value="items:write" />
  <MarketRow mode="checkbox" title="Manage team" value="team:admin" />
</MarketList>

// Toggle list
<MarketList selectionMode="multiple" selectedValues={enabled} onSelectionChange={(e) => setEnabled(e.detail.values)}>
  <MarketRow mode="toggle" title="Email notifications" value="email" controlPosition="trailing" />
  <MarketRow mode="toggle" title="SMS notifications" value="sms" controlPosition="trailing" />
</MarketList>

// Non-selectable list (navigable rows)
<MarketList showDividers={false}>
  {orders.map((o) => (
    <MarketRow key={o.id} href={`/orders/${o.id}`} title={`Order #${o.number}`} secondaryText={o.date} sideText={o.total} />
  ))}
</MarketList>
```

## Patterns

- **Single select**: `selectionMode="single"` + `selectedValue` + `onSelectionChange`. Row uses `mode="radio"`.
- **Multi select**: `selectionMode="multiple"` + `selectedValues` (Set) + `onSelectionChange`. Row uses `mode="checkbox"`.
- **Toggle**: Row uses `mode="toggle"` with `controlPosition="trailing"`. List still uses `selectionMode="multiple"`.
- **Non-selectable**: Omit `selectionMode`. Rows can use `href` for navigation.
- **No dividers**: `showDividers={false}` for card-style layouts.
