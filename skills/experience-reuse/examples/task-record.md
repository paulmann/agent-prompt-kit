---
id: documentation-pass-on-a-flat-wiki
type: task
title: Turn a repository wiki into a readable documentation set
status: validated
confidence: medium
applicability: A repository whose wiki has pages but no navigation, and links that do not resolve
tags: [documentation, github, wiki, links]
created_at: 2026-10-10
updated_at: 2026-10-24
last_verified_at: 2026-10-24
source: user task
related: [add-nullable-column-to-list-endpoint]
---

# Example: task record

## Request

"Our wiki is unreadable; make it a real documentation set." No page list, no audience, no scope.

## What was done

1. Listed every page through the API, not by eye: the wiki is a separate repository.
2. Recomputed the anchors of every heading and compared them with the table of contents. Six of twelve
   pages were unreachable; the contents listed pages that no longer existed.
3. Counted links by target: internal, cross-repository, image. Images were the dead ones — a wiki is
   a separate repository, so a relative image path resolves to a page that is not there.
4. Wrote a navigation file and a footer with absolute links only.
5. Verified with a script that resolves every anchor, then published to a dry run.

## Outcome

Eight pages plus eight translations, navigation covering all of them, zero broken anchors. The build
and the verification are in the repository; the publication step is one command.

## Verification

```text
wiki build    # 0 errors
wiki verify   # 0 errors, 0 notes
external check against the published bytes: anchors recomputed, 0 findings
```

## Reusable parts

- The anchor recomputation rule: lowercase, drop punctuation, spaces to hyphens, de-duplicate with
  `-1`. An em dash becomes two hyphens, which breaks hand-written tables of contents.
- The image rule: absolute raw URL, never a relative path.
- The navigation rule: order lives in a manifest, so the sidebar is generated, not typed.

## What not to repeat

- Searching the rendered HTML for a page's anchor: the platform's own documentation shows an example
  that contradicts its own output. Recompute from the heading text instead.
- Trusting a "link check" that only checks that a string looks like a link: it never resolved an
  anchor and reported success twelve times.
