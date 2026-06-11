---
name: technical-site-check
description: >
  Use for technical SEO: crawlability, indexation, robots, sitemap, canonicals, HTTPS, Core Web Vitals signals, mobile, and structured data exposure.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
homepage: "https://seometahawk.com/searchmetahawk-skills"
when_to_use: "Technical SEO audit, crawl issues, indexation, robots.txt, Core Web Vitals."
argument-hint: "<domain-or-url>"
allowed-tools: WebFetch
metadata:
  product: SearchHawk Skills
  tagline: "SEO · AEO · GEO for AI assistants"
---

# Technical Site Check

Deep technical SEO diagnosis.

## Skill Contract

- **Done when**: checklist with pass/fail/partial for crawl, index, speed (or N/A with tool named), mobile, security
- **Primary next skill**: `fix-priority-ranker`

## Instructions — 7 phases

1. Fetch robots.txt, sitemap.xml, llms.txt if present
2. Indexation — noindex patterns, canonical samples
3. Crawl budget signals — orphan risk (sitemap vs nav)
4. HTTPS / redirects (sample)
5. CWV — PSI if available else N/A + recommend PageSpeed Insights
6. Schema exposure sitewide sample
7. Report with severity CRITICAL/HIGH/MED/LOW

Run `python3 scripts/connectors/crawl.py <url> --max-pages 30`, `robots.py`, `sitemap.py`, `psi.py`, and `onpage.py` on samples.

## Reference Materials

- [instructions-detail.md](references/instructions-detail.md)
- [example-report.md](references/example-report.md)

## Next Best Skill

`fix-priority-ranker` → `internal-links-helper`
