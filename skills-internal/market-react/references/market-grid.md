# MarketGrid

## Import

```tsx
import { MarketGrid } from '@your-org/market-react/trial';
```

## Props

### MarketGrid

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `columns` | `number` \| `{ narrow?: number; medium?: number; wide?: number; extraWide?: number }` | `{ narrow: 1, medium: 2, wide: 4, extraWide: 4 }` | Number of columns, or responsive breakpoint object |
| `gap` | `number` | `200` | Spacing token number (e.g., `100`, `200`, `300`) |
| `align` | `'start'` \| `'center'` \| `'end'` | — | Horizontal alignment of items within cells |
| `valign` | `'start'` \| `'center'` \| `'end'` | — | Vertical alignment of items within cells |
| `mode` | `'viewport'` \| `'container'` | `'viewport'` | Whether breakpoints reference viewport or container width |
| `children` | `ReactNode` | — | MarketGrid.Item children |

### MarketGrid.Item

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `span` | `number` \| `'full'` \| `'grow'` \| `'content'` \| `{ narrow?: ...; medium?: ...; wide?: ...; extraWide?: ... }` | `'full'` | How many columns this item spans, or responsive object |
| `children` | `ReactNode` | — | Item content |

## Gotchas

- **Responsive values inherit upward (mobile-first)**: Setting `{ narrow: 1, wide: 3 }` means `medium` inherits `1` from `narrow`. Always specify from smallest breakpoint up.
- **`gap` is a token number, not pixels**: Use Market spacing token numbers like `100`, `200`, `300` — not raw pixel values.
- **`span="full"` vs a number**: `'full'` spans all columns regardless of count. `'grow'` fills remaining space. `'content'` sizes to content.
- **Compound component pattern**: Use `MarketGrid.Item`, not a separate import.
- **`mode="container"` requires container support**: Uses CSS container queries. Older browsers may not support this.
