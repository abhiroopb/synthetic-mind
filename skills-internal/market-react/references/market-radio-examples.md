# MarketRadio — examples and patterns

## Example

```tsx
// Primary usage: inside MarketRow with mode="radio"
// Selection state is driven by the row's `selected` prop
function ShippingOptions({ selected, onSelect }) {
  return (
    <MarketList>
      <MarketRow
        mode="radio"
        selected={selected === 'standard'}
        value="standard"
        onClick={() => onSelect('standard')}
      >
        <label slot="label">Standard shipping</label>
        <p slot="subtext">5–7 business days</p>
        <MarketRadio />
      </MarketRow>
      <MarketRow
        mode="radio"
        selected={selected === 'express'}
        value="express"
        onClick={() => onSelect('express')}
      >
        <label slot="label">Express shipping</label>
        <p slot="subtext">1–2 business days</p>
        <MarketRadio />
      </MarketRow>
    </MarketList>
  );
}

// Standalone controlled usage (less common)
<MarketRadio
  checked={selectedOption === 'a'}
  name="option"
  value="a"
  onChange={(e) => {
    if (e.target.checked) setSelectedOption('a');
  }}
/>

// Standalone uncontrolled usage
<MarketRadio
  defaultChecked
  name="option"
  value="b"
/>
```

