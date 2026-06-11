# Example: Performance Snapshot

**Domain:** homebrewbeans.com · **Period:** Last 28 days vs prior 28 · **Date:** 2026-06-11  
**Sources:** User-pasted GSC + GA4 exports (Measured)

## Executive Summary

Organic clicks **+12%** period-over-period. Impressions flat. CTR improved on 4 branded queries. Non-brand clicks down on 2 money pages — likely ranking slip, not seasonality.

## Top Queries (GSC)

| Query | Clicks | Δ | Avg position |
|-------|--------|---|--------------|
| homebrew beans | 842 | +5% | 1.2 |
| best espresso under 500 | 118 | −22% | 14.1 |
| descale breville barista | 76 | +18% | 6.4 |

## Top Landing Pages (GA4 organic)

| Page | Sessions | Δ | Bounce |
|------|----------|---|--------|
| / | 3,210 | +8% | 42% |
| /guides/best-espresso-under-500 | 890 | −31% | 58% |
| /guides/descale-breville | 412 | +24% | 39% |

## Anomalies

| Anomaly | Likely cause | Action |
|---------|--------------|--------|
| /guides/best-espresso-under-500 drop | Content decay + SERP refresh | `content-updater` |
| CTR up on brand terms | Sitelinks stable | Monitor only |
| New query cluster "gaggia classic pro" | Emerging intent | `topic-keyword-finder` |

## Handoff Summary

- **Status:** DONE
- **Recommended next skill:** `content-updater` on decaying URL → `fix-priority-ranker`
