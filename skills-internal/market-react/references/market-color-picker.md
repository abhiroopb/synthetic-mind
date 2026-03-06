# MarketColorPicker

```tsx
import { MarketColorPicker } from '@your-org/market-react/trial';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `string` | — | Current color value (hex, rgb, etc.) |
| `showGradient` | `boolean` | — | Show the gradient picker area |
| `showSwatchList` | `boolean` | — | Show predefined color swatches |
| `showInput` | `boolean` | — | Show the color text input |
| `swatches` | `string[]` | — | Array of swatch color values |
| `onValueChange` | `(e: CustomEvent<{ value: string; prevValue: string }>) => void` | — | Called when color changes |

## Example

```tsx
import { MarketColorPicker } from '@your-org/market-react/trial';

function BrandColorPicker() {
  const [color, setColor] = useState('#4A90D9');

  return (
    <MarketColorPicker
      value={color}
      showGradient
      showSwatchList
      showInput
      swatches={['#FF6900', '#FCB900', '#7BDCB5', '#00D084', '#4A90D9', '#9B59B6']}
      onValueChange={(e) => setColor(e.detail.value)}
    />
  );
}
```

## Gotchas

- **CustomEvent callback** — `onValueChange` receives a CustomEvent. Use `e.detail.value` to get the new color.
- **Trial export** — import from `@your-org/market-react/trial`.
- Do NOT use `onChange` — the callback is `onValueChange`.
