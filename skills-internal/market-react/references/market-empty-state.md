# MarketEmptyState

```tsx
import { MarketEmptyState } from '@squareup/market-react/trial';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `primaryText` | `ReactNode` | — | Heading text |
| `secondaryText` | `ReactNode` | — | Description text |
| `actions` | `ReactNode` | — | Action buttons |
| `icon` | `ReactNode` | — | Illustration or icon (auto-sized to 48px) |
| `borderless` | `boolean` | `false` | Removes default border |
| ~~`media`~~ | ~~`ReactNode`~~ | — | **Deprecated** — use `icon` instead |

## Example

```tsx
import { MarketEmptyState } from '@squareup/market-react/trial';
import { MarketButton } from '@squareup/market-react';
import { PlusIcon } from '@market/market-icons';

function EmptyItemsList() {
  return (
    <MarketEmptyState
      icon={<PlusIcon />}
      primaryText="No items yet"
      secondaryText="Create your first item to start selling."
      actions={
        <MarketButton
          onClick={() => navigateToCreateItem()}
        >
          Create item
        </MarketButton>
      }
    />
  );
}

// Borderless variant for inline empty states
function EmptySearchResults() {
  return (
    <MarketEmptyState
      borderless
      primaryText="No results found"
      secondaryText="Try a different search term."
    />
  );
}
```

## Gotchas

- **`media` is deprecated** — use `icon` instead
- `icon` is auto-sized to 48px — don't manually set icon dimensions
- Import from `@squareup/market-react/trial`, not the stable export
- `actions` accepts any `ReactNode` — typically one or two `MarketButton` components
