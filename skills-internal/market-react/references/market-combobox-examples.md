# MarketCombobox — examples and patterns

## Example

```tsx
// Basic single select with filtering
const [inputValue, setInputValue] = useState('');
const [selected, setSelected] = useState<Fruit | null>(null);
const filtered = allFruits.filter((f) => f.label.toLowerCase().includes(inputValue.toLowerCase()));

<MarketCombobox
  label="Pick a fruit"
  inputValue={inputValue}
  options={filtered}
  value={selected}
  onInputChange={setInputValue}
  onChange={setSelected}
/>

// Multi select with custom option rows
<MarketCombobox
  multiple
  label="Tags"
  inputValue={inputValue}
  options={filteredTags}
  value={selectedTags}
  presentationMode={MarketComboboxPresentationMode.ON_INPUT}
  getOptionRowProps={({ option }) => ({ leadingAccessory: <ColorDot color={option.color} />, subtext: option.description })}
  onInputChange={setInputValue}
  onChange={setSelectedTags}
/>

// Custom type with getKey/getLabel + async loading
<MarketCombobox<User>
  label="Search users"
  inputValue={query}
  options={users}
  value={selectedUser}
  getKey={(u) => u.id}
  getLabel={(u) => u.name}
  getOptionRowProps={({ option }) => ({ subtext: option.email })}
  isLoadingOptions={isLoading}
  onInputChange={(v) => { setQuery(v); debouncedSearch(v); }}
  onChange={setSelectedUser}
/>
```
