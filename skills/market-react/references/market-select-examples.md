# MarketSelect — examples and patterns

## Example

```tsx
import { MarketSelect } from '@squareup/market-react/trial';

// Single select (controlled)
const [fruit, setFruit] = useState<string | null>(null);
<MarketSelect label="Select fruit" selectedValue={fruit} selectionMode="single" onSelectionChange={(e) => setFruit(e.detail.value)}>
  <MarketSelect.Option title="Apple" value="apple" />
  <MarketSelect.Option title="Banana" value="banana" />
  <MarketSelect.Option title="Cherry" value="cherry" />
</MarketSelect>

// Multiple select (controlled) — uses selectedValues (Set) instead of selectedValue
const [selected, setSelected] = useState<Set<string>>(new Set());
<MarketSelect label="Select toppings" selectedValues={selected} selectionMode="multiple" onSelectionChange={(e) => setSelected(e.detail.values)}>
  <MarketSelect.Option title="Cheese" value="cheese" />
  <MarketSelect.Option title="Pepperoni" value="pepperoni" />
</MarketSelect>

// With placeholder, custom selectionLabel, accessories, and disabled option
<MarketSelect label="Select country" placeholder="Choose..." selectionLabel={customLabel} selectionMode="single" onSelectionChange={handleChange}>
  <MarketSelect.Option title="US" secondaryText="United States" leadingAccessory={<FlagUS />} value="us" />
  <MarketSelect.Option title="CA" secondaryText="Canada" leadingAccessory={<FlagCA />} value="ca" />
  <MarketSelect.Option disabled title="AU (unavailable)" value="au" />
</MarketSelect>
```

## Patterns

- **Single select**: `selectionMode="single"` with `selectedValue` / `onSelectionChange`. Event detail: `{ prevValue, value }`.
- **Multiple select**: `selectionMode="multiple"` with `selectedValues` (a `Set`) / `onSelectionChange`. Event detail: `{ prevValues, values }`.
- **Compound component**: Options are `MarketSelect.Option` (subcomponent, not a separate import).
- **Controlled open**: Pass `open` prop to control dropdown visibility.
- **Custom selection label**: `selectionLabel` overrides trigger text when a value is selected.
- **Generic TValue**: `MarketSelect<string>`, `MarketSelect<number>`, etc. TypeScript infers from `value` props.
