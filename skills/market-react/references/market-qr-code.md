# MarketQrCode

## Import

```tsx
import { MarketQrCode } from '@squareup/market-react/trial';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `content` | `string` | **required** | URL or data to encode in the QR code |
| `border` | `boolean` | `false` | Adds a 6-pixel border with background |
| `monochrome` | `boolean` | `false` | Renders in black and white only |
| `size` | `number` | — | Pixel dimensions (width and height) of the QR code |

## Example

```tsx
import { MarketQrCode } from '@squareup/market-react/trial';

// Basic QR code
<MarketQrCode content="https://squareup.com/store/my-shop" />

// QR code with border and fixed size
<MarketQrCode
  border
  content="https://squareup.com/pay/abc123"
  size={200}
/>

// Monochrome QR code for print
<MarketQrCode
  border
  monochrome
  content="https://squareup.com/appointments/book/xyz"
  size={300}
/>
```

## Gotchas

- **`content` is required**: The component won't render without it.
- **Uses @square/qrcode-encoder internally**: You don't need to install or import the encoder separately.
- **`border` adds padding + background**: Useful for placing QR codes on non-white backgrounds so they remain scannable.
- **`size` is in pixels**: Controls both width and height equally (QR codes are always square).
