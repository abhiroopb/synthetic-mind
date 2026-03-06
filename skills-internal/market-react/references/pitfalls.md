# Common pitfalls

A comprehensive reference of the most common mistakes when using `@squareup/market-react`.

## Import paths

| Wrong | Correct |
|-------|---------|
| `import { ... } from '@market/react'` | `import { ... } from '@squareup/market-react'` |
| `import { MarketModal } from '@squareup/market-react'` | `import { MarketModal } from '@squareup/market-react/trial'` |

`@market/react` is the legacy web component wrapper package. Always use `@squareup/market-react` for React-native components. Trial components must be imported from `@squareup/market-react/trial`.

## MarketButton

| Wrong | Correct |
|-------|---------|
| `isLoading={true}` | `loading={true}` |
| `variant="destructive"` | `destructive` (boolean prop) |
| `variant="primary"` | `rank="primary"` |

## MarketRow

| Wrong | Correct |
|-------|---------|
| `<MarketRow><span slot="label">Title</span></MarketRow>` | `<MarketRow title="Title" />` |
| `<MarketRow><span slot="control">...</span></MarketRow>` | `<MarketRow secondaryText="..." />` |
| `<MarketRow>children content</MarketRow>` | `<MarketRow title="..." secondaryText="..." />` |

MarketRow uses **named props** (`title`, `secondaryText`), NOT slot-based patterns. **Children are never used** for content — all content goes through props.

## MarketModal

| Wrong | Correct |
|-------|---------|
| `<MarketModal isOpen={showModal}>` | `{showModal && <MarketModal>}` |
| `onDismiss={handleClose}` | `onClose={handleClose}` |

MarketModal has **no `isOpen` prop**. Render it conditionally. The dismiss callback is `onClose`, not `onDismiss`.

## MarketHeader

| Wrong | Correct |
|-------|---------|
| `showNavigation` | `leadingActions={<button>Back</button>}` |
| `onNavigate={handleBack}` | `leadingActions` / `trailingActions` props |

MarketHeader uses `leadingActions` and `trailingActions` render props, NOT `showNavigation` / `onNavigate`.

## MarketField

| Wrong | Correct |
|-------|---------|
| `<MarketField invalid><span slot="error">Bad</span></MarketField>` | `<MarketField errorMessage="Bad" />` |

Use the `errorMessage` prop, NOT slot-based errors. The `invalid` state is derived from the presence of `errorMessage`.

See also: [pitfalls-advanced.md](pitfalls-advanced.md) for MarketToast, MarketPill, MarketBanner, MarketSelect, and event handler patterns.

## Quick checklist

Before submitting code using Market React components, verify:

1. ✅ Importing from `@squareup/market-react` (stable) or `@squareup/market-react/trial` (trial)
2. ✅ Using correct prop names (not legacy web component names)
3. ✅ Using correct event handler signature for the specific component
4. ✅ MarketRow uses props, not slots or children
5. ✅ MarketModal rendered conditionally, not with `isOpen`
6. ✅ MarketPill uses `label` prop, not children
7. ✅ MarketBanner uses `dismissible` (not `dismissable`) and `status` (not `variant`)
