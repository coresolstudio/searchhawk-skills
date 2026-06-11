---
name: page-audit
description: >
  Use for single-URL on-page audit across SEO, AEO, and GEO signals.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
when_to_use: "Audit this page, check this URL."
argument-hint: "<url>"
allowed-tools: WebFetch
metadata:
  product: SearchHawk Skills
---

# Page Audit

Signal table: Signal | Status | Finding | Fix. Scores SEO/AEO/GEO 1–10.

Run onpage.py for structured extract. Hand off to improve skills per failure.

## Next Best Skill

`content-quality-gate` before publish.
