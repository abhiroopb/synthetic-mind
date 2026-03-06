# MarketAccessory

```tsx
import { MarketAccessory } from '@squareup/market-react';
```

## Overview

`MarketAccessory` is the stable component for wrapping custom SVGs or images as accessories. It is used with `leadingAccessory` and `trailingAccessory` props on components like `MarketRow` and `MarketInput`.

## Props

No required props. Wrap your SVG or image element as a child.

## Example

```tsx
import { MarketAccessory, MarketRow, MarketInput } from '@squareup/market-react';
import { SearchIcon, ChevronRightIcon } from '@market/market-icons';

// Leading accessory on a row
<MarketRow
  leadingAccessory={
    <MarketAccessory>
      <SearchIcon />
    </MarketAccessory>
  }
>
  Search results
</MarketRow>

// Trailing accessory on a row
<MarketRow
  trailingAccessory={
    <MarketAccessory>
      <ChevronRightIcon />
    </MarketAccessory>
  }
>
  View details
</MarketRow>

// Leading accessory on an input
<MarketInput
  leadingAccessory={
    <MarketAccessory>
      <SearchIcon />
    </MarketAccessory>
  }
  placeholder="Search items..."
/>

// Custom image accessory
<MarketRow
  leadingAccessory={
    <MarketAccessory>
      <img
        alt="Item thumbnail"
        src={thumbnailUrl}
      />
    </MarketAccessory>
  }
>
  Item name
</MarketRow>
```

## Gotchas

- There is no `MarketIcon` component — use `MarketAccessory` to wrap SVGs/images
- Pass `MarketAccessory` to `leadingAccessory` / `trailingAccessory` props, do not nest it as a child of `MarketRow`
- Icons from `@market/market-icons` are SVG React components — wrap them in `MarketAccessory` when used as accessories
