---
name: ecom-research
description: "Search and surface ecommerce research insights including seller quotes, site reviews, competitive analysis, CSAT data, and online store UXR findings. Use when searching, querying, browsing, finding, surfacing, discovering, or looking up ecom research, seller feedback, site reviews, competitive insights, or online ordering findings."
depends-on: [slack]
---

# Ecommerce Research

Surface insights from an archived Slack research channel, which was the ecommerce research team's hub.

**STOP** if the `slack` skill is not installed — all workflows depend on searching the archived channel.

## What's in the archive

The channel contained:
- **Seller Quote of the Day/Week**: Daily/weekly NPS and CSAT verbatims from online store sellers, organized by theme weeks (Feature Gap, Performance, Usability, Competitor Mentions, Positive Mentions, Food & Drink, Holiday, Editor)
- **Site of the Day**: Daily reviews of ecommerce sites with UX commentary
- **Industry roundups**: Weekly roundups of industry articles, podcasts, neighborhood spotlights, and competitive intel (DoorDash, Toast, Wix, Shopify, WordPress/WooCommerce)
- **Research share-outs**: UXR synthesis, alpha findings, CSAT reports, seller-buyer relationships, onboarding research
- **Seller Pulse Program**: Live call summaries with sellers
- **3P delivery analysis**: Third-party delivery app penetration data among sellers

## Key research artifacts (check these first)

When a question maps to one of these documents, open and read the doc first before falling back to Slack search:

| Document | Topic |
|----------|-------|
| Online Store UXR Synthesis | Future of online sites research (sellers + buyers) |
| Quarterly CSAT Report | Quarterly seller satisfaction |
| Seller-Buyer Relationships | How sellers use events as engagement spaces |
| NPS Methodology Changes | NPS methodology updates |
| Research Monthly Newsletter | Monthly research newsletter |

## Key findings (verify against source before citing)

These are reference starting points. Always verify against the linked artifact before reusing.

1. **Online Sites Redesign**: Well received by F&B sellers; attractive to buyers; retail shows promise but needs more exploration
2. **Online Onboarding**: Messy catalogs are the #1 blocker to selling online — catalog structure is the root cause, not just missing images
3. **3P Delivery**: ~48% of restaurant sellers use at least one delivery app; DoorDash leads, then UberEats, Grubhub
4. **CSAT themes**: Syncing/performance/reliability issues; design customization limitations; catalog management friction
5. **Competitive landscape**: Sellers find switching "daunting"; majority of millennials/Gen Z check a business website for legitimacy

## How to search

- [ ] Check if the question maps to a linked artifact above — open and read the doc first
- [ ] If the doc doesn't answer the question, load the `slack` skill and search the archived channel

```bash
search-messages --query "CSAT verbatim" --in-channel <research-channel> 
search-messages --query "site of the day" --in-channel <research-channel>
search-messages --query "delivery analysis" --in-channel <research-channel>
```
