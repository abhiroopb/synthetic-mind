# MarketButton — examples and patterns

## Example

```tsx
import { MarketButton } from '@your-org/market-react';
import { IconPlus, IconMore } from '@market/market-icons';

// Ranks and variants
<MarketButton rank="primary" size="large" onClick={handleSave}>Save changes</MarketButton>
<MarketButton destructive rank="primary" onClick={handleDelete}>Delete</MarketButton>
<MarketButton loading rank="primary" onClick={handleSubmit}>Submitting</MarketButton>

// Icon-only buttons
<MarketButton aria-label="Add item" icon={<IconPlus />} rank="secondary" onClick={handleAdd} />
<MarketButton aria-label="More options" icon={<IconMore />} rank="subtle" onClick={handleMore} /> {/* subtle: fixed size, no children */}

// Link button (renders <a>), dropdown trigger, form submit
<MarketButton href="https://example.com" rank="tertiary" target="_blank" rel="noopener noreferrer">Visit site</MarketButton>
<MarketButton aria-controls="menu-id" aria-expanded={isOpen} onClick={toggleMenu}>Options</MarketButton> {/* caret auto-added; use noCaret to hide */}
<MarketButton rank="primary" type="submit">Submit form</MarketButton>
```

## MarketButtonGroup (trial)

```tsx
import { MarketButtonGroup } from '@your-org/market-react/trial';

<MarketButtonGroup align="end" layout="side">
  <MarketButton rank="secondary">Cancel</MarketButton>
  <MarketButton rank="primary">Save</MarketButton>
</MarketButtonGroup>
```

| Prop | Type | Default | Notes |
|------|------|---------|-------|
| `align` | `'end' \| 'start'` | `'end'` | Alignment of buttons |
| `layout` | `'fill' \| 'side' \| 'split' \| 'stack'` | `'side'` | Layout arrangement |
| `maxVisibleItems` | `number` | `2` | Max visible before overflow |

## Patterns

- **Icon + text**: Pass `icon` prop alongside `children` string.
- **Icon-only (non-subtle)**: Omit `children`, pass `icon` + `aria-label`.
- **Icon-only (subtle)**: `rank="subtle"` with `icon` + `aria-label`; no `children` or `size`.
- **Link button**: Set `href` to render as `<a>`. `type` prop not allowed.
- **Dropdown trigger**: `aria-expanded` + `aria-controls`; caret auto-added. Use `noCaret` to hide.
- **Form submit**: `type="submit"` (default is `'button'`).
