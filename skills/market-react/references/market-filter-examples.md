# MarketFilter — examples and patterns

## Example

```tsx
import { MarketFilter } from '@your-org/market-react/trial';

// Single selection
function StatusFilter() {
  const [status, setStatus] = useState('active');

  return (
    <MarketFilter
      label="Status"
      selectionMode="single"
      selectedValue={status}
      selectionLabel={status}
      onSelectionChange={(e) => setStatus(e.detail.value)}
    >
      <MarketFilter.Option value="active">Active</MarketFilter.Option>
      <MarketFilter.Option value="inactive">Inactive</MarketFilter.Option>
      <MarketFilter.Option value="archived">Archived</MarketFilter.Option>
    </MarketFilter>
  );
}

// Multiple selection
function CategoryFilter() {
  const [categories, setCategories] = useState<Set<string>>(new Set(['food']));

  return (
    <MarketFilter
      label="Categories"
      selectionMode="multiple"
      selectedValues={categories}
      selectionLabel={`${categories.size} selected`}
      onSelectionChange={(e) => setCategories(e.detail.values)}
    >
      <MarketFilter.Option value="food">Food</MarketFilter.Option>
      <MarketFilter.Option value="drinks">Drinks</MarketFilter.Option>
      <MarketFilter.Option value="merchandise">Merchandise</MarketFilter.Option>
    </MarketFilter>
  );
}
```

