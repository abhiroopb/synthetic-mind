---
name: ecom-great-stores
description: "Search and surface example ecommerce seller sites by industry, feature, or use case. Use when searching, finding, browsing, discovering, locating, surfacing, or looking up online store examples, seller website references, great stores, demo sites, online ordering examples, or ecommerce inspiration for specific verticals."
depends-on: [slack]
---

# Ecommerce Great Stores

**STOP** if the `slack` skill is not installed or Slack authentication fails — this skill requires Slack search to query the archived channel.

Surface example ecommerce seller sites from a curated Slack channel archive. The channel served as a directory where sales reps shared and requested example online store sites by industry/feature.

## What's in the archive

The channel contained:
- **Site example requests**: Sales reps asking for examples by industry vertical (restaurants, retail, coffee shops, bakeries, florists, jewelry, pet stores, grocery, etc.)
- **Showcase posts**: Links to well-designed online store sites with commentary on what makes them great
- **Feature-specific examples**: Sites demonstrating pickup, delivery, shipping, catering, subscriptions, QR ordering, multi-location, appointments, loyalty, reviews, pre-orders, and third-party delivery integration
- **Competitive comparisons**: Sellers evaluating platforms vs. competitors (Toast, Wix, Shopify, Squarespace, WooCommerce)
- **Configuration help**: Questions about modifiers, fulfillment schedules, item ordering, and store setup

## Key resources

| Resource | Description |
|----------|-------------|
| Example sites directory | Internal curated list of example sites |
| Great stores directory | Internal great stores directory |
| Searchable dashboard | Searchable dashboard of seller sites |
| Active discussion channel | Active channel for new discussions |

## Industry verticals frequently requested

QSR, FSR (full-service restaurant), coffee shops, bakeries, ice cream, pizza, sushi/poke, grocery stores, florists, salons, pet stores, bookstores, jewelry, bridal, wine/liquor, furniture, arts/crafts, candy, clothing/apparel, supplement/vitamin, nonprofit/donations, ghost kitchens, food halls, catering, B2B/wholesale, university campus dining

## How to search

Load the `slack` skill, then search the archived channel using `search-messages`:

```
# Search by keyword in archived channel
search-messages --query "in:#ecom-great-stores <search term>"

# Example searches by industry
search-messages --query "in:#ecom-great-stores coffee shop"
search-messages --query "in:#ecom-great-stores bakery"
search-messages --query "in:#ecom-great-stores grocery"

# Example searches by feature
search-messages --query "in:#ecom-great-stores catering"
search-messages --query "in:#ecom-great-stores multi-location"
search-messages --query "in:#ecom-great-stores shipping"
search-messages --query "in:#ecom-great-stores appointments"
```

Also check the active discussion channel for newer examples.
