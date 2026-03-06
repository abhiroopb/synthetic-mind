# MarketToast — examples and patterns

## Example

```tsx
import { MarketToastProvider, useMarketToast } from '@squareup/market-react/trial';
import { MarketButton, MarketLink } from '@squareup/market-react';

// Wrap app with provider
function App() {
  return (
    <MarketToastProvider>
      <SaveForm />
    </MarketToastProvider>
  );
}

function SaveForm() {
  const { showToast, removeToast, removeAll } = useMarketToast();

  const handleSave = async () => {
    try {
      await saveData();
      showToast({
        message: 'Changes saved successfully',
        variant: 'success',
        duration: 'short',
      });
    } catch {
      const toastId = showToast({
        message: 'Failed to save changes',
        variant: 'critical',
        persistent: true,
        actions: (
          <MarketLink
            onClick={handleSave}
          >
            Retry
          </MarketLink>
        ),
      });
      // Can remove programmatically later: removeToast(toastId)
    }
  };

  return (
    <MarketButton
      onClick={handleSave}
    >
      Save
    </MarketButton>
  );
}
```

