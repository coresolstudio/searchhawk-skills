---
name: content-quality-gate
description: >
  Use before publish or when auditing content quality across SEO, AEO, and GEO. Runs 60-item Hawk-Trust benchmark with veto checks. Not for domain-only trust — use domain-trust-check.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
homepage: "https://seometahawk.com/searchmetahawk-skills"
when_to_use: "Content quality audit, publish gate, E-E-A-T check, Hawk-Trust."
argument-hint: "<URL or pasted content> [keyword]"
allowed-tools: WebFetch
class: auditor
metadata:
  product: SearchHawk Skills
  tagline: "SEO · AEO · GEO for AI assistants"
---

# Content Quality Gate

Hawk-Trust (HTF) 60-item protocol gate.

## When This Must Trigger

- User asks publish-ready / quality audit / E-E-A-T
- Before any publish-ready claim from create skills
- YMYL topics

## Skill Contract

- **Writes**: scored audit, verdict SHIP/FIX/BLOCK, veto list
- **Done when**: all HTF items scored or N/A with evidence; handoff includes cap fields

## Instructions

1. Fetch or parse content
2. Score [hawk-trust-benchmark.md](../../references/hawk-trust-benchmark.md) — 0/1/2 per item
3. Apply [auditor-runbook.md](../../references/auditor-runbook.md)
4. Output verdict + top 5 fixes

### Handoff Summary

Include `cap_applied`, `raw_overall_score`, `final_overall_score`, `verdict`.

## Reference Materials

- [hawk-trust-benchmark.md](../../references/hawk-trust-benchmark.md)
- [auditor-runbook.md](../../references/auditor-runbook.md)

## Next Best Skill

FIX → relevant improve skill. BLOCK → user must resolve vetoes.
