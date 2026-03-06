# MarketField — examples and patterns

## Example

```tsx
import { MarketField } from '@squareup/market-react';

// Basic with helper text
<MarketField label="Full name" helperText="Enter your legal name" value={name} onChange={(e) => setName(e.target.value)} />

// With error message (auto-invalidates)
<MarketField label="Full name" errorMessage={nameError} value={name} onChange={(e) => setName(e.target.value)} />

// Multiline with character limit, helper, and error
<MarketField
  label="Bio"
  type="multiline"
  rows={4}
  charLimit={280}
  helperText="Tell us about yourself"
  errorMessage={bioError}
  value={bio}
  onChange={(e) => setBio(e.target.value)}
/>

// Other input types
<MarketField label="Email" type="email" value={email} onChange={(e) => setEmail(e.target.value)} />
<MarketField label="Password" type="password" helperText="Min 8 characters" value={pw} onChange={(e) => setPw(e.target.value)} />

// Override auto-invalid; uncontrolled with char limit
<MarketField label="Name" errorMessage="Has issues" invalid={false} value={name} onChange={(e) => setName(e.target.value)} />
<MarketField label="Short note" charLimit={50} defaultValue="Hello world" />
```

## Patterns

- **Error**: `errorMessage` shows red error and auto-sets `invalid={true}`. Override with `invalid={false}`.
- **Char counter**: `charLimit` shows "X/Y" counter; auto-invalidates when exceeded.
- **Stacking**: error, char count, and helper text stack vertically in that order.
