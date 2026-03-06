# MarketSpinner and MarketSkeletonLoader

```tsx
// Stable
import { MarketSpinner, MarketSkeletonLoader } from '@your-org/market-react';

// Trial
import { MarketProgressMeter } from '@your-org/market-react/trial';
```

## MarketSpinner props

No required props. Renders an indeterminate loading spinner.

## MarketSkeletonLoader props

No required props. Renders a pulsing content placeholder for loading states.

## MarketProgressMeter props (trial)

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | `'bar' \| 'radial'` | — | Display type |
| `percent` | `number` (0–100) | — | Progress percentage |
| `size` | `'small' \| 'large'` | `'large'` | Size variant |

## Example

```tsx
import { MarketSpinner, MarketSkeletonLoader } from '@your-org/market-react';
import { MarketProgressMeter } from '@your-org/market-react/trial';

// Simple loading spinner
function LoadingView() {
  return <MarketSpinner />;
}

// Skeleton placeholder for content loading
function ItemListSkeleton() {
  return (
    <div>
      <MarketSkeletonLoader />
      <MarketSkeletonLoader />
      <MarketSkeletonLoader />
    </div>
  );
}

// Progress bar
function UploadProgress({ percent }: { percent: number }) {
  return (
    <MarketProgressMeter
      percent={percent}
      type="bar"
    />
  );
}

// Radial progress
function CompletionIndicator({ percent }: { percent: number }) {
  return (
    <MarketProgressMeter
      percent={percent}
      size="small"
      type="radial"
    />
  );
}
```

## Gotchas

- `MarketSpinner` and `MarketSkeletonLoader` are stable imports; `MarketProgressMeter` is trial
- `MarketProgressMeter` `percent` is 0–100, not 0–1
- Use `MarketSkeletonLoader` for content placeholders (e.g., list rows) — use `MarketSpinner` for general indeterminate loading
- `MarketProgressMeter` requires both `type` and `percent` to render meaningfully
