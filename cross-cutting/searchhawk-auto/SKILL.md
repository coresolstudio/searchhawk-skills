---
name: searchhawk-auto
description: >
  SearchHawk router for SEO, AEO, GEO goals. Routes to the smallest skill chain from 24 skills.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
when_to_use: "Any search visibility goal without naming a skill."
argument-hint: "<goal> [--deep]"
metadata:
  product: SearchHawk Skills
---

# SearchHawk Auto

Follow [searchhawk-product-api.md](../../references/searchhawk-product-api.md) and [evals/searchhawk-scenarios.md](../../evals/searchhawk-scenarios.md).

## Mode commands (logical)

| Mode | Skills |
|------|--------|
| research | topic-keyword-finder, serp-reviewer, competitor-snapshot, content-gap-finder |
| audit | site-search-audit, page-audit, technical-site-check, content-quality-gate, domain-trust-check |
| create | search-content-writer, answer-content-optimizer, ai-friendly-content-optimizer, meta-tags-helper, schema-helper, content-updater |
| track | rank-monitor, ai-citation-checker, performance-snapshot, change-alerts, project-memory |

`--deep`: plan phases → full audit chain → fix-priority-ranker → create → content-quality-gate

## Output

Execution summary: steps, evidence, blockers, next action.

## Reference Materials

- [example-report.md](references/example-report.md)
