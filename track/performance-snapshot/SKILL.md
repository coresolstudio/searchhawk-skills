---
name: performance-snapshot
description: >
  Use to summarize traffic and search performance from GA4/GSC exports: trends, top pages, queries, and anomalies.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
homepage: "https://github.com/searchhawk/skills"
when_to_use: "Performance report, traffic summary, GSC report."
argument-hint: "<domain> [--period range]"
metadata:
  product: SearchHawk Skills
  tagline: "SEO · AEO · GEO for AI assistants"
---

# Performance Snapshot

Requires pasted GA4/GSC export or API data. Optional: `python3 scripts/connectors/psi.py <url>` for CWV baseline.

Output: executive summary, top queries/pages, anomalies, recommended next skills.

## Reference Materials

- [example-report.md](references/example-report.md)
