# SearchHawk Skill Contract

One operating system across all SearchHawk skills. Every `SKILL.md` exposes these sections.

## Required sections

- `Quick Start` — shortest valid invocation + output expectation
- `Skill Contract` — Reads, Writes, Promotes, Done when, Primary next skill
- `Handoff Summary` — standard format below
- `Data Sources` — Tier 1 paste/URL; Tier 2 optional tools (see CONNECTORS.md)
- `Instructions` — phased workflow with `[Phase X/N]` announcements
- `Reference Materials` — links to `references/` in skill folder
- `Next Best Skill` — one primary + optional alternates

## Auditor-class skills

`content-quality-gate` and `domain-trust-check` additionally require:

- `When This Must Trigger`
- `Validation Checkpoints`
- Inline runbook from [auditor-runbook.md](auditor-runbook.md)

Gate verdicts:

- **content-quality-gate**: SHIP / FIX / BLOCK
- **domain-trust-check**: TRUSTED / CAUTIOUS / UNTRUSTED

## Handoff Summary format

```markdown
### Handoff Summary

- **Status**: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_INPUT
- **Objective**: what was analyzed or created
- **Key Findings / Output**: highest-signal result
- **Evidence**: URLs or data reviewed (Measured / User-provided / Estimated)
- **Assumptions**: inferences made, or "none"
- **Open Loops**: blockers, missing inputs
- **Recommended Next Skill**: one primary move
```

Auditor extensions: `cap_applied`, `raw_overall_score`, `final_overall_score`

## Data labeling

Every metric: **Measured** | **User-provided** | **Estimated** | **N/A**

Never present Estimated as Measured.

## Promotion rules

Promote to `memory/` only durable facts: priorities, approved decisions, entity names, recurring blockers.

Do not promote: raw logs, speculation, unverified competitor claims.

## Termination rules

1. Visited-set: if next skill already ran this chain, STOP
2. Default max-depth: 3 handoffs
3. Ambiguity: stop and present options

## Output voice

Banned filler: "crucial", "leverage", "delve", "landscape" (metaphorical), "comprehensive" (unless checklist-complete).

Lead with findings. Name data sources. Short paragraphs.

## Save results

After delivery, ask: "Save these results for future sessions?"

Write dated summary to skill's memory path: `memory/{category}/YYYY-MM-DD-{slug}.md`
