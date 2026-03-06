# MarketPagingTabs and MarketSegmentedControl — examples and patterns

## MarketPagingTabs

- Compound components: **MarketPagingTabList** (wrapper), **MarketPagingTab** (button, `id` required), **MarketPagingTabPanel** (content, order must match tabs)
- `onSelectedTabChange` receives a **plain object** `{ prevValue, value }`, NOT a CustomEvent
- Props: `selectedTab`, `defaultTab`, `size` (`'small' | 'medium' | 'large'`)

```tsx
import { MarketPagingTabs, MarketPagingTabList, MarketPagingTab, MarketPagingTabPanel } from '@squareup/market-react/trial';

const [tab, setTab] = useState('general');

<MarketPagingTabs selectedTab={tab} onSelectedTabChange={({ value }) => setTab(value)}>
  <MarketPagingTabList>
    <MarketPagingTab id="general">General</MarketPagingTab>
    <MarketPagingTab id="billing">Billing</MarketPagingTab>
    <MarketPagingTab id="notifications">Notifications</MarketPagingTab>
  </MarketPagingTabList>
  <MarketPagingTabPanel>General settings content</MarketPagingTabPanel>
  <MarketPagingTabPanel>Billing settings content</MarketPagingTabPanel>
  <MarketPagingTabPanel>Notifications content</MarketPagingTabPanel>
</MarketPagingTabs>
```

## MarketSegmentedControl

- Compound component: **MarketSegmentedControl.Segment** (`value` required)
- `onChange` receives a **CustomEvent** `e.detail.value`
- Props: `value`, `defaultValue`, `disabled`

```tsx
import { MarketSegmentedControl } from '@squareup/market-react/trial';

const [view, setView] = useState('list');

<MarketSegmentedControl value={view} onChange={(e) => setView(e.detail.value)}>
  <MarketSegmentedControl.Segment value="list">List</MarketSegmentedControl.Segment>
  <MarketSegmentedControl.Segment value="grid">Grid</MarketSegmentedControl.Segment>
</MarketSegmentedControl>
```
