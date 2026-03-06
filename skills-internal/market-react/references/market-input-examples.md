# MarketInput — examples and patterns

## Example

```tsx
import { MarketInput } from '@your-org/market-react';
import { IconDollar } from '@market/market-icons';

// Basic text, number, password (password auto-renders visibility toggle)
<MarketInput label="Full name" value={name} onChange={(e) => setName(e.target.value)} />
<MarketInput label="Amount" type="number" value={amount} onChange={(e) => setAmount(e.target.value)} />
<MarketInput label="Password" type="password" value={password} onChange={(e) => setPassword(e.target.value)} />

// Multiline textarea
<MarketInput label="Description" type="multiline" rows={4} value={description} onChange={(e) => setDescription(e.target.value)} />

// Search input (auto-renders magnifying glass + clear button)
<MarketInput label="Search items" type="search" value={query} onChange={(e) => setQuery(e.target.value)} onCleared={() => setQuery('')} />
<MarketInput compact label="Search" type="search" value={query} onChange={(e) => setQuery(e.target.value)} onCleared={() => setQuery('')} /> {/* compact variant */}

// With accessory, invalid state, small size, uncontrolled, and ref
<MarketInput label="Price" leadingAccessory={<IconDollar />} type="number" value={price} onChange={(e) => setPrice(e.target.value)} />
<MarketInput invalid label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
<MarketInput label="Zip code" size="small" value={zip} onChange={(e) => setZip(e.target.value)} />
<MarketInput defaultValue="hello" label="Notes" /> {/* uncontrolled */}

const inputRef = useRef<MarketInputElement>(null);
<MarketInput ref={inputRef} label="Focus me" />
```

## Patterns

- **Controlled**: Pass `value` + `onChange`. Warns if mixed with uncontrolled.
- **Uncontrolled**: Pass `defaultValue` only.
- **Floating label**: `label` floats above input when focused or has value.
- **Search**: `type="search"` auto-renders magnifying glass + clear button. Overrides `leadingAccessory`.
- **Password**: `type="password"` auto-renders visibility toggle as trailing accessory.
- **Textarea**: `type="multiline"` renders `<textarea>`. Pass `rows` etc.
- **Accessibility**: If no `label`, provide `aria-label`. Component warns if neither is set.
