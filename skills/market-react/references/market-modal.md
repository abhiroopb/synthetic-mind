# MarketModal

```tsx
import { MarketModal } from '@squareup/market-react/trial';
```

## Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `type` | `'full' \| 'partial' \| 'dialog' \| 'blade' \| 'sheet'` | **required** | Modal variant |
| `onClose` | `() => void` | — | Callback when modal is closed |
| `persistent` | `boolean` | `false` | Prevents close on veil click or Escape key |
| `noVeil` | `boolean` | `false` | Removes the backdrop overlay |
| `portalRootId` | `string` | — | ID of DOM element to portal into |
| `zIndex` | `number` | `1000` | z-index of the modal |
| `contentWidth` | `'regular' \| 'wide' \| 'fluid'` | `'regular'` | Content width (full modals only) |
| `aria-label` | `string` | — | Accessible name when no header is present |

## Gotchas

| Wrong | Correct | Why |
|-------|---------|-----|
| `<MarketModalPartial>` / `<MarketModalFull>` / `<MarketDialog>` | `<MarketModal type="partial">` | Single component with `type` prop, not separate components |
| `<MarketModal isOpen={show}>` | `{show && <MarketModal>}` | No `isOpen` prop — renders when mounted, unmount to hide |
| `onDismiss={fn}` | `onClose={fn}` | Callback is `onClose`, not `onDismiss` |
| `contentWidth` on `type="partial"` | `contentWidth` on `type="full"` only | `contentWidth` only applies to full modals |
| Missing `aria-label` on dialog without header | Add `aria-label="..."` | Required for accessibility when no MarketHeader is present |
