# MarketInlineStatus

```tsx
import { MarketInlineStatus } from '@your-org/market-react';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `status` | `'info' \| 'success' \| 'warning' \| 'error'` | — | Status type and color |
| `icon` | `boolean` | `true` | Whether to show the status icon |
| `children` | `ReactNode` | — | Text content |

## Example

```tsx
import { MarketInlineStatus } from '@your-org/market-react';

function FormFeedback() {
  return (
    <div>
      <MarketInlineStatus status="success">
        Payment processed successfully
      </MarketInlineStatus>

      <MarketInlineStatus status="error">
        Card declined — please try another payment method
      </MarketInlineStatus>

      <MarketInlineStatus
        status="warning"
        icon={false}
      >
        This action cannot be undone
      </MarketInlineStatus>

      <MarketInlineStatus status="info">
        Processing may take up to 24 hours
      </MarketInlineStatus>
    </div>
  );
}
```

## Gotchas

- **Use `status`, NOT `variant`** — the prop is `status`
- Use `icon={false}` to hide the status icon, not `hideIcon` or `showIcon`
- This is display only — not interactive, no click handlers
- Status uses `'error'`, not `'critical'` (unlike MarketBanner/MarketPill)
