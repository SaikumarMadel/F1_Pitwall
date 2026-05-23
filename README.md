# The Pit Wall · F1 Dashboard

Static GitHub Pages site with auto-refreshing F1 content.

## What Is Automated

1. `Refresh F1 Data` runs every 30 minutes (and on manual dispatch).
2. It updates `data/content.json` from the Ergast API.
3. If content changed, it commits/pushes to `main`.
4. `Deploy Static Site to GitHub Pages` runs on:
   - direct push to `main`
   - successful completion of `Refresh F1 Data`
5. Pages is redeployed automatically.

## Where To Edit Website Content

- Dynamic content source: `data/content.json`
- Site template/layout: `index.html`
- Refresh script: `scripts/update_f1_content.py`

## Manual Run

From GitHub Actions tab, run:
- `Refresh F1 Data` to pull latest data now.
- `Deploy Static Site to GitHub Pages` to redeploy now.

## Notes

- The site fetches `data/content.json` with `cache: no-store`.
- If API data is unchanged, no new commit is created.
- `.nojekyll` keeps static file serving behavior predictable.
