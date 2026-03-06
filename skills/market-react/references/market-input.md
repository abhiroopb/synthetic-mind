# MarketInput

Load when building any text input, textarea, search bar, or password field in market-react.

## Import

```tsx
import { MarketInput } from '@squareup/market-react';
import type { MarketInputProps, MarketInputElement } from '@squareup/market-react';
```

## Props

### Base props (all input types)

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `type` | `'text' \| 'number' \| 'email' \| 'password' \| 'tel' \| 'url' \| 'multiline' \| 'search'` | `'text'` | `'multiline'` renders `<textarea>`, `'search'` enables search features |
| `label` | `string` | — | Text label that floats on focus/value. For search, used as aria-label/placeholder fallback |
| `size` | `'small' \| 'medium'` | `'medium'` | Input size variant |
| `invalid` | `boolean` | `false` | Sets invalid state and `aria-invalid` |
| `disabled` | `boolean` | `false` | Prevents user interaction |
| `readOnly` | `boolean` | — | Makes the input read-only |
| `value` | `string` | — | Controlled value |
| `defaultValue` | `string` | — | Initial value for uncontrolled inputs |
| `leadingAccessory` | `ReactNode` | — | Content at the start of the input. Overridden by search icon when `type="search"` |
| `trailingAccessory` | `ReactNode` | — | Content at the end of the input |
| `placeholder` | `string` | — | Placeholder text. For search, falls back to `label` |
| `onChange` | `ChangeEventHandler<HTMLInputElement \| HTMLTextAreaElement>` | — | Standard React change handler |
| `onFocus` | `FocusEventHandler` | — | Focus handler |
| `onBlur` | `FocusEventHandler` | — | Blur handler |

### Search-specific props (only when `type="search"`)

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `onCleared` | `() => void` | — | Called when clear button is clicked |
| `clearButtonProps` | `{ 'aria-label'?: string }` | — | Props for the clear button |
| `searchIconButtonProps` | `{ 'aria-label'?: string }` | — | Props for the search icon button |
| `compact` | `boolean` | `false` | Compact search mode; expands on focus/type |

## Gotchas

1. This is a **single component** for all input types — there is no separate `MarketInputText`, `MarketInputSearch`, or `MarketInputPassword`. Those are old web component patterns.
2. `type="multiline"` renders a `<textarea>`, not an `<input>`. The `onChange` event type is `ChangeEvent<HTMLInputElement | HTMLTextAreaElement>`.
3. `type="search"` overrides `leadingAccessory` with the search/back icon. Your custom `leadingAccessory` will not render.
4. `type="search"` uses `label` as the fallback for both `aria-label` and `placeholder` when those props are not explicitly set.
5. The `size` prop only has two values: `'small'` and `'medium'`. There is no `'large'` size.
6. `MarketInputElement` is the ref type: `HTMLInputElement | HTMLTextAreaElement`. Use this for `useRef`.
7. The `compact` prop is only for `type="search"`. It collapses the input to icon-only until focused or typed into.
8. Do not mix `value` and `defaultValue` — the component will warn about controlled/uncontrolled conflicts.
