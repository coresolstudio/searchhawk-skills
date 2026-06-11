---
name: site-search-audit
description: >
  Use for full-site SEO, AEO, and GEO audit via live crawl. Entry point for search visibility diagnosis.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
when_to_use: "Audit my site, SEO AEO GEO check, why not ranking."
argument-hint: "<url> [--quick|--full]"
allowed-tools: WebFetch
metadata:
  product: SearchHawk Skills
---

# Site Search Audit

SearchHawk tri-pillar entry audit.

## Quick Start

```
Audit https://example.com for SEO, AEO, and GEO
Run a full SearchHawk audit on [domain]
```

## Skill Contract

- **Done when**: SEO/AEO/GEO scores 1–10 with evidence; pages listed; handoff complete
- **Primary next skill**: `fix-priority-ranker`

## Instructions — 6 phases

1. **Scope** — Quick (~6 pages) vs Full (sitemap/nav)
2. **Crawl** — robots, sitemap, homepage, About, services, blog, contact, FAQ
3. **SEO score** — on-page, depth, schema sample, links
4. **AEO score** — answers, FAQ, snippet patterns
5. **GEO score** — E-E-A-T, facts, entity
6. **Report** + recommend deep skills

Never flag missing pages without full-site check.

Optional: `python3 scripts/connectors/onpage.py <url>` per key URL.

## Reference Materials

- [instructions-detail.md](references/instructions-detail.md)
- [example-report.md](references/example-report.md)

## Next Best Skill

`fix-priority-ranker` · `content-quality-gate` (full) · `technical-site-check`
