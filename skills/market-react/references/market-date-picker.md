# MarketDatePicker

```tsx
import { MarketDatePicker } from '@your-org/market-react/trial';
```

## Props

MarketDatePicker uses a discriminated union based on `selectionMode`:

### Shared props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `selectionMode` | `'single' \| 'range'` | `'single'` | Determines single date or date range selection |
| `presets` | `ReadonlyArray<BuiltInPreset \| CustomPreset>` | All built-in | Presets shown in the menu. Built-in: `'today'`, `'yesterday'`, `'this-week'`, `'last-week'`, `'this-month'`, `'last-month'`, `'this-year'`. Custom: `{ id, label }` |
| `timeframe` | `'past' \| 'present' \| 'future'` | — | `'past'` disables future dates, `'future'` disables past dates |
| `weekStartsOn` | `'sunday' \| 'monday' \| ... \| 'saturday'` | Locale-based | Override the first day of the week |
| `isDateDisabled` | `(day: Date) => boolean` | — | Custom function to disable specific dates |
| `locale` | `string` | `navigator.language` | Locale for date formatting |
| `displayedDate` | `Date` | — | Initially displayed month/year in the calendar |
| `displayMenu` | `boolean` | — | Whether to show the preset menu |
| `mobileMenuPosition` | `'top' \| 'bottom'` | `'top'` | Position of preset menu on mobile |
| `withInputs` | `'' \| 'date' \| 'date-and-time'` | `''` | Enables input fields: `''` = none, `'date'` = date only, `'date-and-time'` = date and time |
| `onPresetChange` | `(presetId: string) => void` | — | Called when a preset is selected |
| `className` | `string` | — | Additional CSS class |

### Single mode props (`selectionMode='single'` or omitted)

| Prop | Type | Description |
|------|------|-------------|
| `selectedDate` | `Date \| null` | Currently selected date (required) |
| `onSelectedDateChange` | `(date: Date \| null) => void` | Called when the selected date changes |

### Range mode props (`selectionMode='range'`)

| Prop | Type | Description |
|------|------|-------------|
| `selectedDateRange` | `{ start: Date, end: Date } \| null` | Currently selected date range (required) |
| `onSelectedDateRangeChange` | `(range: { start: Date, end: Date } \| null) => void` | Called when the selected range changes |

## Gotchas

- **Discriminated union** — you cannot mix single and range props. If `selectionMode='range'`, use `selectedDateRange` / `onSelectedDateRangeChange`. If `selectionMode='single'` (or omitted), use `selectedDate` / `onSelectedDateChange`. TypeScript enforces this with `never` types.
- **`selectedDate` is required in single mode** — pass `null` for no selection, not `undefined`
- **Custom presets need `onPresetChange`** — built-in presets (like `'today'`) are handled automatically. Custom presets (`{ id, label }`) only fire `onPresetChange`; you must update the date/range yourself.
- **`withInputs`** — empty string `''` (default) disables inputs. Use `'date'` or `'date-and-time'` to enable them.
- **`BUILT_IN_PRESETS` constant is available** — import `{ BUILT_IN_PRESETS }` from `@your-org/market-react/trial` for type-safe preset strings (`BUILT_IN_PRESETS.TODAY`, `BUILT_IN_PRESETS.THIS_WEEK`, etc.)
- **`MENU_SLOT_NAMES` and `MarketDatePickerPresetLabels` are deprecated** — use `presets` array and `BUILT_IN_PRESETS` instead
