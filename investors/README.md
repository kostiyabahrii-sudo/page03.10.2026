# Fitkit — investors site

Frontend only. React + Vite + React Router. Mobile-first (most visitors come from a QR code).

## Run

```
npm install
npm run dev      # http://localhost:5173
npm run build    # -> dist/
```

## Pages

| Route       | What                                                         |
|-------------|--------------------------------------------------------------|
| `/`         | About (placeholder copy)                                     |
| `/team`     | Wide team photo, then one card per member                    |
| `/roadmap`  | Now / Next / Later, then FAQ (`/roadmap#faq`)                 |
| `/products` | Two screens: extension (“Open in store”), app (“Join waitlist”) |

LinkedIn in the nav opens https://www.linkedin.com/company/fitkitcommerce/ in a new tab.

## Content

All text, links and images are in `src/content.js`. Images go into `public/`;
set `src` (e.g. `"/team.jpg"`). While `src` is `null` a labelled placeholder
box is shown.

Build-time env vars:

- `VITE_WAITLIST_URL` — where “Join waitlist” goes
- `VITE_STORE_URL` — where “Open in store” goes

## Deploy

It's a single-page app: the host must rewrite every path to `/index.html`
(on Render static sites: Redirects/Rewrites → `/*` → `/index.html`, Rewrite).
`npm run dev` proxies `/api` to `http://localhost:8000` if the backend is needed later.

## Style notes

- Headings: Newsreader (Google Fonts). Body: SF on Apple devices, Helvetica fallback.
- White background, #111 text and lines, `border-radius: 0` everywhere, no animations.
- Checked at 320, 390 and 1280 px wide with no horizontal scroll.
