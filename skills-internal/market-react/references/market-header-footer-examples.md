# MarketHeader and MarketFooter — examples and patterns

## Example

```tsx
import { MarketModal, MarketHeader, MarketFooter, MarketButton } from '@squareup/market-react/trial';

// Header with title, secondary text, and action buttons inside a modal
<MarketModal type="partial" onClose={onClose}>
  <MarketHeader
    title="Create item"
    secondaryText="Add a new item to your catalog"
    leadingActions={<MarketButton rank="secondary" onClick={onClose}>Cancel</MarketButton>}
    trailingActions={<MarketButton onClick={onSave}>Save</MarketButton>}
  />
  <main>{/* Form content */}</main>
  <MarketFooter>
    <MarketButton rank="secondary" onClick={onClose}>Cancel</MarketButton>
    <MarketButton onClick={onSave}>Save</MarketButton>
  </MarketFooter>
</MarketModal>

// Header with eyebrow text
<MarketHeader title="Item details" secondaryText="CATALOG" secondaryTextPosition="eyebrow" />

// Compact header with back navigation
<MarketHeader compact title="Long title truncated with ellipsis" size="compact"
  leadingActions={<MarketButton rank="secondary" onClick={onBack}>Back</MarketButton>}
/>

// Footer with single action
<MarketFooter>
  <MarketButton onClick={onDone}>Done</MarketButton>
</MarketFooter>
```

## Patterns

- **Header actions**: `leadingActions` (left) and `trailingActions` (right) accept `MarketButton` elements.
- **Secondary text**: Below title by default; use `secondaryTextPosition="eyebrow"` to place above.
- **Compact**: `compact` + `size="compact"` for smaller header with truncated title.
- **Footer**: Renders children as actions. Two buttons auto-split left/right.
