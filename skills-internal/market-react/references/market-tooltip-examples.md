# MarketTooltip and MarketToggletip — examples and patterns

## Example

```tsx
import { MarketTooltip, MarketToggletip } from '@squareup/market-react/trial';
import { MarketButton, MarketLink, MarketPill } from '@squareup/market-react';

// Simple hover tooltip
<MarketTooltip placement="top">
  <MarketTooltip.Trigger>
    <MarketButton>Save</MarketButton>
  </MarketTooltip.Trigger>
  <MarketTooltip.Content>
    Save your changes (⌘S)
  </MarketTooltip.Content>
</MarketTooltip>

// Toggletip with info icon trigger (no children = auto icon)
<MarketToggletip>
  <MarketToggletip.Trigger ariaLabel="Learn more about pricing" />
  <MarketToggletip.Content>
    <p>Pricing is based on your plan tier.</p>
  </MarketToggletip.Content>
</MarketToggletip>

// Toggletip with text trigger and actions
<MarketToggletip
  actions={<MarketLink href="/help">Learn more</MarketLink>}
>
  <MarketToggletip.Trigger>What's this?</MarketToggletip.Trigger>
  <MarketToggletip.Content>
    <p>This feature allows you to customize your storefront.</p>
  </MarketToggletip.Content>
</MarketToggletip>

// Toggletip with pill trigger
<MarketToggletip>
  <MarketToggletip.Trigger>
    <MarketPill label="Beta" />
  </MarketToggletip.Trigger>
  <MarketToggletip.Content>
    <p>This feature is in beta and may change.</p>
  </MarketToggletip.Content>
</MarketToggletip>
```

