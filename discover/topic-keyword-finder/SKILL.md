---
name: topic-keyword-finder
description: >
  Use when the user asks to find keywords, topic ideas, search volume, or what to write about. Prioritizes intent, difficulty, clusters, and AEO/GEO opportunities. Not for competitor gap lists — use content-gap-finder.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
homepage: "https://seometahawk.com/searchmetahawk-skills"
when_to_use: "Keyword research, topic clusters, what should I write about, long-tail keywords."
argument-hint: "<topic> [market/language]"
metadata:
  product: SearchHawk Skills
  tagline: "SEO · AEO · GEO for AI assistants"
---

# Topic & Keyword Finder

Discovers, scores, and clusters keywords for SEO, AEO, and GEO planning.

## Quick Start

```
Research keywords for [topic/product/service]
Find long-tail keywords for [niche] in [country]
```

## Skill Contract

- **Reads**: seed topic, audience, goal, market, optional DR/metrics
- **Writes**: prioritized keyword brief + handoff summary
- **Promotes**: pillar keywords, cluster names to `memory/research/`
- **Done when**: each shortlisted keyword has intent + difficulty + opportunity label; 3+ Quick Win / Growth / AEO flags
- **Primary next skill**: `competitor-snapshot`

### Handoff Summary

Emit format from [references/skill-contract.md](../../references/skill-contract.md).

## Data Sources

Tier 1: user seeds, site content, `~~SEO tool` paste, `python3 scripts/connectors/suggest.py "<seed>" --expand`. Tier 2: GSC. See [CONNECTORS.md](../../CONNECTORS.md).

## Instructions

Run 8 phases — announce `[Phase X/8: Name]`:

1. **Scope** — product, audience, goal, geography, language
2. **Discover** — seeds from problem/solution/audience terms
3. **Expand** — modifiers, questions, comparisons, long-tail
4. **Classify** — informational / commercial / transactional / navigational
5. **Score** — difficulty 1–100; Opportunity = (Volume × IntentValue) / Difficulty (label Estimated if no volume)
6. **AEO flag** — questions, definitions, lists, how-tos
7. **GEO flag** — cite-worthy definitional queries
8. **Deliver** — Executive Summary, clusters, calendar, next steps

Label every metric **Measured / User-provided / Estimated / N/A**.

> Detail: [references/instructions-detail.md](references/instructions-detail.md)

## Reference Materials

- [instructions-detail.md](references/instructions-detail.md)
- [keyword-intent-taxonomy.md](references/keyword-intent-taxonomy.md)
- [topic-cluster-templates.md](references/topic-cluster-templates.md)
- [example-report.md](references/example-report.md)

## Next Best Skill

Primary: `competitor-snapshot`. Also: `serp-reviewer`, `content-gap-finder`.
