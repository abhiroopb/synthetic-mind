# MarketCard — examples and patterns

## Example

```tsx
import { MarketCard } from '@squareup/market-react/trial';
import { MarketAccessory } from '@squareup/market-react';

// Readonly card
<MarketCard title="Revenue">
  <p>$12,345.00</p>
</MarketCard>

// Emphasis readonly card
<MarketCard
  appearance="emphasis"
  title="Highlighted metric"
>
  <p>99.9% uptime</p>
</MarketCard>

// Selectable card (checkbox mode)
<MarketCard
  controlPosition="leading"
  mode="checkbox"
  selected={isSelected}
  title="Premium plan"
  value="premium"
  onSelectedChange={(e) => setIsSelected(e.detail.selected)}
>
  <p>$29/month</p>
</MarketCard>

// Transient card (clickable, no persistent selection)
<MarketCard
  mode="transient"
  title="View details"
  onClick={handleClick}
/>

// Link card
<MarketCard
  href="/settings"
  title="Account settings"
/>
```

