# MarketBanner

```tsx
import { MarketBanner } from '@your-org/market-react';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `status` | `'info' \| 'success' \| 'warning' \| 'critical' \| 'insight'` | `'info'` | Visual status style |
| `title` | `string` | — | Bold title text |
| `children` | `ReactNode` | — | Body content |
| `dismissible` | `boolean` | `false` | Shows dismiss button |
| `actions` | `ReactNode` | — | Action slot, typically `MarketLink` |
| `onDismiss` | `MouseEventHandler` | — | Called when dismiss button clicked |

## Example

```tsx
import { MarketBanner, MarketLink } from '@your-org/market-react';

function PaymentWarning() {
  const [visible, setVisible] = useState(true);

  if (!visible) return null;

  return (
    <MarketBanner
      dismissible
      status="warning"
      title="Payment method expiring"
      actions={
        <MarketLink href="/settings/billing">
          Update payment method
        </MarketLink>
      }
      onDismiss={() => setVisible(false)}
    >
      Your credit card ending in 4242 expires next month.
      Update your payment method to avoid service interruption.
    </MarketBanner>
  );
}
```

## Gotchas

- **NOT `variant`** — use `status` for the visual style
- **NOT `dismissable`** — the correct spelling is `dismissible`
- `onDismiss` only fires when `dismissible` is `true`
- `actions` renders below the body content — use `MarketLink` (not `MarketButton`) for banner actions
- `title` is a prop, not a child element — body content goes in `children`
