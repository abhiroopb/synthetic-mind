---
Skill name: market-react
Skill description: >-
roles:
  - frontend
  Reference docs for a design system's React UI components.
  Use when building, implementing, debugging, styling, migrating, testing,
  or reviewing React components that use design system components
  (Button, Row, Select, Modal, Table, Input, etc.) in a web application.
---

# Design System React Components

This skill covers the **React components** from the design system UI library.

## Package selection

| Package | Status | Use when |
|---------|--------|----------|
| `@your-org/design-system-react` | **React-native** (this skill) | New development, preferred |
| `@design-system/react` | Web component wrappers | Legacy code, migration needed |

This skill documents `@your-org/design-system-react`. For converting from the legacy package, see the migration skill.

## Component references

Load `references/component-index.md` to find the right reference file for any component. Key references:

- `references/pitfalls.md` — Common mistakes and wrong→correct patterns
- `references/button.md`, `input.md`, `select.md`, `modal.md` — Most-used components
- 39 reference docs total covering all design system React components

## Quick reference

### Import source

```tsx
// Stable components
import { Button, Row, Input, ... } from '@your-org/design-system-react';

// Trial components (may have breaking API changes)
import { Modal, Table, Select, ... } from '@your-org/design-system-react/trial';
```

### Stable vs trial

Stable components are exported from `@your-org/design-system-react`. Trial components are exported from `@your-org/design-system-react/trial` and may have breaking API changes.

**Stable**: Accessory, Banner, Button, Checkbox, Divider, Field, InlineStatus, Input, Link, LinkGroup, Pill, Radio, Row, SkeletonLoader, Spinner, Tag, Theme, Toggle

**Trial**: Accordion, ButtonGroup, Card, ChoiceButton, CodeDisplay, CodeInput, Collection, ColorPicker, Combobox, DatePicker, Dropdown, EmptyState, Filter, Grid, Header, Footer, List, Modal, PagingTabs, Popover, ProgressMeter, QrCode, ScrollArea, SegmentedControl, Select, Slider, Stepper, Table, Text, Toast, Toggletip, Tooltip

### Critical gotchas

See `references/pitfalls.md` for the full list of common mistakes and wrong→correct patterns.
