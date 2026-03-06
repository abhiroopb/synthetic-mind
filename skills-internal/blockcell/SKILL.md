---
name: static-site-deployer
description: Deploy static website prototypes and demos to an internal static site hosting service for sharing.
metadata:
  status: experimental
  author: anonymous
  version: "0.1"
---

# Static Site Deployment Skill

Deploy static sites to an internal hosting service for sharing prototypes and demos.

**Sites are hosted at:** `https://<hosting-service-url>/sites/{site_name}/`

Features:

- Version-controlled deployments
- Automatic `index.html` serving
- SSO authentication integration

## Prerequisites

- **VPN Connection Required**: Must be connected to corporate VPN

## Agent Instructions

When a user requests static site deployment:

1. **Always ask for site name** if not provided
2. **Check existing versions** using `list_versions` to understand ownership
3. **Decide on the best deployment path** there are 2 options -- MCP or REST API documented below
4. **Confirm base path configuration** before building
5. **Validate build directory** contains `index.html` before uploading
6. **Provide clear success feedback** with URL and version ID

## Two Deployment Paths

|              | **Path 1: MCP (Agent)**                        | **Path 2: REST API (Script)**            |
| ------------ | ---------------------------------------------- | ---------------------------------------- |
| **How**      | Ask agent in natural language                  | Run `npm run deploy`                     |
| **Requires** | MCP server configured                          | Just curl (no MCP)                       |
| **Setup**    | None                                           | One-time `package.json` script           |
| **Best for** | Quick deploys, exploration, version management | Repeated deploys, CI/CD, team automation |
| **Pros**     | Flexible, conversational, handles edge cases   | Fast, automated, no agent needed         |
| **Cons**     | Needs MCP, agent must be running               | Manual setup, less flexible              |

**Choose Path 1** if you want the agent to handle deployment  
**Choose Path 2** if you want automated `package.json` scripts

## Path 1: Deploy via MCP (Agent)

### 1. Choose Site Name

**Agent Instructions for Site Names:**

- **Prompt for a name** if not provided
- **Check if it exists**: Use `manage_site(site_name="example", action="list_versions")` to see if the name is already in use
- **If site already exists**:
  - **If user owns it**: Upload creates a new version automatically (recommended workflow)
  - **If user doesn't own it**: Upload will fail - ask if they want to use `force=True` or choose a different name
- **DO NOT** automatically use `force=True` or pick a different name without confirmation
- **DO NOT** append numbers (`my-site-2`, `my-site-3`) without asking

**Naming Best Practices:** Use descriptive, reusable names like `brand-tools` or `spring26-demo`. Every upload creates a new version automatically - **reuse the same name when iterating**!

### 2. Configure Base Path

Once you have a site name, set the base path **before building**:

```javascript
// vite.config.js
export default {
  base: "/sites/YOUR-SITE-NAME/", // Use the name from step 1
};
```

Sites live at `/sites/{site-name}/`.

### 3. Build

```bash
npm run build  # outputs to dist/
```

Must be static output. **SvelteKit** needs `adapter-static`, **Next.js** needs static export.

### 4. Deploy

**Agent Action:** Use the `manage_site` MCP tool to upload the build directory:

```
manage_site(
    site_name="YOUR-SITE-NAME",  // From step 1
    action="upload",
    directory_path="./dist"  // Or ./build, ./out depending on framework
)
```

**What to tell the user:** Confirm the deployment with the site URL and version ID.

### 5. Visit

**What to tell the user:** The site is live at `https://<hosting-service-url>/sites/YOUR-SITE-NAME/`

### 6. Rollback (if needed)

**Agent Actions:**

To list versions:

```
manage_site(site_name="YOUR-SITE-NAME", action="list_versions")
```

To rollback to a specific version:

```
manage_site(site_name="YOUR-SITE-NAME", action="promote", version_id="abc123")
```

---

## Path 2: Deploy via REST API (Script)

### 1. Configure Base Path (if needed)

**Option A: Use CLI flag (Vite only)**
No config needed! Use `--base` flag in your script (see step 2).

**Option B: Framework config (SvelteKit, Next.js)**

For **SvelteKit**, edit `svelte.config.js`:

```javascript
import adapter from "@sveltejs/adapter-static";
export default {
  kit: {
    adapter: adapter(),
    paths: { base: process.env.DEPLOY_BASE || "" },
  },
};
```

For **Next.js**, edit `next.config.js`:

```javascript
module.exports = {
  basePath: process.env.DEPLOY_BASE || "",
  assetPrefix: process.env.DEPLOY_BASE || "",
};
```

### 2. Add Deploy Scripts

Add to `package.json`:

**For Vite:**

```json
{
  "scripts": {
    "build": "vite build",
    "build:deploy": "vite build --base /sites/my-demo/",
    "deploy": "npm run build:deploy && cd dist && zip -r ../site.zip . && curl -X POST 'https://<hosting-service-url>/api/v1/sites/my-demo/upload' -H 'Accept: application/json' -F 'file=@site.zip' && rm ../site.zip"
  }
}
```

**For SvelteKit:**

```json
{
  "scripts": {
    "build": "vite build",
    "build:deploy": "DEPLOY_BASE=/sites/my-demo npm run build",
    "deploy": "npm run build:deploy && cd build && zip -r ../site.zip . && curl -X POST 'https://<hosting-service-url>/api/v1/sites/my-demo/upload' -H 'Accept: application/json' -F 'file=@site.zip' && rm ../site.zip"
  }
}
```

**For Next.js:**

```json
{
  "scripts": {
    "build": "next build",
    "build:deploy": "DEPLOY_BASE=/sites/my-demo next build && next export",
    "deploy": "npm run build:deploy && cd out && zip -r ../site.zip . && curl -X POST 'https://<hosting-service-url>/api/v1/sites/my-demo/upload' -H 'Accept: application/json' -F 'file=@site.zip' && rm ../site.zip"
  }
}
```

**Customize:** Replace `my-demo` with your site name, and update output directory (`dist`, `build`, or `out`).

### 3. Deploy

```bash
npm run deploy
```

This builds with the correct base path and uploads in one command.

### 4. Visit

`https://<hosting-service-url>/sites/my-demo/`

### 5. Rollback (if needed)

```bash
# List versions
curl "https://<hosting-service-url>/api/v1/sites/my-demo/versions"

# Promote a specific version
curl -X POST "https://<hosting-service-url>/api/v1/sites/my-demo/versions/abc123/promote"
```

---

## Troubleshooting

| Issue                       | Solution                                                                               |
| --------------------------- | -------------------------------------------------------------------------------------- |
| **VPN Connection Required** | Connect to corporate VPN                                                               |
| **Broken images/CSS/JS**    | Wrong base path - rebuild with `--base /sites/NAME/`                                   |
| **Upload fails**            | Check build directory exists and contains `index.html`                                 |
| **Can't upload to site**    | You don't own it - choose different name (or use `force=True` if intentional override) |
| **SvelteKit not working**   | Use `adapter-static` + add `export const prerender = true` to `+layout.js`             |

---
