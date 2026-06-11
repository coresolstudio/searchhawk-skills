---
name: audit
description: "Audit SEO, AEO, GEO, technical health, and quality gates."
argument-hint: "<url> [--full|--tech|--quality|--trust]"
---

# /searchhawk:audit

| Flag | Skills |
|------|--------|
| default | site-search-audit or page-audit |
| --tech | technical-site-check |
| --quality | content-quality-gate |
| --trust | domain-trust-check |
| --full | site-search-audit + technical + content-quality-gate + domain-trust-check |

Then `fix-priority-ranker`.
