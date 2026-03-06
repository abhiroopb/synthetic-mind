# Accessibility: Content Patterns and Testing

## Accessible Content Patterns

### Error Messages
Make error messages clear and actionable. Structure: **Problem → Context → Solution**

- ✅ "We couldn't verify your email address. Check for typos and try again."
- ❌ "Error 403" (not meaningful to users)
- ❌ "Invalid input" (blames user, not helpful)

### Form Fields

**Labels**: Always visible, not placeholder-only
- ✅ Label above or beside field, stays visible when typing
- ❌ Placeholder text that disappears when user starts typing

**Helper text**: Explain requirements before user acts
- ✅ "Password must be at least 8 characters"
- ❌ Showing error after user submits (make requirements clear upfront)

**Error messages**: Specific and helpful
- ✅ "Phone number must be 10 digits"
- ❌ "Invalid phone number"

### Navigation
**Descriptive labels**:
- ✅ "Account settings"
- ❌ "Settings" (too vague without context)

**Skip links**: Allow keyboard users to skip repetitive navigation → "Skip to main content"

### Time-Based Content
- Don't auto-advance carousels
- Provide pause buttons for moving content
- Allow users to extend timeouts
- ✅ "You have 5 minutes to complete this. Need more time?"
- ❌ Silent countdown with no warning

## Testing Checklist

- [ ] Keyboard navigation: Can you navigate using only Tab and Enter?
- [ ] Screen reader: Turn on VoiceOver (Mac) or NVDA (Windows) and listen
- [ ] Color contrast: Aim for 4.5:1 ratio minimum
- [ ] Reading level: Use a readability checker (target 7th-8th grade)
- [ ] Zoom test: Zoom to 200% — is content still readable and usable?
- [ ] Can someone understand this without seeing images or colors?
- [ ] Does this work for people across different cultures, languages, and backgrounds?

## Quick Reference

| Element | Requirement |
|---------|-------------|
| Images | Descriptive alt text |
| Icons | Accessible label or text alternative |
| Links | Descriptive text (not "click here") |
| Buttons | Clear, action-oriented labels |
| Form labels | Always visible, not placeholder-only |
| Error messages | Specific, helpful, solution-focused |
| Headings | Logical hierarchy (H1 → H2 → H3) |
| Color | Not the only way to convey meaning |
| Reading level | 7th-8th grade for general audiences |
| Sentence length | 8-14 words for maximum comprehension |
