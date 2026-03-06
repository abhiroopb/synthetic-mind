# MarketPill

```tsx
import { MarketPill } from '@squareup/market-react';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `string` | **(required)** | Text content of the pill |
| `status` | `'normal' \| 'emphasis' \| 'success' \| 'warning' \| 'critical' \| 'insight' \| 'alpha' \| 'beta'` | `'normal'` | Visual style |
| `size` | `'medium' \| 'small'` | `'medium'` | Pill size |
| `icon` | `ReactElement` (SVG) | — | Leading icon element |
| `onClick` | `MouseEventHandler` | — | Makes pill render as a `<button>` |
| `href` | `string` | — | Makes pill render as an `<a>` |

## Render modes

MarketPill renders as different elements based on props:

- **div** — no `onClick` or `href` (display only)
- **button** — when `onClick` is provided
- **anchor** — when `href` is provided

## Example

```tsx
import { MarketPill } from '@squareup/market-react';
import { CheckIcon } from '@market/market-icons';

function OrderStatus({ status }: { status: 'paid' | 'pending' | 'overdue' }) {
  const config = {
    paid: { label: 'Paid', status: 'success' as const },
    pending: { label: 'Pending', status: 'warning' as const },
    overdue: { label: 'Overdue', status: 'critical' as const },
  };

  const { label, status: pillStatus } = config[status];

  return (
    <MarketPill
      label={label}
      status={pillStatus}
    />
  );
}

// With icon
<MarketPill
  icon={<CheckIcon />}
  label="Completed"
  status="success"
/>

// As clickable button
<MarketPill
  label="Beta"
  status="beta"
  onClick={() => showBetaInfo()}
/>

// As link
<MarketPill
  href="/features/new"
  label="New feature"
  status="alpha"
/>
```

## Gotchas

- **NOT `variant`** — use `status` for the visual style
- **Content via `label` prop, NOT children** — `<MarketPill>Text</MarketPill>` is wrong
- Do not pass both `onClick` and `href` — pick one render mode
- `icon` expects a React SVG element, not a string name
