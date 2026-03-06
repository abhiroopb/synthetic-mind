# MarketDatePicker — examples and patterns

## Example

```tsx
// Single date selection
function SingleDatePicker() {
  const [date, setDate] = useState<Date | null>(null);

  return (
    <MarketDatePicker
      selectedDate={date}
      timeframe="past"
      presets={['today', 'yesterday', 'this-week', 'last-month']}
      displayMenu
      onSelectedDateChange={(newDate) => setDate(newDate)}
    />
  );
}

// Date range selection
function DateRangePicker() {
  const [range, setRange] = useState<{ start: Date; end: Date } | null>(null);

  return (
    <MarketDatePicker
      selectionMode="range"
      selectedDateRange={range}
      timeframe="past"
      displayMenu
      withInputs="date"
      onSelectedDateRangeChange={(newRange) => setRange(newRange)}
    />
  );
}

// With custom presets
function CustomPresetPicker() {
  const [date, setDate] = useState<Date | null>(null);

  return (
    <MarketDatePicker
      selectedDate={date}
      displayMenu
      presets={[
        'today',
        'yesterday',
        { id: 'fiscal-year-start', label: 'Fiscal year start' },
        { id: 'company-founding', label: 'Company founding' },
      ]}
      onSelectedDateChange={(newDate) => setDate(newDate)}
      onPresetChange={(presetId) => {
        if (presetId === 'fiscal-year-start') {
          setDate(new Date(2025, 0, 1));
        } else if (presetId === 'company-founding') {
          setDate(new Date(2009, 1, 1));
        }
      }}
    />
  );
}

// Disable weekends
<MarketDatePicker
  selectedDate={date}
  isDateDisabled={(day) => day.getDay() === 0 || day.getDay() === 6}
  onSelectedDateChange={setDate}
/>
```

