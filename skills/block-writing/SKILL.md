---
name: brand-voice-writing
description: Use when writing, reviewing, drafting, editing, auditing, or revising product content across multiple brand lines. Covers UI copy, marketing, support articles, transactional communications, and legal copy. Applies brand voice principles and accessibility standards.
metadata:
  author: anonymous
  version: "1.1.0"
  status:
---

# Brand Voice Writing Standards

This skill helps you create and review content that aligns with your brand voice and meets standards for clarity, accessibility, and user experience.

**STOP** — Before proceeding, confirm:
1. **Which product?** (Product A, Product B, Product C, etc.) — voice, terminology, and component rules differ by product
2. **What content type?** (UI copy, marketing, support, legal) — determines which reference files apply

If either is unclear, ask before writing.

## Workflow

For any content task, work through these steps:

- [ ] **Identify the context** — Product line, content type (UI, marketing, support, legal), audience (consumer or merchant), and component if applicable

- [ ] **Apply brand voice principles** — Apply all four in order:
  - **Crisp**: Lead with what matters most; cut clutter
  - **Self-assured**: Direct, declarative language; skip hype
  - **Fluent**: Adapt tone to the moment; sound like a real person
  - **Upfront**: Start with the truth; don't bury important information
  - [See [references/voice-principles.md](references/voice-principles.md) for tactics and examples]

- [ ] **Apply function-specific standards** — Choose based on content type:
  - *UI/Product copy*: Sentence case, active voice, contractions; error messages follow problem → context → solution ([references/style-voice-pov.md](references/style-voice-pov.md))
  - *Component content*: Product A → [arcade-universal-standards.md](references/arcade-universal-standards.md); Product B → [square-voice-standards.md](references/square-voice-standards.md); decision support → [decision-trees-product-context.md](references/decision-trees-product-context.md)
  - *Marketing*: see Marketing Content routing section below for product-specific growth, marketing, and BNPL files
  - *Support*: [references/support-writing-principles.md](references/support-writing-principles.md) + relevant article guide

- [ ] **Verify terminology** — Product names must match exactly; use current approved terms ([references/terminology-brand-b.md](references/terminology-brand-b.md))

- [ ] **Check accessibility** — 7th-8th grade reading level, clear hierarchy, text alternatives for visual elements, no color-only meaning ([references/accessibility-readability.md](references/accessibility-readability.md))

## Reference File Routing

Use these trigger-based rules to load the appropriate reference files:

### UI Copy and Patterns

#### WHEN writing button labels or CTAs:
→ Load [references/patterns-buttons.md](references/patterns-buttons.md)

#### WHEN writing error messages:
→ Load [references/patterns-errors.md](references/patterns-errors.md)

#### WHEN writing form field labels, helper text, or validation messages:
→ Load [references/patterns-forms.md](references/patterns-forms.md)

#### WHEN writing modal content:
→ Load [references/content-patterns-modals.md](references/content-patterns-modals.md)

#### WHEN writing toast, empty state, loading, or success content:
→ Load [references/patterns-states.md](references/patterns-states.md)

#### WHEN writing transactional email subject lines or body structure:
→ Load [references/patterns-email-voice.md](references/patterns-email-voice.md)

### Style and Mechanics

#### WHEN questions about capitalization or sentence case:
→ Load [references/style-capitalization.md](references/style-capitalization.md)

#### WHEN questions about voice, active voice, contractions, point of view, or reading level:
→ Load [references/style-voice-pov.md](references/style-voice-pov.md)

#### WHEN questions about punctuation (periods, commas, em dashes, exclamation marks):
→ Load [references/style-punctuation.md](references/style-punctuation.md)

#### WHEN questions about numbers, dates, times, phone numbers, or text formatting:
→ Load [references/style-numbers-formatting.md](references/style-numbers-formatting.md)

### Voice and Product

#### WHEN user asks about or emphasizes voice principles (crisp, self-assured, fluent, upfront):
→ Load [references/voice-principles.md](references/voice-principles.md)

#### WHEN user mentions Product A (consumer product):
→ Load [references/product-voice-brand-b.md](references/product-voice-brand-b.md)

#### WHEN user mentions Product B (merchant product):
→ Load [references/product-voice-square.md](references/product-voice-square.md)

#### WHEN user mentions other product lines:
→ Load [references/product-voice-others.md](references/product-voice-others.md)

### Accessibility

#### WHEN questions about screen readers, alt text, or link text:
→ Load [references/accessibility-screen-readers.md](references/accessibility-screen-readers.md)

#### WHEN questions about reading level, heading hierarchy, or color:
→ Load [references/accessibility-readability.md](references/accessibility-readability.md)

#### WHEN questions about inclusive language, gender-neutral terms, or biased language:
→ Load [references/accessibility-inclusive-language.md](references/accessibility-inclusive-language.md)

#### WHEN reviewing content patterns for accessibility or need testing guidance:
→ Load [references/accessibility-patterns-testing.md](references/accessibility-patterns-testing.md)

### Terminology

#### WHEN questions about consumer product names, feature names, or money movement terms:
→ Load [references/terminology-brand-b.md](references/terminology-brand-b.md)

#### WHEN questions about merchant product names or audience terms:
→ Load [references/terminology-square.md](references/terminology-square.md)

#### WHEN questions about other product lines or corporate brand names:
→ Load [references/terminology-afterpay-other.md](references/terminology-afterpay-other.md)

#### WHEN checking for deprecated or incorrect terms:
→ Load [references/terminology-deprecated.md](references/terminology-deprecated.md)

### Component Content

#### WHEN working on consumer product / Arcade Design System components:
- **Universal rules** → [arcade-universal-standards.md](references/arcade-universal-standards.md)
- **Buttons, forms, selection controls** → [arcade-buttons-forms.md](references/arcade-buttons-forms.md)
- **Cells, modals, toasts** → [arcade-cells-modals-toasts.md](references/arcade-cells-modals-toasts.md)
- **Product voice + QA checklist** → [arcade-product-quality.md](references/arcade-product-quality.md)

#### WHEN working on merchant product / Market Design System components:
- **Voice + universal standards** → [square-voice-standards.md](references/square-voice-standards.md)
- **Buttons, forms, selection controls, dialogs, toasts** → [square-components.md](references/square-components.md)
- **Business patterns, QA, cross-product integration** → [square-business-patterns.md](references/square-business-patterns.md)

#### WHEN need decision support for choosing component types:
- **Buttons and toasts** → [decision-trees-buttons-toasts.md](references/decision-trees-buttons-toasts.md)
- **Content length** → [decision-trees-content-length.md](references/decision-trees-content-length.md)
- **Form inputs** → [decision-trees-forms.md](references/decision-trees-forms.md)
- **Selection controls** → [decision-trees-selection.md](references/decision-trees-selection.md)
- **Modals** → [decision-trees-modals.md](references/decision-trees-modals.md)
- **Error messages** → [decision-trees-errors.md](references/decision-trees-errors.md)
- **Product context (choosing between product lines)** → [decision-trees-product-context.md](references/decision-trees-product-context.md)

#### WHEN need component content templates or examples:
- **Buttons** → [content-patterns-buttons.md](references/content-patterns-buttons.md)
- **Form inputs** → [content-patterns-forms.md](references/content-patterns-forms.md)
- **Selection controls** → [content-patterns-selection-controls.md](references/content-patterns-selection-controls.md)
- **Modals (confirmation, error, info)** → [content-patterns-modals.md](references/content-patterns-modals.md)
- **Toasts** → [content-patterns-toasts.md](references/content-patterns-toasts.md)
- **Error message patterns** → [content-patterns-errors.md](references/content-patterns-errors.md)
- **Success messages and product voice** → [content-patterns-success-voice.md](references/content-patterns-success-voice.md)

#### WHEN need character limits for a specific component:
→ Load [references/quick-ref-limits.md](references/quick-ref-limits.md)

#### WHEN reviewing component content for quality or common mistakes:
→ Load [references/quick-ref-qa.md](references/quick-ref-qa.md)

### Marketing Content

#### WHEN working on consumer product email campaigns:
→ Load [references/growth-writing-email.md](references/growth-writing-email.md)

#### WHEN working on consumer product push notifications or ads:
→ Load [references/growth-writing-push-ads.md](references/growth-writing-push-ads.md)

#### WHEN working on consumer product growth messaging — banking features (banking, direct deposit, overdraft, savings, ATM):
→ Load [references/growth-messaging-banking.md](references/growth-messaging-banking.md)

#### WHEN working on consumer product growth messaging — card, offers, or rewards:
→ Load [references/growth-messaging-card.md](references/growth-messaging-card.md)

#### WHEN working on consumer product growth messaging — investing, payments, or security:
→ Load [references/growth-messaging-investing-pay.md](references/growth-messaging-investing-pay.md)

#### WHEN working on merchant product marketing — grammar, style, or mechanics (punctuation, numbers, dates):
→ Load [references/square-style-grammar.md](references/square-style-grammar.md)

#### WHEN working on merchant product marketing — content guidelines, readability, or formatting:
→ Load [references/square-style-content.md](references/square-style-content.md)

#### WHEN working on merchant product marketing — inclusivity, technology terms, or localization:
→ Load [references/square-style-inclusivity.md](references/square-style-inclusivity.md)

#### WHEN working on merchant product marketing — specific word choices or term spellings:
→ Load [references/square-style-dictionary.md](references/square-style-dictionary.md) (key terms, audience terms, words to avoid)
→ Load [references/square-style-specific-terms.md](references/square-style-specific-terms.md) (A–Z spelling and capitalization reference)

#### WHEN working on BNPL product marketing — brand strategy or naming:
→ Load [references/afterpay-brand-strategy.md](references/afterpay-brand-strategy.md)

#### WHEN working on BNPL product marketing — UI patterns or notifications:
→ Load [references/afterpay-ui-patterns.md](references/afterpay-ui-patterns.md)

#### WHEN working on BNPL product marketing — terminology or compliance language:
→ Load [references/afterpay-terminology.md](references/afterpay-terminology.md)

#### WHEN marketing content involves dates, times, or locations:
→ Load [references/creative-dates-times-locations.md](references/creative-dates-times-locations.md)

#### WHEN marketing content involves number formatting:
→ Load [references/creative-numbers.md](references/creative-numbers.md)

#### WHEN writing financial education or thought leadership content:
→ Load [references/financial-inclusion-context.md](references/financial-inclusion-context.md) (mission, demographics, trust stats)
→ Load [references/financial-inclusion-products.md](references/financial-inclusion-products.md) (product facts, fee comparisons, key stats)

#### WHEN reviewing marketing copy for accessibility or transparency:
→ Load [references/creative-inclusivity-and-transparency.md](references/creative-inclusivity-and-transparency.md)

#### WHEN checking grammar or style in marketing copy:
→ Load [references/creative-style-and-grammar.md](references/creative-style-and-grammar.md)

### Support Content

#### WHEN working on support or help articles (load first):
→ Load [references/support-writing-principles.md](references/support-writing-principles.md)
- **IF** need how-to article structure → [support-how-to-article.md](references/support-how-to-article.md)
- **IF** need troubleshooting article structure → [support-troubleshooting-article.md](references/support-troubleshooting-article.md)
- **IF** consumer product web help → [support-brand-b-web-help.md](references/support-brand-b-web-help.md)
- **IF** writing steps → [support-steps-writing.md](references/support-steps-writing.md)
- **IF** CF1 article → [support-cf1-article-guidelines.md](references/support-cf1-article-guidelines.md)

#### WHEN need support-specific formatting rules not covered in the articles above:
→ Load [references/support-specific-style.md](references/support-specific-style.md)

### Transactional and Legal

#### WHEN working on email, SMS, or push notifications:
→ Load [references/product-brand-b-transactional-communications.md](references/product-brand-b-transactional-communications.md)

#### WHEN working on legal copy for banking, direct deposit, savings, or account settings:
→ Load [references/legal-footers-banking-deposits.md](references/legal-footers-banking-deposits.md)

#### WHEN working on legal copy for card products, crypto, investing, or lending:
→ Load [references/legal-footers-card-investing.md](references/legal-footers-card-investing.md)

### General Product Copy

#### WHEN questions about punctuation, symbols, or text formatting mechanics:
- **Punctuation** (periods, commas, colons, semicolons, question marks, quotation marks, slashes, etc.) → [product-mechanics-punctuation.md](references/product-mechanics-punctuation.md)
- **Text mechanics** (abbreviations, active voice, bolded text, contractions, emojis, plurals, prepositions, trademarks) → [product-mechanics-text.md](references/product-mechanics-text.md)

#### WHEN questions about numbers, currency, or financial formatting:
→ Load [references/product-numbers-currency.md](references/product-numbers-currency.md)

#### WHEN questions about dates, times, time zones, or timestamps:
→ Load [references/product-numbers-dates-times.md](references/product-numbers-dates-times.md)

#### WHEN questions about point of view or perspective:
→ Load [references/product-point-of-view.md](references/product-point-of-view.md)

#### WHEN tagging or organizing content by type:
→ Load [references/content-tag-taxonomy.md](references/content-tag-taxonomy.md)

### Examples

#### WHEN you need a worked example (button, error message, design review):
→ Load [examples/common-workflows.md](examples/common-workflows.md)

## Communication Style

- Lead with your recommendation; put context and rationale after
- Prioritize fixes by importance — flag what's critical before what's nice to fix
- Be brief; skip fluff and unnecessary preamble
- Provide detail only when the user asks for it
- Prioritize truth over agreement — think critically, even if it means disagreeing
- Never fabricate standards; if uncertain, say so and note when you're inferring from general best practices

## Related Skills

- `arcade-design-review` — Use when validating or selecting Arcade design system components; pairs well with this skill when reviewing component content in consumer product UI
- `figma-atlas` — Use when syncing UI copy from Figma to localization files or managing i18n keys for component content

