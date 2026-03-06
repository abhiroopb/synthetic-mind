# MarketHeader and MarketFooter

```tsx
import { MarketHeader, MarketFooter } from '@your-org/market-react/trial';
```

## MarketHeader props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `string` | — | Header title text (rendered as h2) |
| `secondaryText` | `string` | — | Secondary descriptive text |
| `secondaryTextPosition` | `'eyebrow' \| 'subtitle'` | `'subtitle'` | Position of secondary text relative to title |
| `compact` | `boolean` | `false` | Truncates the title with ellipsis |
| `size` | `'large' \| 'compact'` | `'large'` | Header size variant |
| `contentWidth` | `'regular' \| 'wide' \| 'fluid'` | — | Content width constraint |
| `leadingActions` | `ReactNode` | — | Left-side actions (close/back buttons) |
| `trailingActions` | `ReactNode` | — | Right-side actions (action buttons) |

## MarketFooter props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `ReactNode` | — | Footer content, typically MarketButton components |

**Footer layout**: Single button is positioned left. Two buttons are automatically split left/right.

## Gotchas

| Wrong | Correct | Why |
|-------|---------|-----|
| `showNavigation` / `onNavigate` | `leadingActions` / `trailingActions` | Old slot-based API is removed; use action props |
| `<slot name="navigation">` | `leadingActions={<MarketButton>...</MarketButton>}` | No slots — pass ReactNode to action props |
| `<h2>Title</h2>` as children | `title="Title"` | Title is a string prop, not a child element |
| `<MarketHeader>` with children for title | `<MarketHeader title="...">` | Title goes in the prop, not as children |
| `variant="compact"` | `size="compact"` | Size prop, not variant |
