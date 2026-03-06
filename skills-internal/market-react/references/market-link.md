# MarketLink

```tsx
import { MarketLink, MarketLinkGroup } from '@squareup/market-react';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `href` | `string` | — | URL. When set, renders `<a>`. When omitted, renders `<button>` |
| `target` | `string` | — | Link target (e.g., `'_blank'`) |
| `rel` | `string` | — | Link relationship |
| `disabled` | `boolean` | `false` | Disable the link |
| `destructive` | `boolean` | `false` | Destructive styling |
| `onClick` | `MouseEventHandler` | — | Click handler |

## Example

```tsx
import { MarketLink, MarketLinkGroup } from '@squareup/market-react';

function NavigationLinks() {
  const navigate = useNavigate();

  return (
    <MarketLinkGroup>
      {/* Anchor mode — renders <a> */}
      <MarketLink
        href="https://squareup.com/help"
        target="_blank"
        rel="noopener noreferrer"
      >
        Help center
      </MarketLink>

      {/* Button mode — renders <button>, use for React Router */}
      <MarketLink onClick={() => navigate('/settings')}>
        Settings
      </MarketLink>

      {/* Destructive link */}
      <MarketLink
        destructive
        onClick={() => handleDelete()}
      >
        Delete account
      </MarketLink>
    </MarketLinkGroup>
  );
}
```

## Gotchas

- **Two render modes**: providing `href` renders an `<a>` tag; omitting it renders a `<button>`. Use button mode with `onClick` for React Router navigation.
- **Stable export** — import from `@squareup/market-react`, NOT from `/trial`.
- **MarketLinkGroup** is also a stable export for grouping multiple links.
- Do NOT use `variant` or `type` props — use `destructive` boolean for destructive styling.
