# MarketGrid — examples and patterns

## Example

```tsx
import { MarketGrid } from '@squareup/market-react/trial';

// Basic responsive grid
<MarketGrid columns={{ narrow: 1, medium: 2, wide: 3 }}>
  <MarketGrid.Item>
    <p>Item 1</p>
  </MarketGrid.Item>
  <MarketGrid.Item>
    <p>Item 2</p>
  </MarketGrid.Item>
  <MarketGrid.Item>
    <p>Item 3</p>
  </MarketGrid.Item>
</MarketGrid>

// Fixed 4-column grid with custom gap
<MarketGrid
  columns={4}
  gap={300}
>
  <MarketGrid.Item span={2}>
    <p>Wide item (spans 2 columns)</p>
  </MarketGrid.Item>
  <MarketGrid.Item>
    <p>Normal item</p>
  </MarketGrid.Item>
  <MarketGrid.Item>
    <p>Normal item</p>
  </MarketGrid.Item>
</MarketGrid>

// Full-width header with responsive items below
<MarketGrid columns={{ narrow: 1, medium: 2, wide: 4 }}>
  <MarketGrid.Item span="full">
    <h2>Dashboard</h2>
  </MarketGrid.Item>
  <MarketGrid.Item span={{ narrow: 'full', medium: 1 }}>
    <p>Metric A</p>
  </MarketGrid.Item>
  <MarketGrid.Item span={{ narrow: 'full', medium: 1 }}>
    <p>Metric B</p>
  </MarketGrid.Item>
</MarketGrid>

// Container-query mode
<MarketGrid
  columns={{ narrow: 1, medium: 2 }}
  mode="container"
>
  <MarketGrid.Item>
    <p>Adapts to container width</p>
  </MarketGrid.Item>
  <MarketGrid.Item>
    <p>Not viewport width</p>
  </MarketGrid.Item>
</MarketGrid>
```

