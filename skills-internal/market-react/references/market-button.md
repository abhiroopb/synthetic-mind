# MarketButton

Load when building any button, link-styled-as-button, or dropdown trigger in market-react.

## Import

```tsx
import { MarketButton } from '@squareup/market-react';
import type { MarketButtonProps } from '@squareup/market-react';

// MarketButtonGroup is a TRIAL component
import { MarketButtonGroup } from '@squareup/market-react/trial';
```

## Props

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `rank` | `'primary' \| 'secondary' \| 'tertiary' \| 'subtle'` | `'secondary'` | `'subtle'` is icon-only with fixed 24px height |
| `size` | `'large' \| 'medium' \| 'small'` | `'medium'` | Not available for `rank="subtle"` |
| `destructive` | `boolean` | `false` | Applies destructive action styling. NOT a variant string |
| `loading` | `boolean` | `false` | Shows spinner and prevents interaction |
| `disabled` | `boolean` | `false` | Prevents interaction and applies disabled styling |
| `icon` | `ReactElement<SVGProps<SVGElement>>` | — | SVG element rendered alongside text content |
| `noCaret` | `boolean` | `false` | Removes the caret icon in dropdown usage |
| `children` | `string` | — | Button label. Not allowed for `rank="subtle"` |
| `type` | `'button' \| 'submit' \| 'reset'` | `'button'` | Only for `<button>` rendering. Not allowed when `href` is set |
| `href` | `string` | — | When set, renders as `<a>` instead of `<button>` |
| `target` | anchor target | — | Only when `href` is set |
| `rel` | anchor rel | — | Only when `href` is set |
| `aria-label` | `string` | — | Required for icon-only buttons (no children) and `rank="subtle"` |
| `aria-expanded` | `boolean` | — | Dropdown pattern: set `true`/`false` for open/closed |
| `aria-controls` | `string` | — | Required when `aria-expanded` is `true` |
| `onClick` | mouse event handler | — | `MouseEventHandler<HTMLButtonElement>` or `MouseEventHandler<HTMLAnchorElement>` depending on `href` |

## Gotchas

1. `rank` defaults to `'secondary'`, not `'primary'` — explicitly set `rank="primary"` for primary actions.
2. `type` defaults to `'button'`, not `'submit'` — set `type="submit"` for form submissions.
3. `rank="subtle"` enforces icon-only: `children` and `size` are `never` types; `icon` and `aria-label` are required.
4. `destructive` is a boolean prop, NOT `variant="destructive"` — the old web component API is gone.
5. When `aria-expanded` is `true`, `aria-controls` is required. When `false`, it's optional.
6. `onClick` type differs based on whether `href` is set: `MouseEventHandler<HTMLButtonElement>` vs `MouseEventHandler<HTMLAnchorElement>`.
7. `MarketButtonGroup` is a **trial** component — import from `@squareup/market-react/trial`, not the main export.
8. Content requirements are enforced by TypeScript: you must provide either `children` (string) or `icon` + `aria-label`. You cannot have an empty button.
