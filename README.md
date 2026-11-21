# Master Key Genie — Marketing Site

Static marketing website for **Master Key Genie** (Appfinity LLC). Designed for deployment to **Cloudflare Pages**.

## Pages

| File | Purpose |
|------|---------|
| `index.html` | Homepage — hero, features, product visuals, store CTAs |
| `offline.html` | Offline Edition — project data stays on the device |
| `government.html` | Redirects to `offline.html` |
| `about.html` | About Us |
| `news.html` | News & Press (HTML press release + PDF) |
| `blog/` | Blog index and posts (static HTML, no comments) |
| `privacy.html` | Privacy Policy |
| `contact.html` | Contact (`support@masterkeygenie.com`) |

### Publishing a blog post

1. Add `blog/your-slug.html` using an existing post as the template.
2. Add a short entry to the list in `blog/index.html` (date, title, excerpt, link).
3. Keep tone practical for locksmiths; end with CTAs (Offline Edition, Pricing, Contact).
4. No comments—use Contact for replies.

## Local preview

Open `index.html` in a browser, or serve the folder:

```bash
npx --yes serve .
```

## Cloudflare Pages

1. Create a Git repo and push this folder (root of the repo).
2. In Cloudflare Dashboard → **Workers & Pages** → **Create** → **Pages** → connect the repo.
3. Build settings:
   - **Framework preset:** None
   - **Build command:** *(leave empty)*
   - **Build output directory:** `/` (or `.`)
4. Save and deploy. Attach your custom domain when ready.

No build step is required; Pages will publish the static files as-is.

## Before you launch

1. **Store links** — Edit `js/links.js` and set `appStore` / `playStore` to your real Apple App Store and Google Play URLs. Update `windowsMsi` when you publish a new GitHub Release build.
2. **Screenshots** — Live shots live in `assets/screenshots/` and are used on the homepage hero + gallery.
3. **Privacy** — Review `privacy.html` with counsel if needed; it reflects the product’s offline + encrypted sync design.

## Brand assets

Copied from the Windows app:

- `assets/brand-mark.png` — genie + key mark
- `assets/logo.png` — full wordmark lockup
- `assets/favicon.png` / `assets/icon.png`
- `assets/appfinity-logo.png` — company mark (footer)
