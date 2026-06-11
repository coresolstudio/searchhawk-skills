# Example: Change Alerts

**Domain:** homebrewbeans.com · **Baseline:** June 2026 audit · **Date:** 2026-06-11

## Alert Configuration

| Alert ID | Metric | Threshold | Window | Channel |
|----------|--------|-----------|--------|---------|
| A1 | Primary keyword rank | Drop ≥ 5 positions | 7 days | Email |
| A2 | GSC clicks (site) | Drop ≥ 20% WoW | 7 days | Email |
| A3 | Indexed pages | Change ± 10% | 14 days | Slack |
| A4 | AI brand mention | 0 → any on 3 test prompts | 30 days | Manual review |
| A5 | Core Web Vitals | LCP needs-improvement | 30 days | Email |

## Baseline Values (Measured)

| Metric | Current | Source |
|--------|---------|--------|
| "best espresso under 500" rank | 14 | User rank export |
| Weekly GSC clicks | 1,240 | GSC paste |
| Indexed URLs | 186 | GSC coverage |
| PSI mobile LCP (lab) | 3.1s | psi.py |

## Notification Checklist

- [ ] GSC email alerts enabled for coverage + manual actions
- [ ] Rank tracker export scheduled weekly (user tool)
- [ ] `ai-citation-checker` re-run monthly for A4
- [ ] `psi.py` monthly for A5 (set `PAGESPEED_API_KEY`)

## Escalation Rules

| Severity | Trigger | Response |
|----------|---------|----------|
| CRITICAL | A2 + A1 same week | `site-search-audit` within 48h |
| HIGH | A3 indexed drop | `technical-site-check` |
| MED | A5 CWV slip | Page-level `page-audit` |

## Handoff Summary

- **Status:** DONE
- **Recommended next skill:** `rank-monitor` for ongoing rank baselines
