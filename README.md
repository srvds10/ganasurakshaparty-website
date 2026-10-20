# Gana Suraksha Party — Website

Source for the official website at **https://ganasurakshaparty.org**, hosted free on GitHub Pages.

- `index.html` — the whole site (one page)
- `logo.png`, `og.jpg` — party emblem and social-share image
- `favicon.ico`, `favicon-32.png`, `icon-192.png`, `apple-touch-icon.png` — browser tab / home-screen icons
- `CNAME` — tells GitHub Pages to serve the site on ganasurakshaparty.org

To update the site, edit `index.html` and commit to `main`; GitHub Pages republishes automatically within a minute or two.

## Videos section

The Videos section shows the 6 latest uploads from the party's YouTube channel as small cards.
The list lives in `videos.json` and is refreshed every 6 hours by the **Update YouTube videos**
GitHub Action (`.github/workflows/update-videos.yml`, which runs `scripts/update_videos.py`).
To refresh it right away: **Actions → Update YouTube videos → Run workflow**.
If `videos.json` is missing, the page falls back to a single channel player.
