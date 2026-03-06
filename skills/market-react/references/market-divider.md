# MarketDivider

## Import

```tsx
import { MarketDivider } from '@squareup/market-react';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| — | — | — | No required or notable props. Renders a horizontal visual separator. |

## Example

```tsx
import { MarketDivider } from '@squareup/market-react';

// Simple section separator
<div>
  <p>Section A content</p>
  <MarketDivider />
  <p>Section B content</p>
</div>
```

## Gotchas

- **Stable import**: MarketDivider is exported from `@squareup/market-react` (not `/trial`).
- **No semantic meaning**: This is a visual-only separator. It does not imply any semantic grouping — use appropriate HTML sectioning elements for that.
