# MarketStepper

```tsx
import { MarketStepper } from '@squareup/market-react/trial';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `number` | — | Current value |
| `min` | `number` | — | Minimum allowed value |
| `max` | `number` | — | Maximum allowed value |
| `step` | `number` | `1` | Increment/decrement step |
| `disabled` | `boolean` | `false` | Disable the stepper |
| `invalid` | `boolean` | `false` | Show invalid state |
| `readOnly` | `boolean` | `false` | Read-only mode |
| `placeholder` | `string` | — | Placeholder text |
| `id` | `string` | — | Element ID |
| `name` | `string` | — | Form field name |
| `onValueChange` | `(value: number) => void` | — | Called with the new number value directly |

## Example

```tsx
import { MarketStepper } from '@squareup/market-react/trial';

function QuantitySelector() {
  const [quantity, setQuantity] = useState(1);

  return (
    <MarketStepper
      value={quantity}
      min={1}
      max={99}
      step={1}
      onValueChange={(value) => setQuantity(value)}
    />
  );
}
```

## Gotchas

- **Direct number callback** — `onValueChange` receives the new number directly, NOT an event or CustomEvent. Use `(value) => setState(value)`, not `(e) => ...`.
- **Buttons auto-disable** — increment/decrement buttons automatically disable when `value` reaches `min` or `max`.
- **Trial export** — import from `@squareup/market-react/trial`.
