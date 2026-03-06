# MarketCodeInput — examples and patterns

## Example

```tsx
// 6-digit verification code in two groups
function VerificationCodeInput() {
  const [code, setCode] = useState('');
  const [error, setError] = useState('');

  return (
    <MarketCodeInput
      format="*** ***"
      helperText="Enter the code sent to your email"
      errorMessage={error}
      invalid={!!error}
      value={code}
      onChange={(e) => {
        setCode(e.target.value);
        setError('');
      }}
      onComplete={(value) => {
        // value is clean, e.g. "123456" (no spaces)
        verifyCode(value);
      }}
    />
  );
}

// 4-digit PIN entry
<MarketCodeInput
  masked
  type="number"
  format="****"
  onComplete={(pin) => submitPin(pin)}
/>

// Text-based code (e.g. gift card)
<MarketCodeInput
  type="text"
  format="**** **** ****"
  value={giftCode}
  onChange={(e) => setGiftCode(e.target.value)}
/>

// Showing a valid state with checkmark
<MarketCodeInput
  valid
  format="******"
  value={confirmedCode}
/>
```

