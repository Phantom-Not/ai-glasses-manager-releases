# Maintain the product guide

The public site is a static product reference hosted by GitHub Pages from `main`, in `/docs`. The Android app remains proprietary. This repository contains its public downloads and documentation.

## Build and check

Python 3.10 or later is sufficient. No packages or build service are required.

```text
python tools/build_site.py
python tools/check_site.py
python tools/preview_site.py
```

Preview at <http://127.0.0.1:4173/ai-glasses-manager-releases/>. The checker detects stale generated pages, broken internal links, missing images, language mismatches, incorrect metadata and release-feed timestamps.

## Publish a release update

1. Verify the released APK version and published notes. Describe available features, not private development work.
2. Update `content/site.json` in English, Simplified Chinese and Japanese. Set `current_version` only when that release is public. Update page copy, feature lists, language counts and the README together. Shared navigation and interface labels live in each locale’s `ui` section.
3. Add the release to `releases`, newest first. Preserve its original `published` timestamp. Set a separate ISO 8601 `updated` timestamp only if that release entry changes. Editing the overall site date must not mark every old release as newly updated.
4. Keep upcoming features in the explicitly labelled preview. Remove or revise the teaser when they ship. Avoid precise catalogue counts that change with sources.
5. Update the bilingual Markdown in `release-notes/` and the matching GitHub release body. Do not change APK assets or `manager-update.json` as part of a documentation update.
6. Build, check and inspect desktop and mobile layouts, including the matching-page language links. Use approved public screenshots with no private files, identifiers or networks.
7. Review the diff, commit and push. GitHub Pages publishes `/docs` from `main`. Check the deployed pages, links, sitemap, feeds and download destination.
8. Notify participating search engines with the optional IndexNow command below. Submission is not a promise of indexing or ranking.

## Search-engine notifications

```text
python tools/submit_indexnow.py
python tools/submit_indexnow.py --submit
```

The default is a dry run. Submission first verifies that the public key file is available. `content/indexnow.json` stores a public ownership-verification key, not a password. The `keyLocation` limits verification to this project directory rather than other repositories on the shared GitHub Pages host.

For Google, add this exact URL-prefix property to Search Console:

<https://phantom-not.github.io/ai-glasses-manager-releases/>

Use the HTML verification file Google provides, publish it inside `docs/`, complete ownership verification in the account, then submit `sitemap.xml`. Do not put private account credentials in this repository. Google decides when to crawl and what to index.

## Content rules

Use plain, human wording with no em or en dashes. Identify AI Glasses Manager as Bruce's independent app for Rokid Glasses, formerly Rokid Manager. Explain the broad Android App Store separately from curated Rokid developer apps. Do not call the proprietary application open source, an official Rokid phone app or a fork of a community list.

Keep titles and descriptions useful to readers. Do not invent reviews, ratings, compatibility, search rankings or a Google rich-result guarantee. Search and AI tools can take time to reflect corrections.

## Photo viewer and update feeds

Filter examples on Home and Camera use a small local script with a native dialog. Keep full-image links as the fallback and verify close-button, Escape, backdrop, focus restoration and mobile sizing when changing it. The checker allows the deferred viewer script only on those six localized pages, plus the local appearance script in each page head.

The footer Atom link opens the readable Updates page at `#feed`, which provides a copyable feed address. Preserve the actual `updates/feed.xml` addresses and timestamps for feed-reader subscriptions.

## Appearance

Every localized page offers System, Light and Dark beside the language picker. System is the default. An explicit choice is saved only in the visitor's browser under `ai-glasses-manager:appearance`; selecting System removes it. The synchronous local `assets/theme.js` sets the appearance before CSS loads, updates browser chrome, follows system changes, and synchronizes choices between tabs. Storage failures still allow a choice for the current page. Without JavaScript, CSS follows the system setting and hides the nonfunctional picker. Print uses light colors. Original photos and app screenshots are never recolored.

Run `node tools/test_theme.cjs` for preference, denied-storage, system-change, cross-tab and menu behavior fixtures. Check dark and light on desktop and narrow mobile layouts, localized menus, the photo dialog, feed field, links, buttons and keyboard focus. Keep theme scripts local and preserve the checker's exact script allowlist.

## Ownership files and robots scope

`content/search-verification.json` stores only Google's public verification filename and body downloaded from the authenticated Search Console property. The builder validates both before generating anything and emits the file unchanged. Keep the file after verification so ownership can be checked again. Never add account credentials, OAuth tokens or private keys here.

The builder creates `docs/robots.txt` with the requested allow-all group and the existing sitemap address. On this project site it is served at:

<https://phantom-not.github.io/ai-glasses-manager-releases/robots.txt>

Crawlers use robots rules from the **host root**, <https://phantom-not.github.io/robots.txt>, not the project subdirectory. A missing host-root robots file does not itself block crawling. This project file is not a substitute for sitemap submission or ownership verification. Do not modify another repository's root policy as part of this site's routine maintenance.

After Google verification, submit the existing full sitemap URL in Search Console, then inspect and request indexing for these URLs:

- <https://phantom-not.github.io/ai-glasses-manager-releases/>
- <https://phantom-not.github.io/ai-glasses-manager-releases/features/>
- <https://phantom-not.github.io/ai-glasses-manager-releases/camera-filters/>
- <https://phantom-not.github.io/ai-glasses-manager-releases/updates/2.6.3/>

Import the verified property and its sitemap into Bing Webmaster Tools using the owner account, or verify directly if import is unavailable. A successful request confirms submission, not indexing. Review Coverage/Pages and Performance in the consoles after data is available. Avoid duplicate metadata/JSON-LD, near-duplicate keyword pages and claims of guaranteed rankings. Existing App Store, camera and file-transfer guides already cover the corresponding checklist subjects. Dedicated social artwork and third-party listings are optional editorial work, not requirements for crawling.

Primary references: [Google robots placement](https://developers.google.com/crawling/docs/robots-txt/create-robots-txt), [Google ownership verification](https://support.google.com/webmasters/answer/9008080), [Bing site verification/import](https://www2.bing.com/webmasters/help/add-and-verify-site-12184f8b).
