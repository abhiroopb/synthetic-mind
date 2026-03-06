# MarketAccordion — examples and patterns

## Example

```tsx
import { MarketAccordion, MarketAccordionGroup } from '@squareup/market-react/trial';

// Single uncontrolled accordion
<MarketAccordion
  defaultExpanded
  header="Order details"
>
  <p>Order #1234 — 3 items</p>
</MarketAccordion>

// Controlled accordion
const [expanded, setExpanded] = useState(false);

<MarketAccordion
  expanded={expanded}
  header="Advanced settings"
  id="advanced"
  size="small"
  onExpandedChange={(_id, isExpanded) => setExpanded(isExpanded)}
>
  <p>Configuration options here</p>
</MarketAccordion>

// Accordion group (multiple, coordinated)
const [expandedItems, setExpandedItems] = useState<string[]>(['faq-1']);

<MarketAccordionGroup
  expandedItems={expandedItems}
  onExpandedItemsChange={setExpandedItems}
>
  <MarketAccordion
    header="What is Market?"
    id="faq-1"
  >
    <p>Market is Block's design system.</p>
  </MarketAccordion>
  <MarketAccordion
    header="How do I get started?"
    id="faq-2"
  >
    <p>Install @squareup/market-react.</p>
  </MarketAccordion>
  <MarketAccordion
    header="Is it free?"
    id="faq-3"
  >
    <p>Yes, for internal use.</p>
  </MarketAccordion>
</MarketAccordionGroup>
```

