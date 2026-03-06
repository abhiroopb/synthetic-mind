# MarketPagingTabs and MarketSegmentedControl

```tsx
import { MarketPagingTabs, MarketSegmentedControl } from '@your-org/market-react/trial';
```

## Gotchas

- **MarketPagingTabs `onSelectedTabChange` is NOT a CustomEvent** — it receives a plain `{ prevValue, value }` object. Do NOT use `e.detail.value`.
- **MarketSegmentedControl `onChange` IS a CustomEvent** — use `e.detail.value`. These two components have **different callback signatures**.
- **Panel order matters** — `MarketPagingTabPanel` components must appear in the same order as their corresponding `MarketPagingTab` components.
- **`id` is required on `MarketPagingTab`** when using controlled mode (`selectedTab`).
- Both components are **trial** exports — import from `@your-org/market-react/trial`.
