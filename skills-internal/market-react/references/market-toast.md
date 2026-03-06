# MarketToast

```tsx
import { MarketToastProvider, useMarketToast } from '@squareup/market-react/trial';
```

## MarketToastProvider props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `zIndex` | `number` | `9999` | Z-index of the toast container |
| `portalRootId` | `string` | — | Portal target element ID |

## useMarketToast hook

Returns `{ showToast, removeToast, removeAll }`.

### showToast options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `message` | `ReactNode` | — | Toast content |
| `variant` | `'info' \| 'success' \| 'warning' \| 'critical'` | `'info'` | Visual style |
| `duration` | `'short' \| 'medium' \| 'long' \| number` | `'medium'` | Auto-dismiss timing (short=2s, medium=5s, long=10s) |
| `persistent` | `boolean` | `false` | Stays until dismissed, ignores `duration` |
| `actions` | `ReactNode` | — | Action slot, typically `MarketLink` |
| `onOpen` | `() => void` | — | Called when toast appears |
| `onDismiss` | `() => void` | — | Called when toast is dismissed by user |
| `onClose` | `() => void` | — | Called when toast is removed (dismiss or timeout) |

`showToast` returns a toast ID string for programmatic removal via `removeToast(id)`.

## Gotchas

- **Requires `MarketToastProvider`** wrapping your app — toasts won't render without it
- **NOT `useToaster`** from `@squareup/shared-ui-react` — use `useMarketToast` from `@squareup/market-react/trial`
- **NOT `text` prop** — use `message` for toast content
- `persistent: true` overrides `duration` — the toast stays until the user dismisses it
- `showToast` returns a string ID — save it if you need `removeToast(id)` later
- Import from `@squareup/market-react/trial`, not the stable export
