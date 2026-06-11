---
name: content-gap-finder
description: >
  Use when finding content gaps vs competitors: missing topics, weak pages, and priority opportunities. Requires competitor or keyword context.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
homepage: "https://github.com/searchhawk/skills"
when_to_use: "Content gap analysis, what am I missing, competitor content gaps."
argument-hint: "<your-domain> [--competitors <domains>]"
allowed-tools: WebFetch
metadata:
  product: SearchHawk Skills
  tagline: "SEO · AEO · GEO for AI assistants"
---

# Content Gap Finder

Find topics and pages competitors cover that you don't.

## Skill Contract

- **Done when**: gap list with priority, intent, and suggested page type per gap
- **Primary next skill**: `topic-keyword-finder` or `search-content-writer`

## Instructions — 5 phases

1. **Inventory** — your site topics (nav, sitemap, blog categories)
2. **Competitor inventory** — same for 2–3 competitors
3. **Diff** — topics they have, you lack
4. **Score gaps** — traffic potential (Estimated), effort, strategic fit
5. **Deliver** — prioritized gap table + brief page recommendations

## Next Best Skill

`search-content-writer` for top gap.
