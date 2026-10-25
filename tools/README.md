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
