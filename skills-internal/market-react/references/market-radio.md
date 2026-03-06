# MarketRadio

```tsx
import { MarketRadio } from '@squareup/market-react';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `checked` | `boolean` | — | Current selected state (controlled mode, requires `onChange`) |
| `defaultChecked` | `boolean` | — | Initial selected state (uncontrolled mode) |
| `disabled` | `boolean` | — | Prevents interaction, applies disabled styling |
| `id` | `string` | — | HTML id, used for associating with a label |
| `invalid` | `boolean` | — | Controls invalid styling and `aria-invalid` |
| `name` | `string` | — | Groups related radios and identifies selection in form submissions |
| `required` | `boolean` | — | Makes the radio required for form submission |
| `value` | `string` | `"on"` | Value submitted in form data |
| `onChange` | `ChangeEventHandler<HTMLInputElement>` | — | Required in controlled mode, optional in uncontrolled |

Also accepts all `React.InputHTMLAttributes<HTMLInputElement>` except `type`.

**Discriminated union**: If you pass `checked`, you **must** also pass `onChange` (controlled mode). If you use `defaultChecked`, `onChange` is optional (uncontrolled mode). You cannot pass both `checked` and `defaultChecked`.

## Gotchas

- **Prefer MarketRow with `mode="radio"`** — MarketRadio is primarily used inside `<MarketRow mode="radio">`. The row manages selected state via its `selected` prop; `MarketRadio` is the visual indicator
- **Don't set `checked` on MarketRadio inside a MarketRow** — the row's `selected` prop drives the radio's visual state. Setting `checked` directly can conflict
- **Controlled mode enforces `onChange`** — if you pass `checked`, TypeScript requires you also pass `onChange`
- **Use `e.target.checked`** — standard React change event, NOT `e.detail.value`
- **Group with `name`** — for standalone radios, use the same `name` prop to group them. Inside MarketRow/MarketList, grouping is handled by the list
