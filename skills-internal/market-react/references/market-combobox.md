# MarketCombobox

```tsx
import { MarketCombobox, MarketComboboxPresentationMode } from '@squareup/market-react/trial';
```

## Props

MarketCombobox is generic: `MarketCombobox<TOption>`. It uses a discriminated union based on `multiple`:

### Shared props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `inputValue` | `string` | — | Current text in the input (required, controlled) |
| `onInputChange` | `(value: string) => void` | — | Called when input text changes (required) |
| `options` | `TOption[]` | — | Array of options to display (required) |
| `getKey` | `(option: TOption) => string` | `option.key` | Extracts unique key from an option |
| `getLabel` | `(option: TOption) => string` | `option.label` | Extracts display label from an option |
| `presentationMode` | `MarketComboboxPresentationMode` | `ON_FOCUS` | `ON_FOCUS` = show options on focus, `ON_INPUT` = show options when typing |
| `label` | `string` | — | Floating label for the input |
| `placeholder` | `string` | — | Placeholder text |
| `size` | `MarketInputProps['size']` | — | Input size |
| `disabled` | `boolean` | — | Disables the combobox |
| `invalid` | `boolean` | — | Invalid state styling |
| `isLoadingOptions` | `boolean` | — | Shows loading state when initially loading async options |
| `isLoadingMoreOptions` | `boolean` | — | Shows loading state for infinite scroll / load more |
| `trailingAccessory` | `ReactNode` | Auto clear button | Custom trailing accessory; overrides default clear button |
| `getOptionRowProps` | `(props: { option, key, label }) => Partial<MarketRowProps>` | — | Customize each option row's props (e.g. add icons, subtext) |
| `popoverPlacement` | `string` | — | Placement of the options popover |
| `popoverPortalRootId` | `string` | — | Portal root for the popover |
| `popoverClassName` | `string` | — | CSS class for the popover container |
| `aria-labelledby` | `string` | — | Accessibility label reference |
| `onPopoverOpen` | `() => void` | — | Called when the options popover opens |
| `className` | `string` | — | CSS class for the input container |

### Single select (`multiple={false}` or omitted)

| Prop | Type | Description |
|------|------|-------------|
| `value` | `TOption \| null` | Currently selected option |
| `onChange` | `(value: TOption \| null) => void` | Called when selection changes |

### Multi select (`multiple={true}`)

| Prop | Type | Description |
|------|------|-------------|
| `value` | `TOption[]` | Currently selected options |
| `onChange` | `(value: TOption[]) => void` | Called when selection changes |

## Gotchas

- **Fully controlled** — you must manage `inputValue` and `value` yourself. There is no uncontrolled mode.
- **Filter options yourself** — the component does NOT filter `options` automatically. You must filter them based on `inputValue` before passing them in.
- **`getKey` / `getLabel` default to `option.key` / `option.label`** — if your option type has `key` and `label` properties, you don't need to provide these. For other shapes, you must provide them.
- **Default clear button** — a clear button appears automatically when there's input or a selection. Pass `trailingAccessory` to override this behavior.
- **`presentationMode` controls popup timing** — use `ON_FOCUS` (default) when users need to browse options, `ON_INPUT` when they're expected to type first.
- **Multi-select renders tags** — when `multiple={true}`, selected options appear as dismissible `MarketTag` components inside the input.
- **"No results" shown automatically** — when `inputValue` is non-empty and `options` is empty (and not loading), a "No results" row is displayed.
- **NOT the same as MarketSelect** — MarketCombobox is for typeahead/autocomplete. Use MarketSelect for static dropdown selection without text input.
