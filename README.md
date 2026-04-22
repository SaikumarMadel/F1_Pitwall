# The Pit Wall · F1 2026 Dashboard
**Auto-deployed static site with live content updates.**

---

## Quick Start: Update & Deploy in 3 Steps

### 1. Update Content (Edit Once)
Open [`data/content.json`](data/content.json) and change:
- News headlines, body text, kickers
- Stats labels, values, subtitles

Save the file.

### 2. Commit & Push
```bash
git add data/content.json
git commit -m "Update F1 stats and stories"
git push origin main
```

### 3. Done
The Ergast refresh workflow updates every 5 minutes, and the live site reflects the latest committed content after GitHub Pages redeploys. No HTML editing needed.

---

## Project Structure

```
.
├── index.html                 # Main page (do not edit for content)
├── v2.html                    # Secondary page
├── data/
│   └── content.json           # ← EDIT THIS to update stories & stats
├── .github/
│   └── workflows/
│       └── deploy-pages.yml   # Auto-deploy pipeline (leave as is)
└── .nojekyll                  # Tells GitHub Pages to serve as-is
```

---

## How It Works

1. **You edit [`data/content.json`](data/content.json)**
   - Add/remove/update news items or stats
   - JSON structure is human-readable

2. **You commit and push to `main` branch**
   ```bash
   git push origin main
   ```

3. **GitHub Action triggers automatically**
   - Runs workflow in `.github/workflows/deploy-pages.yml`
   - Uploads all files to GitHub Pages
   - Runs `.github/workflows/update-f1-data.yml` on a 5-minute schedule to refresh Ergast data

4. **Live site updates**
   - Your domain refreshes with new content
   - Visitors see changes within 30–60 seconds

---

## Content File Format

### News Items in [`data/content.json`](data/content.json)

```json
{
  "news": [
    {
      "number": "01",
      "variant": "lead",           // "lead" or "neutral" or "" for normal
      "kicker": "The Story",        // Category badge
      "headline": "Your headline",
      "body": "Full story text..."
    }
  ]
}
```

**Variants:**
- `"lead"` — Large headline, featured
- `"neutral"` — Engine gray badge
- `""` — Normal item

### Stats in [`data/content.json`](data/content.json)

```json
{
  "stats": [
    {
      "label": "Championship Lead",
      "valuePrefix": "+9",          // Before the emphasized part
      "valueEm": "pts",             // Emphasized (italics)
      "valueSuffix": "",            // After emphasized
      "sub": "Antonelli over Russell"
    }
  ]
}
```

**Example rendering:**
- `valuePrefix: "+9"` + `valueEm: "pts"` → displays as: **+9 *pts***

---

## First-Time Setup

Only do this once:

### 1. Initialize Git Repo (if not already)
```bash
cd d:\Projects\F1_Pitwall
git init
git branch -M main
git add .
git commit -m "Initial commit: Pit Wall dashboard"
```

### 2. Add Remote & Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/F1_Pitwall.git
git push -u origin main
```

### 3. Enable GitHub Pages
1. Go to **GitHub repo** → **Settings** → **Pages**
2. Set:
   - Source: **Deploy from a branch**
   - Branch: **main** / root folder
3. Wait 1–2 minutes for first deploy

Your site will be live at: `https://YOUR_USERNAME.github.io/F1_Pitwall/`

---

## Browser Caching (Optional But Recommended)

If visitors see stale content, set cache headers. For now, pages cache for 5 minutes, which is safe for live updates.

---

## Common Tasks

### Add a new story
Edit [`data/content.json`](data/content.json), add item to `news` array, push.

### Update a stat
Edit [`data/content.json`](data/content.json), modify `stats` array, push.

### Change page layout/styling
Edit [`index.html`](index.html) directly, push. Content updates from JSON automatically.

### Preview before deploying
1. Open [`index.html`](index.html) locally in a browser
2. Open DevTools Console (F12)
3. It will fetch [`data/content.json`](data/content.json) and render

---

## What NOT to Edit

- ❌ Don't add `<div>` HTML to [`index.html`](index.html) for stats/stories — they're rendered from JSON
- ❌ Don't delete the `id="newsBlock"` or `id="statsGrid"` elements in [`index.html`](index.html)
- ❌ Don't modify `.github/workflows/` unless you know what you're doing

---

## Troubleshooting

### Site not updating after push?
1. Check GitHub Actions: **repo** → **Actions** tab
2. Look for red ✗ (failed) or green ✓ (passed) workflow
3. If failed, click it to see error details

### Content not loading when I open index.html locally?
- Browser might block fetch for local files (CORS security)
- Use a local server: `python -m http.server 8000` then visit `http://localhost:8000`

### JSON syntax error?
- Validate [`data/content.json`](data/content.json) at [jsonlint.com](https://www.jsonlint.com)
- Check for missing commas, quotes, brackets

---

## Next Steps (Optional)

Want even more automation? Consider:

1. **Auto-fetch live F1 API data**
   - Update standings, race results, lap times hourly
   - Use GitHub Actions schedule

2. **Custom domain**
   - Add CNAME file to point to your own domain
   - GitHub Pages supports custom domains free

3. **Email alerts**
   - Notify you when content needs updating
   - Use IFTTT or webhook

---

**That's it.** You now have a fully automated, no-hustle update pipeline.

Just edit [`data/content.json`](data/content.json) and push. Done.
