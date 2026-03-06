# Common pitfalls (continued)

Advanced component pitfalls — continuation of [pitfalls.md](pitfalls.md).

## MarketToast

| Wrong | Correct |
|-------|---------|
| `import { useToaster } from '@squareup/shared-ui'` | `import { useMarketToast, MarketToastProvider } from '@squareup/market-react/trial'` |
| `toast({ text: 'Saved' })` | `toast({ message: 'Saved' })` |

Use `useMarketToast` with `MarketToastProvider`, NOT `useToaster` from shared-ui. The content prop is `message`, NOT `text`.

## MarketPill

| Wrong | Correct |
|-------|---------|
| `<MarketPill>Active</MarketPill>` | `<MarketPill label="Active" />` |
| `variant="success"` | `status="success"` |

`label` is a **required prop** — content is NOT passed as children. Use `status` not `variant`.

## MarketBanner

| Wrong | Correct |
|-------|---------|
| `dismissable` | `dismissible` |
| `variant="info"` | `status="info"` |

Note the spelling: `dismissible` (with **i**), not `dismissable`. Use `status` not `variant`.

## MarketSelect

| Wrong | Correct |
|-------|---------|
| `onChange={(value) => ...}` | `onSelectionChange={(e) => e.detail.value}` |
| Direct value callback | CustomEvent with `{ prevValue, value }` detail |

MarketSelect uses **CustomEvent-based** `onSelectionChange`, not a direct value callback. Access the value via `e.detail.value`.

## Event handler patterns

| Pattern | Wrong | Correct |
|---------|-------|---------|
| Web component events | `onMarketClick` | `onClick` |
| Custom event detail | `e.detail.value` (always) | Varies by component — check each reference |
| Standard inputs | `onValueChange` | `onChange` with `e.target.value` (MarketSlider) |

**Event callbacks are NOT uniform across components.** Some use CustomEvent (`onSelectionChange`, `onValueChange` on MarketColorPicker), some use plain objects (`onSelectedTabChange` on MarketPagingTabs), some use direct value callbacks (`onValueChange` on MarketStepper), and some use standard React events (`onChange` on MarketSlider). Always check the specific component reference.
