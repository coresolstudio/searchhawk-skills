# Example: Project Memory

**Project:** homebrewbeans.com · **Session:** 2026-06-11

## HOT Cache (active context)

| Key | Value |
|-----|-------|
| site_url | https://homebrewbeans.com |
| primary_goal | Recover rankings on money guide |
| last_audit | SEO 62 · AEO 48 · GEO 41 (2026-06-11) |
| top_fix | Refresh `/guides/best-espresso-under-500` |
| open_loop | Internal link orphans (6 pages) |

## WARM Capture (dated summary)

```markdown
## 2026-06-11 — Audit + performance review

- Ran site-search-audit + performance-snapshot from GSC paste
- Decaying URL: best-espresso-under-500 (−34% clicks YoY)
- Orphan products need hub links from /products
- AI citation: brand mentioned 1/6 test prompts, 0 URL citations
- Next: content-updater → internal-links-helper
```

## Promoted Decisions (user-approved)

| Date | Decision |
|------|----------|
| 2026-06-11 | Prioritize content refresh over new posts this month |
| 2026-06-11 | Set PAGESPEED_API_KEY for monthly psi.py alerts |

## Query Response (recall)

**User asks:** "What were we fixing on my site?"

**Answer from memory:** Primary focus is refreshing the best-espresso-under-500 guide (rank 14, traffic down). Secondary: 6 orphan product pages need internal links from /products and the espresso-care hub.

## Handoff Summary

- **Status:** CAPTURED
- **Write path:** `memory/open-loops.md` (pending user confirm)
- **Recommended next skill:** `content-updater`
