# MarketSlider

```tsx
import { MarketSlider } from '@squareup/market-react/trial';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `number` | — | Current slider value (controlled) |
| `min` | `number` | — | Minimum value |
| `max` | `number` | — | Maximum value |
| `step` | `number` | — | Step increment |
| `disabled` | `boolean` | `false` | Disable the slider |
| `onChange` | `ChangeEventHandler<HTMLInputElement>` | — | Standard React change handler |

## Example

```tsx
import { MarketSlider } from '@squareup/market-react/trial';

function VolumeControl() {
  const [volume, setVolume] = useState(50);

  return (
    <MarketSlider
      value={volume}
      min={0}
      max={100}
      step={1}
      onChange={(e) => setVolume(Number(e.target.value))}
    />
  );
}
```

## Gotchas

- **Standard React `onChange`** — uses `e.target.value`, NOT a CustomEvent. Convert to number with `Number(e.target.value)`.
- **Always controlled** — always provide `value`. There is no uncontrolled / `defaultValue` mode.
- **Trial export** — import from `@squareup/market-react/trial`.
