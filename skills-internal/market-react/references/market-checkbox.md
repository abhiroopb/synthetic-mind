# MarketCheckbox

```tsx
import { MarketCheckbox } from '@squareup/market-react';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `checked` | `boolean` | — | Current checked state (controlled mode) |
| `defaultChecked` | `boolean` | — | Initial checked state (uncontrolled mode) |
| `indeterminate` | `boolean` | — | Current indeterminate state (controlled mode) |
| `defaultIndeterminate` | `boolean` | — | Initial indeterminate state (uncontrolled mode) |
| `disabled` | `boolean` | — | Prevents interaction, applies disabled styling |
| `invalid` | `boolean` | — | Controls invalid styling and `aria-invalid` |
| `name` | `string` | — | HTML name for form submissions |
| `required` | `boolean` | — | Makes checkbox required for form submission |
| `value` | `string` | `"on"` | Value submitted in form data |
| `onChange` | `ChangeEventHandler<HTMLInputElement>` | — | Handles checked state changes |

Also accepts all `React.InputHTMLAttributes<HTMLInputElement>` except `type`.

## Example

```tsx
// Controlled checkbox
function TermsCheckbox() {
  const [agreed, setAgreed] = useState(false);

  return (
    <MarketRow mode="checkbox">
      <label slot="label">I agree to the terms</label>
      <MarketCheckbox
        checked={agreed}
        onChange={(e) => setAgreed(e.target.checked)}
      />
    </MarketRow>
  );
}

// Uncontrolled checkbox
<MarketCheckbox
  defaultChecked
  name="notifications"
/>

// Indeterminate (controlled) — for "select all" patterns
function SelectAll({ items, selected, onToggleAll }) {
  const allSelected = selected.length === items.length;
  const someSelected = selected.length > 0 && !allSelected;

  return (
    <MarketCheckbox
      checked={allSelected}
      indeterminate={someSelected}
      onChange={() => onToggleAll()}
    />
  );
}

// Inside a MarketRow with checkbox mode
<MarketRow
  mode="checkbox"
  selected={isSelected}
  onSelectedChange={() => toggle()}
>
  <label slot="label">Option A</label>
  <MarketCheckbox />
</MarketRow>
```

## Gotchas

- **Use `e.target.checked`** — standard React change event, NOT `e.detail.value`
- **Indeterminate is a DOM property, not an attribute** — MarketCheckbox handles this internally via refs, just pass the `indeterminate` prop
- **Don't mix controlled/uncontrolled** — don't pass both `checked` and `defaultChecked` (same for `indeterminate` / `defaultIndeterminate`)
- **Inside MarketRow**: when using `mode="checkbox"`, selection state is driven by the row's `selected` prop. The `MarketCheckbox` child is visual only — you don't need to wire up its `checked` prop separately
- **`value` defaults to `"on"`** per the HTML spec — only set it if you need a specific form submission value
