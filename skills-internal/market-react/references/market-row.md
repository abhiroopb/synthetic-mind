# MarketRow

```tsx
import { MarketRow } from '@your-org/market-react';
```

## Props

### Common props (all row types)

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `ReactNode` | **required** | Primary text content |
| `secondaryText` | `ReactNode` | — | Secondary line of text |
| `tertiaryText` | `ReactNode` | — | Tertiary line of text |
| `sideText` | `ReactNode` | — | Right-aligned primary text |
| `secondarySideText` | `ReactNode` | — | Right-aligned secondary text |
| `leadingAccessory` | `ReactNode` | — | Left-side accessory (icon, avatar, thumbnail) |
| `trailingAccessory` | `ReactNode` | — | Right-side accessory (icon, chevron) |
| `titlePill` | `ReactNode` | — | MarketPill element displayed after the title |
| `inlineStatus` | `ReactNode` | — | MarketInlineStatus element |
| `linkActions` | `ReactNode` | — | MarketLink elements |
| `size` | `'small' \| 'medium'` | `'medium'` | Row size variant |
| `verticalAlignment` | `'center' \| 'top'` | `'center'` | Vertical alignment of content |

### Readonly row (renders as div)

No additional props. Omit `mode` and `href` for a readonly row.

### Transient row (renders as button)

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `mode` | `'destructive' \| 'transient'` | — | Row interaction mode |
| `disabled` | `boolean` | `false` | Disables interaction |
| `onClick` | `() => void` | — | Click handler |

### Selectable row (renders as button)

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `mode` | `'checkbox' \| 'radio' \| 'toggle' \| 'selectable' \| 'toggleable'` | — | Selection mode |
| `selected` | `boolean` | — | Controlled selected state |
| `defaultSelected` | `boolean` | — | Uncontrolled initial selected state |
| `value` | `TValue` | — | Value emitted on selection change |
| `controlPosition` | `'leading' \| 'trailing'` | `'leading'` | Position of the selection control |
| `disabled` | `boolean` | `false` | Disables interaction |
| `onSelectedChange` | `(e: CustomEvent<{ selected: boolean; value: TValue }>) => void` | — | Selection change callback |

### Link row (renders as anchor)

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `href` | `string` | — | Link destination (presence makes it a link row) |
| `target` | `string` | — | Link target (`_blank`, etc.) |
| `rel` | `string` | — | Link relationship |

## Gotchas

| Wrong | Correct | Why |
|-------|---------|-----|
| `<MarketRow><span slot="label">Title</span></MarketRow>` | `<MarketRow title="Title" />` | No slots — all content goes through named props |
| `<MarketRow>Title text</MarketRow>` | `<MarketRow title="Title text" />` | `children` is never used; use `title` prop |
| `<MarketRow><MarketCheckbox /></MarketRow>` | `<MarketRow mode="checkbox" />` | Controls are built-in via `mode` prop |
| `<MarketRow mode="radio" checked>` | `<MarketRow mode="radio" selected>` | Use `selected` / `defaultSelected`, not `checked` |
| `onChange={(e) => ...}` | `onSelectedChange={(e) => ...}` | Selection callback is `onSelectedChange` |
| `e.target.checked` | `e.detail.selected` | Value comes from `e.detail`, not `e.target` |
| `disabled` on readonly row | `disabled` on transient/selectable rows only | Readonly rows don't support `disabled` |
