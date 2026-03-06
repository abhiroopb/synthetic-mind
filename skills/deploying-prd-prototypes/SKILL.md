---
Skill name: deploying-prd-prototypes
Skill description: Deploy interactive prototypes from PRDs to Blockcell for internal sharing. Use when building demos, prototypes, or static sites from product requirements documents.
---

# Deploying PRD Prototypes to Blockcell

Deploy static website prototypes and demos from PRDs to Blockcell hosting service for internal sharing at Block.

**Sites are hosted at:** `https://blockcell.sqprod.co/sites/{site_name}/`

## Prerequisites

- **VPN Connection Required**: Must be connected to WARP VPN

## Prototype Source Code

All prototype source code should be placed in the `prototypes/` directory at the repository root (e.g., `prototypes/my-feature-demo/`). This directory is gitignored — prototype code is not committed to the repository. Only the deployed Blockcell URL matters.

## Workflow

### 1. Choose Site Name

- Use descriptive, reusable names like `neighborhoods-spring26-demo` or `local-cash-prototype`
- Check if it exists: Use `list_versions` to see if the name is already in use
- Every upload creates a new version automatically - reuse the same name when iterating

### 2. Configure Base Path

Set the base path **before building**:

```javascript
// vite.config.js
export default {
  base: "/sites/YOUR-SITE-NAME/",
};
```

### 3. Build

```bash
npm run build  # outputs to dist/
```

Must be static output. **SvelteKit** needs `adapter-static`, **Next.js** needs static export.

### 4. Deploy via REST API

Add to `package.json`:

```json
{
  "scripts": {
    "build:blockcell": "vite build --base /sites/my-demo/",
    "deploy:blockcell": "npm run build:blockcell && cd dist && zip -r ../site.zip . && curl -X POST 'https://blockcell.sqprod.co/api/v1/sites/my-demo/upload' -H 'Accept: application/json' -F 'file=@site.zip' && rm ../site.zip"
  }
}
```

Then run:

```bash
npm run deploy:blockcell
```

### 5. Update PRD

After deploying, update the Prototype section (§7 in PRD template) in the corresponding `requirements/<scope>/<feature>/PRD.md`:
- Blockcell URL
- Access notes
- What to test
- Known limitations

### 6. Rollback (if needed)

```bash
# List versions
curl "https://blockcell.sqprod.co/api/v1/sites/my-demo/versions"

# Promote a specific version
curl -X POST "https://blockcell.sqprod.co/api/v1/sites/my-demo/versions/abc123/promote"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **VPN Connection Required** | Connect to WARP VPN |
| **Broken images/CSS/JS** | Wrong base path - rebuild with `--base /sites/NAME/` |
| **Upload fails** | Check build directory exists and contains `index.html` |
| **Can't upload to site** | You don't own it - choose different name |
