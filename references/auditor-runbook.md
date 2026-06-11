# SearchHawk Auditor Runbook

For `content-quality-gate` and `domain-trust-check`.

## §1 Handoff schema (authoritative)

Auditor handoffs MUST include:

```yaml
status: DONE | BLOCKED | NEEDS_INPUT
verdict: SHIP|FIX|BLOCK  # or TRUSTED|CAUTIOUS|UNTRUSTED
cap_applied: boolean
raw_overall_score: number
final_overall_score: number
veto_items: []
top_fixes: []
evidence_mode: Measured|Mixed|Estimated
```

## §2 Critical fail cap

If ≥5 items score 0 in any single letter group (T/R/U/S/H/M or Authority section), cap final score at 60 and set `cap_applied: true`.

## §3 Evidence gate

BLOCK and UNTRUSTED require cited evidence URLs or quoted page text. FIX and CAUTIOUS may proceed with partial crawl if labeled DONE_WITH_CONCERNS.

## §4 Publish coupling

No skill may declare publish-ready unless:

1. `content-quality-gate` verdict = SHIP
2. `cap_applied: false`
3. No open veto items

Domain pages additionally recommend `domain-trust-check` TRUSTED or CAUTIOUS with documented gaps.

## §5 Cross-session rule

When project-memory is active, load prior auditor handoffs from `memory/audits/` before re-auditing same URL.
