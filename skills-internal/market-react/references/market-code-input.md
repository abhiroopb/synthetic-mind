# MarketCodeInput

```tsx
import { MarketCodeInput } from '@squareup/market-react/trial';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | `'text' \| 'number'` | `'number'` | Controls keyboard and validation |
| `format` | `string` | `'****'` | Pattern defining segments and characters. Each `*` = one slot, spaces = visual gaps (e.g. `'*** ***'` for 6 digits in two groups) |
| `masked` | `boolean` | `false` | Masks input like a PIN (shows dots) |
| `value` | `string` | — | Clean value without spaces (controlled mode) |
| `defaultValue` | `string` | — | Clean initial value without spaces (uncontrolled mode) |
| `invalid` | `boolean` | `false` | Sets invalid state and `aria-invalid` |
| `valid` | `boolean` | — | Shows a checkmark icon when `true` |
| `errorMessage` | `string` | — | Error message displayed below the input |
| `helperText` | `string` | — | Helper text displayed below the input |
| `trailingAccessory` | `ReactNode` | — | Trailing accessory content (icon or button) |
| `onChange` | `ChangeEventHandler<HTMLInputElement>` | — | `e.target.value` contains clean value (no spaces) |
| `onComplete` | `(value: string) => void` | — | Called with clean value when all slots are filled |

Also accepts native `React.InputHTMLAttributes<HTMLInputElement>` except `type`, `value`, `defaultValue`, `onChange`, and `maxLength`.

## Gotchas

- **Use `format`, NOT `length`** — there is no `length` prop. Use the `format` pattern (e.g. `'****'` for 4 slots, `'*** ***'` for 6 slots in two groups)
- **Values are always "clean"** — `e.target.value`, `onComplete` value, and `value`/`defaultValue` props never include formatting spaces. A format of `'*** ***'` with input `123456` gives `value="123456"`, not `"123 456"`
- **`onComplete` fires when all slots are filled** — use it for auto-submission. It receives the same clean value
- **`type="number"` is the default** — it restricts to numeric input and shows a numeric keyboard on mobile. Use `type="text"` for alphanumeric codes
- **`valid` shows a checkmark** — this is a separate visual state from `invalid`. Don't set both simultaneously
- **`maxLength` is derived from `format`** — don't set it manually
