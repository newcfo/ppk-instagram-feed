# PERFECT POTION — weekly Instagram feed

This **public repository** contains only automation code and public Instagram post metadata for the PERFECT POTION Korean store. The existing store operations repository `newcfo/ppk-store-launch` remains **private**.

The scheduled job reads a Behold JSON feed for `@perfectpotion.kr`, selects the six newest eligible posts, generates a static JavaScript data file, and publishes it with GitHub Pages. **No Cafe24 FTP password or Meta OAuth token is needed.**

- Intended Pages address: https://newcfo.github.io/ppk-instagram-feed/ppk-instagram-weekly.js
- Schedule: every Monday at 00:00 UTC (**09:00 Korea time**); GitHub may delay scheduled workflows
- Data: six public Instagram permalinks, optimized Behold thumbnails, short alt text and update timestamp
- Safeguard: feed validation failures stop deployment and retain the previous successful Pages release
- Site integration: after the Pages deployment succeeds, the Cafe24 homepage must **once** load the JS snapshot and the published six-card adapter. The current homepage will not change merely by creating this repo.

## First activation

1. **Settings → Pages → Build and deployment → Source: GitHub Actions**.
2. **Actions → Update PPK Instagram every Monday → Run workflow**. Check the run succeeds.
3. Open the Pages asset URL above and verify the six links and images.
4. In the active Cafe24 storefront skin, back up `index.html`. On the existing Instagram **six-card grid container** (not the whole Instagram section), add the attribute `data-ppk-instagram-grid`. Load the following scripts in order and preserve original six static cards as fallback:

   ```html
   <script defer src="https://newcfo.github.io/ppk-instagram-feed/ppk-instagram-weekly.js"></script>
   <script defer src="https://newcfo.github.io/ppk-instagram-feed/ppk-instagram-home-adapter.js"></script>
   ```

   The adapter updates only the six existing card anchors and images and does not change grid CSS. It requires that exactly six card anchors contain Instagram URLs and an `<img>` element. If the existing markup differs, inspect and adapt carefully before saving. Do not overwrite the existing product, story, or legal sections.
5. Check desktop, 390px mobile, links, reel covers, and fallback. The GitHub workflow can then update the public file weekly without changing the Cafe24 HTML again.

## Files

- `scripts/build_feed.py`: validated Behold → six-item public JS
- `scripts/test_build_feed.py`: synthetic feed validation tests
- `site/ppk-instagram-home-adapter.js`: public storefront six-card adapter
- `.github/workflows/weekly.yml`: scheduled and manual GitHub Pages deployment

**Important:** This repository is intentionally public. Never add customer data, ecommerce operations files, GitHub secrets, Meta tokens, login credentials or Cafe24 FTP details.
