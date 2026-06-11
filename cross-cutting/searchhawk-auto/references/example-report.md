# Example: SearchHawk Auto Router

**Input:** "Audit https://homebrewbeans.com — what should I fix first?"  
**Date:** 2026-06-11 · **Mode:** audit (default)

## Execution Summary

| Step | Skill | Outcome |
|------|-------|---------|
| 1 | `site-search-audit` | SEO 62 · AEO 48 · GEO 41 |
| 2 | `technical-site-check` | 3 HIGH issues (sitemap orphans, slow LCP, missing FAQ schema) |
| 3 | `fix-priority-ranker` | Top 5 fixes ordered by impact × effort |

## Evidence Used

- `onpage.py` on homepage + 2 sample URLs
- `robots.py --check-ai-bots` — GPTBot allowed
- User goal: fix-first, not full content rewrite

## Blockers

None — Tier 1 data sufficient for ranked fix list.

## Recommended Next Action

Run `internal-links-helper` on homebrewbeans.com to address orphan product pages (HIGH #2).

## Handoff Summary

- **Status:** DONE
- **Primary next skill:** `internal-links-helper`
- **Deep mode available:** `--deep` would add `content-quality-gate` before create phase
