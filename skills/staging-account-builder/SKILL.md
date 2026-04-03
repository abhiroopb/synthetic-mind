---
name: staging-account-builder
description: Use when creating, provisioning, building, populating, generating, or configuring F&B staging accounts, test restaurants, catalog images, daily orders, labor data, inventory, or merchant provisioning endpoints. Provisions merchants on a staging environment with activated payments, subscriptions, AI-generated catalog photos, menus, locations, ordering profiles, labor, inventory with COGS, and daily orders.
---

# F&B Staging Account Builder

Provisions complete F&B staging merchant accounts from scratch, with brand-specific catalog, photos, locations, menus, orders, ordering profiles, labor, inventory, and more — ready for AI prompt testing and COGS/variable cost analysis.

**STOP** if the user needs accounts on production (not staging) — this skill only works with staging APIs.

## Prerequisites

See `SETUP.md` for full setup including AI image generation backends (Vertex AI / Gemini API key / Unsplash fallback). The skill works out of the box with stock photos; AI-generated images require additional setup.

## Available Verticals

| Vertical | Brand | Tier | Concept | MCC |
|----------|-------|------|---------|-----|
| `qsr` | Matt's Pizza & Burgers | QSR Tier 3 | Regional pizza + burger chain | 5814 |
| `fsr` | Harvest Table | FSR Tier 1 | Farm-to-table, seasonal menu | 5812 |
| `bakery` | Morning Light Bakery | Bakery Tier 2 | Artisan sourdough, pastries, sandwiches | 5812 |
| `coffee` | Fog City Coffee | Coffee Tier 2 | Specialty roaster, espresso, light bites | 5812 |
| `bar` | The Brass Rail | Bar | Craft cocktails, beer, bar snacks | 5813 |

## Scripts

### 1. Provision a New Account

```bash
python3 scripts/provision_account.py --vertical=bakery
```

| Flag | Description |
|------|-------------|
| `--vertical` | **Required.** One of: `qsr`, `fsr`, `bakery`, `coffee`, `bar` |
| `--email-prefix` | Email prefix for the new account |
| `--skip-orders` | Skip order generation (faster provisioning) |
| `--skip-photos` | Skip photo uploads (much faster provisioning) |
| `--generate-images` | Use AI to generate item-specific photos (requires API key) |
| `--skip-labor` | Skip labor/staffing setup |
| `--skip-inventory` | Skip inventory setup |

#### What It Does (14 steps)

1. **Create merchant** via provisioning API (with payment activation)
2. **Add subscriptions** (POS Plus, KDS, marketing, team-management, etc.)
3. **Create extra locations** as needed
4. **F&B onboard** via restaurant onboarding API
5. **Populate catalog** — items with descriptions, variations, prices, and categories
6. **Upload photos** — AI-generated or curated stock images
7. **Create menus** — category structure with grouped items assigned to all channels
8. **Configure locations** — names, addresses, hours, descriptions, website, socials
9. **Generate customers** via provisioning API
10. **Create floorplans** (FSR/bar only)
11. **Generate orders** — a full day of paid orders across all locations
12. **Set up ordering profile** — configure brand, assign menu, enable pickup/delivery
13. **Set up labor** — create jobs with wages, team members, timecards, scheduled shifts
14. **Set up inventory** — stock counts, adjustments, cost data for COGS analysis

### 2. Generate / Refresh Catalog Images

```bash
python3 scripts/generate_images.py <vertical> [--upload] [--dry-run]
```

Uses Gemini 2.5 Flash Image via Vertex AI for photorealistic, item-specific images. Each prompt is context-aware: vertical setting, surfaces, lighting, camera angle, and category hints. Falls back to Unsplash URLs if AI is unavailable.

### 3. Generate Daily Orders + Publish Weekly Schedules

```bash
python3 scripts/create_daily_orders.py
```

**Orders:**
- **Hours-aware**: Only creates orders within each location's business hours
- **Hourly distribution**: Morning rush for coffee/bakery, lunch+dinner peaks for QSR
- **Day-of-week volume**: Weekend multipliers (bar x1.6 Saturday, coffee x1.1 Monday)
- **Channel diversity**: POS, Online, DoorDash, Cash App — weighted per vertical
- **Fulfillment types**: Dine-in, pickup, delivery — weighted per vertical
- **Payment variety**: Card, cash, external sources with realistic tip probabilities

**Weekly Schedules:**
- Publishes a rolling 7-day schedule for all team members
- Vertical-specific shift patterns (bakery early-morning, bar late-night)
- Full-time staff scheduled most days; part-time randomly with realistic skip rates

### 4. Set Up Labor (Existing Accounts)

Creates jobs, team members with wages, past timecards (7 days), and upcoming scheduled shifts (7 days).

| Vertical | Staff | Example Jobs |
|----------|-------|-------------|
| QSR | 8 | Shift Lead, Line Cook, Cashier, Delivery Driver |
| FSR | 12 | GM, Sous Chef, Server, Host, Bartender, Food Runner |
| Bakery | 6 | Head Baker, Baker, Pastry Chef, Counter Staff |
| Coffee | 6 | Lead Barista, Barista, Shift Lead, Counter Staff |
| Bar | 7 | Head Bartender, Bartender, Barback, Server, Door Staff |

### 5. Set Up Inventory (Existing Accounts)

Sets physical stock counts for all catalog variations at all locations. Creates inventory adjustments. Brand configs include `cost_cents` on each variation for COGS calculation: Revenue (orders) - COGS (cost_cents x units) - Labor (wages x hours) = variable margin.

## What's On Every Account

- Payments activated (no KYC — provisioning API handles it)
- Full catalog with photos, descriptions, and pricing
- Menus with groups assigned to all channels and locations
- Business hours, website, socials on all locations
- Sample customers
- Restaurant floorplans and sections (FSR/bar)
- KDS defaults configured
- Ordering profiles enabled (brand info, colors, pickup/delivery, tipping)
- Loyalty, gift cards, and marketing enabled
- Daily orders across all locations with channel + fulfillment diversity
- Team members with job titles, wages, and tip eligibility
- Timecards (7 days past) and scheduled shifts (7 days upcoming)
- Inventory stock counts + cost data per variation for COGS analysis

## After Provisioning (Manual Steps)

- [ ] **Logo**: Upload in Dashboard (generate with the `logo_prompt` in the brand config)
- [ ] **Loyalty**: Launch program in Dashboard (wizard: 3 clicks)
- [ ] **Gift Cards**: Already enabled via Plus subscription
- [ ] **Marketing**: Already enabled via Plus subscription

## Brand Config Schema

Each vertical is defined by a JSON file in `brands/`. To add a new vertical, create a new JSON file following the same schema.
