# Gravity Marketing — Weekly Social Playbook

This repo powers the automated Facebook + Instagram posting for **Gravity Marketing**
(Metricool brand id `7257314`, timezone `Asia/Karachi`, IG `@gravitymarketingltd`).
The weekly scheduled task follows this file exactly.

## Who we are (facts only — never invent beyond these)
- Software development company: web development, mobile (iOS/Android) development, backend
  development and full-stack product builds.
- Stack we can mention: React, Next.js, React Native, TypeScript, Node.js/Express, GraphQL, REST,
  Python/FastAPI, .NET, microservices, Socket.IO, AWS (Lambda, AppSync, Amplify), Docker, CI/CD,
  MongoDB, PostgreSQL, MySQL, DynamoDB.
- Own products:
  - **SehatFlow** (sehatflow.com) — pharmacy management: sales, inventory, purchasing, reporting
    in one workspace; AI-assisted invoice import; built-in drug interaction checker.
  - **Cheech** — ride-sharing app, live on Google Play, iOS coming to the App Store.
- Target audience: **international** founders, startups and business owners (US, UK, EU, Gulf)
  who need an app, web platform or backend built. Write in clear, friendly English.

## Hard rules
- NEVER invent clients, testimonials, results, metrics, awards, team size, years in business,
  prices, or product features not listed above. No fake screenshots of real products.
- No website URL for Gravity unless one is added here. Calls to action are DMs with a keyword
  (e.g. "DM us STACK"), or sehatflow.com for SehatFlow posts.
- Keep claims general and true ("we build…", "here's how to think about…").
- No political, religious or controversial topics. No competitor bashing.

## Weekly cadence
- 5 posts per week, Monday–Friday, at **21:30 Asia/Karachi** (≈ 12:30 US Eastern / 17:30 UK).
  Once Metricool `getBestTimeToPostByNetwork` returns non-zero values for Instagram, use the best
  slot between 18:00 and 23:30 Asia/Karachi instead.
- Mix per week (adjust toward what performed best):
  - 2 × education carousels (founder-friendly: costs, tech choices, MVP scoping, hiring a team,
    launch checklists, security basics, performance, maintenance)
  - 1 × product showcase (alternate SehatFlow / Cheech; at most 1 product post per week)
  - 1 × myth-vs-reality or quick-take single image
  - 1 × services / behind-the-build / "how we work" post
- Every post ends with ONE call to action.

## How to produce a post
1. Create `posts/YYYY-MM-DD-slug/post.json` (see existing posts for format). Keys:
   `publish`, `pillar`, `topic`, `caption`, `first_comment`, `slides`.
   Slide types: cover, point, list, compare, myth, cta (see `tools/render.py`).
   - Carousels: 3–7 slides, cover first, cta last. Keep text short — ≤ 30 words per slide body.
   - Captions: hook line, short value, CTA, "save/share" nudge, 6–8 hashtags at the end.
2. Render: `PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers python3 tools/render.py posts/<folder>/post.json`
   (if Chromium is missing: `python3 -m playwright install chromium`).
3. Look at every rendered PNG (make a contact sheet) and fix overflow or awkward wrapping.
4. Commit and push to `main`. Image URLs are
   `https://raw.githubusercontent.com/shoaibbadshah/gravity-social-assets/main/posts/<folder>/slide-NN.png`.
   Confirm one URL returns HTTP 200 before scheduling.
5. Schedule with Metricool `createScheduledPost` (blogId `7257314`), one call per post:
   providers facebook + instagram, `autoPublish: true`, `media` = slide URLs in order,
   `instagramData: {"type": "POST"}`, `facebookData: {"type": "POST"}`,
   `publicationDate: {"dateTime": "<publish>", "timezone": "Asia/Karachi"}`.
6. Append each post to `content-log.md`.
7. Verify with `getScheduledPosts` that every post is there.

## Weekly review (before planning)
- Pull last 7 days of Instagram + Facebook post metrics from Metricool (reach, likes, comments,
  saves, shares, follower growth). Note the top and bottom post in `content-log.md` under
  "Weekly notes" and shift the next week's mix toward the top pillar.
- Never repeat a topic already in `content-log.md` within 8 weeks.
