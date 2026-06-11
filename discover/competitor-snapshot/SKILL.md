---
name: competitor-snapshot
description: >
  Use when analyzing competitors: rankings, content strategy, SERP features, and positioning. Not for keyword-only lists — use topic-keyword-finder first.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
homepage: "https://github.com/searchhawk/skills"
when_to_use: "Competitor analysis, who ranks for, battlecard, competitive SEO."
argument-hint: "<domain-or-competitor> [--compare <your-domain>]"
allowed-tools: WebFetch
metadata:
  product: SearchHawk Skills
  tagline: "SEO · AEO · GEO for AI assistants"
---

# Competitor Snapshot

Map who wins in search and why.

## Quick Start

```
Analyze competitors for [topic] — compare [your-site.com] vs [competitor.com]
```

## Skill Contract

- **Reads**: competitor URLs/domains, optional your domain, keyword set
- **Writes**: battlecard + gap themes
- **Done when**: 3+ competitors profiled with content type, strengths, weaknesses
- **Primary next skill**: `content-gap-finder`

## Instructions — 6 phases

1. **Identify** — top 3–5 SERP or user-named competitors
2. **Profile** — homepage, key landing, blog depth (fetch sample pages)
3. **SERP features** — snippets, PAA, video they hold
4. **Content patterns** — format, depth, freshness
5. **Authority cues** — Estimated unless backlink data provided
6. **Battlecard** — table + recommended angles for you

## Reference Materials

- [instructions-detail.md](references/instructions-detail.md)
- [example-report.md](references/example-report.md)

## Next Best Skill

`content-gap-finder` → `search-content-writer`
