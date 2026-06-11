---
name: content-updater
description: >
  Use when refreshing decaying content: outdated stats, lost rankings, freshness signals, and AEO/GEO re-optimization.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
homepage: "https://seometahawk.com/searchmetahawk-skills"
when_to_use: "Refresh content, update old blog post, content decay."
argument-hint: "<URL>"
metadata:
  product: SearchHawk Skills
  tagline: "SEO · AEO · GEO for AI assistants"
---

# Content Updater

## 6 phases

1. Baseline — current content + user metrics if any
2. Decay signals — dates, broken links, outdated facts
3. SERP delta — what winners added (via serp-reviewer)
4. Update plan — sections to add/cut/rewrite
5. AEO/GEO pass — answer blocks + cite quotes
6. Re-gate — `content-quality-gate` before republish

## Reference Materials

- [example-report.md](references/example-report.md)
