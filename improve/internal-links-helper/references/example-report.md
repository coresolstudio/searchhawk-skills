# Example: Internal Links Helper

**Domain:** homebrewbeans.com · **Crawl:** 47 pages · **Date:** 2026-06-11

## Graph Summary (linkgraph.py)

| Metric | Value |
|--------|-------|
| Pages crawled | 47 |
| Orphan pages | 6 |
| Deep pages (>3 clicks) | 11 |
| Max depth | 5 |

## Top PageRank URLs

| URL | In | Out | PR |
|-----|----|----|-----|
| / | 38 | 12 | 0.18 |
| /products | 22 | 8 | 0.11 |
| /guides/espresso-care | 4 | 6 | 0.06 |

## Orphan Pages (no internal in-links)

| URL | Suggested hub | Priority |
|-----|---------------|----------|
| /products/breville-barista-pro | /products + /guides/espresso-care | HIGH |
| /guides/water-hardness | /guides/espresso-care | MED |
| /blog/2023-holiday-blend | /blog or archive hub | LOW |

## Recommendations

| From | To | Anchor text |
|------|-----|-------------|
| /guides/descale-breville | /guides/espresso-care | full espresso machine care guide |
| / | /products/breville-barista-pro | Breville Barista Pro review |
| /products | /guides/water-hardness | how water hardness affects espresso |

## Priority Table

| Action | Impact | Effort | Order |
|--------|--------|--------|-------|
| Rescue 3 product orphans from /products | HIGH | LOW | 1 |
| Link care guides into hub/spoke | HIGH | MED | 2 |
| Reduce depth on 4 blog posts | MED | LOW | 3 |

## Handoff Summary

- **Status:** DONE
- **Recommended next skill:** `fix-priority-ranker`
