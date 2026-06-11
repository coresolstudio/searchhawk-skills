---
name: fix-priority-ranker
description: >
  Use after audits to rank fixes by effort (S/M/L) and impact. Surfaces quick wins first.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
when_to_use: "What to fix first, priorities, quick wins."
argument-hint: "<findings-or-url>"
metadata:
  product: SearchHawk Skills
---

# Fix Priority Ranker

## Skill Contract

- **Done when**: ordered table with effort, impact, pillar (SEO/AEO/GEO), and "if you only do 3" list

## Instructions

1. Ingest audit/findings
2. Tag effort S/M/L and impact High/Med/Low
3. Sort: S+High first
4. Avoid generic advice — tie to evidence

## Next Best Skill

Top item's matching improve/diagnose skill.
