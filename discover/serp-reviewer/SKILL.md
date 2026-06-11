---
name: serp-reviewer
description: >
  Use when analyzing SERPs: ranking patterns, featured snippets, PAA, AI Overviews, and intent. Not for full site audits.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
when_to_use: "SERP analysis, featured snippet, who ranks for."
argument-hint: "<query> [your-url]"
allowed-tools: WebFetch
metadata:
  product: SearchHawk Skills
---

# SERP Reviewer

## Instructions — 6 phases

1. **Query context** — intent, geography, device
2. **Top results** — format, angle, domain types
3. **SERP features** — snippet, PAA, video, local, AI Overview (Observed/Estimated)
4. **Snippet anatomy** — holder, format, win strategy
5. **Barrier** — content depth, authority cues (Estimated)
6. **Playbook** — format to match + differentiation

## Reference Materials

- [instructions-detail.md](references/instructions-detail.md)
- [example-report.md](references/example-report.md)

## Next Best Skill

`answer-content-optimizer` or `search-content-writer`
