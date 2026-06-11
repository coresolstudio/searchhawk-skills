---
name: project-memory
description: >
  Use to save, query, promote, and archive SearchHawk project context across sessions: site URL, keywords, audit verdicts, decisions.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
homepage: "https://github.com/searchhawk/skills"
when_to_use: "Remember my site, save audit, project memory, recall last analysis."
metadata:
  product: SearchHawk Skills
  tagline: "SEO · AEO · GEO for AI assistants"
---

# Project Memory

HOT/WARM/COLD lifecycle per [state-model.md](../../references/state-model.md).

## Operations

- **capture** — write dated summary to WARM path
- **query** — read hot-cache + relevant WARM files
- **promote** — user-approved items to decisions.md
- **archive** — monthly rollup

Requires user confirmation before writes.

## Reference Materials

- [example-report.md](references/example-report.md)
