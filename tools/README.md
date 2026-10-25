# Website maintenance

The product guide is published by GitHub Pages from `main`, in `/docs`.

## Build and preview

Python 3.10 or later is sufficient. No packages are required.

```text
python tools/build_site.py
python tools/check_site.py
python tools/preview_site.py
```

Preview at <http://127.0.0.1:4173/ai-glasses-manager-releases/>. Check desktop and mobile layouts before publishing.

## Content updates

Edit `content/site.json` in English, Simplified Chinese and Japanese, then rebuild. Keep the public version, downloads, feature descriptions and release notes consistent. Preserve original release dates and use a separate updated date only when an entry changes. Keep unreleased changes in the labelled preview.

Use concise, natural wording and approved screenshots. Review the diff before committing. Website updates should preserve APK assets and `manager-update.json`.

## Interface checks

Appearance offers System, Light and Dark. The choice stays in the visitor's browser. Run `node tools/test_theme.cjs` when changing appearance behavior. Verify menus, keyboard focus, photo viewing and narrow mobile layouts in both modes.

Photo examples open in a dialog with a full-image link as fallback. Check the close button, Escape, tapping outside, and focus restoration. Keep the existing localized feed addresses and release timestamps stable.

The builder also maintains the sitemap and public verification files. Keep verification files unchanged.
