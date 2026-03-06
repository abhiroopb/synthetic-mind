# MarketToggle

```tsx
import { MarketToggle } from '@your-org/market-react';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `checked` | `boolean` | — | Current toggled state (controlled mode) |
| `defaultChecked` | `boolean` | — | Initial toggled state (uncontrolled mode) |
| `disabled` | `boolean` | — | Prevents interaction, applies disabled styling |
| `id` | `string` | — | HTML id, used for associating with a label |
| `name` | `string` | — | HTML name for form submissions |
| `value` | `string` | `"on"` | Value submitted in form data |
| `onChange` | `ChangeEventHandler<HTMLInputElement>` | — | Handles toggled state changes |

Also accepts all `React.InputHTMLAttributes<HTMLInputElement>` except `type`.

## Example

```tsx
// Controlled toggle
function NotificationSetting() {
  const [enabled, setEnabled] = useState(false);

  return (
    <MarketRow mode="toggle">
      <label slot="label">Enable notifications</label>
      <p slot="subtext">Receive email alerts for new orders</p>
      <MarketToggle
        checked={enabled}
        onChange={(e) => setEnabled(e.target.checked)}
      />
    </MarketRow>
  );
}

// Uncontrolled toggle
<MarketToggle
  defaultChecked
  name="dark-mode"
/>

// Standalone toggle with id for external label
<label htmlFor="auto-save">Auto-save</label>
<MarketToggle
  id="auto-save"
  checked={autoSave}
  onChange={(e) => setAutoSave(e.target.checked)}
/>
```

## Gotchas

- **Use `e.target.checked`** — standard React change event, NOT `e.detail.value`
- **Don't mix controlled/uncontrolled** — don't pass both `checked` and `defaultChecked`
- **Inside MarketRow**: when using `mode="toggle"`, place the `<MarketToggle />` as a child of `<MarketRow>`. Selection state is typically driven by the toggle's own `checked`/`onChange` props (unlike checkbox/radio rows where the row's `selected` prop drives state)
- **`value` defaults to `"on"`** per the HTML spec — only set it if you need a specific form submission value
