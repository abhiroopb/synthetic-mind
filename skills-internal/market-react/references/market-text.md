# MarketText

```tsx
import { MarketText } from '@your-org/market-react/trial';
```

## Overview

Basic typography component for Market-styled text. Provides consistent text styles that match the Market design system.

## Example

```tsx
import { MarketText } from '@your-org/market-react/trial';

function ProductDetails() {
  return (
    <div>
      <MarketText>
        This is body text styled with Market typography tokens.
      </MarketText>
    </div>
  );
}
```

## Gotchas

- Import from `@your-org/market-react/trial`, not the stable export
- Use Market design tokens for custom text styling when `MarketText` doesn't cover your use case
