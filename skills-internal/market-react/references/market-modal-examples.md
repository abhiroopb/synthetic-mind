# MarketModal — examples and patterns

## Example

```tsx
import { MarketModal, MarketHeader, MarketFooter, MarketButton } from '@squareup/market-react/trial';

// Partial modal with header actions and footer
function EditItemModal({ item, onSave, onCancel }: Props) {
  return (
    <MarketModal type="partial" onClose={onCancel}>
      <MarketHeader
        title="Edit item"
        leadingActions={<MarketButton rank="secondary" onClick={onCancel}>Cancel</MarketButton>}
        trailingActions={<MarketButton onClick={onSave}>Save</MarketButton>}
      />
      <main><p>{item.name}</p></main>
      <MarketFooter>
        <MarketButton onClick={onSave}>Save</MarketButton>
      </MarketFooter>
    </MarketModal>
  );
}

// Control visibility via conditional rendering
const [showModal, setShowModal] = useState(false);
<MarketButton onClick={() => setShowModal(true)}>Open</MarketButton>
{showModal && <EditItemModal item={item} onSave={handleSave} onCancel={() => setShowModal(false)} />}

// Full-screen modal with wide content
<MarketModal type="full" contentWidth="wide" onClose={onClose}>
  <MarketHeader title="Inventory" />
  <main>{/* content */}</main>
</MarketModal>

// Persistent confirmation dialog
<MarketModal persistent type="dialog" aria-label="Confirm deletion" onClose={onClose}>
  <MarketHeader title="Delete item?" />
  <main><p>This action cannot be undone.</p></main>
  <MarketFooter>
    <MarketButton rank="secondary" onClick={onClose}>Cancel</MarketButton>
    <MarketButton destructive onClick={onDelete}>Delete</MarketButton>
  </MarketFooter>
</MarketModal>

// Blade (side panel)
<MarketModal type="blade" onClose={onClose}>
  <MarketHeader title="Details" />
  <main>{/* side panel content */}</main>
</MarketModal>
```

## Patterns

- **Types**: `"partial"` (default sheet), `"full"` (full-screen), `"dialog"` (centered), `"blade"` (side panel).
- **Persistent**: `persistent` prevents closing on backdrop click / Escape.
- **Content width**: `contentWidth="wide"` for full-screen modals with wide content.
- **Visibility**: Control via conditional rendering (`{show && <MarketModal>}`), not a prop.
