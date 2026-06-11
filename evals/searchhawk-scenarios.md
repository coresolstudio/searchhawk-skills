# SearchHawk Eval Scenario Library v2.3

Routing contracts for `/searchhawk:auto` and mode commands. **35 scenarios** for regression testing.

## How to use

1. Run prompt through `searchhawk-auto` or named command
2. Check `expected_route`, `must_not`, and `pass_criteria`
3. Run connector smoke tests after script changes

---

## Discover (E1–E8)

### E1 — Site audit (default)
- **Input:** "Audit https://example.com for SEO, AEO, and GEO"
- **Route:** `site-search-audit` → `fix-priority-ranker`
- **Must not:** Flag missing pages without crawl; guarantee rankings
- **Pass:** SEO/AEO/GEO scores + evidence + handoff

### E2 — Keyword discovery
- **Input:** "What keywords should I target for home espresso machines?"
- **Route:** `topic-keyword-finder` → `serp-reviewer`
- **Must not:** Invent volume without Estimated label
- **Pass:** Clusters + 3 quick wins

### E3 — SERP-only
- **Input:** "What does Google show for 'best CRM for startups'?"
- **Route:** `serp-reviewer`
- **Pass:** Intent + snippet format + top results table

### E4 — Competitor battlecard
- **Input:** "Analyze competitors hubspot.com vs pipedrive.com for CRM content"
- **Route:** `competitor-snapshot` → `content-gap-finder`
- **Must not:** Unsupported competitor feature claims
- **Pass:** Battlecard + gap themes

### E5 — Content gaps only
- **Input:** "What topics is competitor.com covering that I'm not?"
- **Route:** `content-gap-finder`
- **Pass:** Prioritized gap table

### E6 — Local keyword research
- **Input:** "Keywords for plumber in Austin TX"
- **Route:** `topic-keyword-finder` (local modifiers)
- **Pass:** Local intent clusters flagged

### E7 — Long-tail expand
- **Input:** "Find long-tail keywords for vegan meal prep"
- **Route:** `topic-keyword-finder` (may use suggest.py)
- **Pass:** 10+ long-tail with intent tags

### E8 — SERP + write chain
- **Input:** "Research and outline a post about technical SEO"
- **Route:** `topic-keyword-finder` → `serp-reviewer` → `search-content-writer`
- **Must not:** Skip research and draft blindly

---

## Diagnose (E9–E16)

### E9 — Publish gate YMYL
- **Input:** "Is my health article ready to publish?" + URL
- **Route:** `content-quality-gate`
- **Risk gates:** ymyl, veto
- **Must not:** SHIP with unverified medical claims
- **Pass:** SHIP/FIX/BLOCK + Hawk-Trust scores

### E10 — Single page audit
- **Input:** "Audit this page: https://example.com/blog/post"
- **Route:** `page-audit`
- **Pass:** Signal table + 3 pillar scores

### E11 — Technical crawl
- **Input:** "Technical SEO check for example.com"
- **Route:** `technical-site-check`
- **Tools:** crawl.py, robots.py, onpage.py
- **Must not:** Guess Core Web Vitals
- **Pass:** Severity-rated findings

### E12 — Domain trust
- **Input:** "Is this domain trustworthy for finance content?" + domain
- **Route:** `domain-trust-check`
- **Pass:** TRUSTED/CAUTIOUS/UNTRUSTED verdict

### E13 — Quick vs full audit
- **Input:** "Quick audit my homepage example.com"
- **Route:** `site-search-audit` (Quick scope ~6 pages)
- **Pass:** Confirms Quick scope in output

### E14 — Schema lint preflight
- **Input:** "Validate structured data on https://example.com"
- **Route:** `schema-helper` + run `schema_lint.py`
- **Must not:** Promise rich results from schema alone
- **Pass:** JSON-LD errors/warnings listed

### E15 — Internal link orphans
- **Input:** "Find orphan pages on example.com"
- **Route:** `internal-links-helper`
- **Tools:** crawl.py | linkgraph.py
- **Pass:** Orphan list + hub recommendations

### E16 — AI bots robots check
- **Input:** "Are AI crawlers blocked on my site?"
- **Route:** `technical-site-check` or robots.py directly
- **Pass:** AI bot mention flags from robots.txt

---

## Decide & Improve (E17–E26)

### E17 — Fix priority
- **Input:** "What should I fix first on my site?" (after audit context)
- **Route:** `fix-priority-ranker`
- **Pass:** S/M/L effort + "if you only do 3"

### E18 — Featured snippet
- **Input:** "Optimize for snippet: what is technical SEO"
- **Route:** `serp-reviewer` → `answer-content-optimizer` → `schema-helper`
- **Pass:** 40–60w answer + FAQ draft

### E19 — GEO cite blocks
- **Input:** "Make this page citable in ChatGPT" + URL
- **Route:** `ai-friendly-content-optimizer`
- **Must not:** Claim site is already cited
- **Pass:** Quotable passage blocks

### E20 — Meta tags only
- **Input:** "Write title and meta for [URL/topic]"
- **Route:** `meta-tags-helper`
- **Pass:** 3 title + 3 meta variants

### E21 — FAQ schema
- **Input:** "Add FAQ schema for visible Q&A on [URL]"
- **Route:** `schema-helper`
- **Must not:** Hidden FAQ in schema only
- **Pass:** JSON-LD matches visible text

### E22 — Content refresh
- **Input:** "Refresh this URL — traffic dropped" + URL
- **Route:** `content-updater` → `content-quality-gate`
- **Must not:** Full rewrite without ask
- **Pass:** Section-level plan

### E23 — Write from brief
- **Input:** "Write a 1500-word guide on email deliverability"
- **Route:** `search-content-writer` → `publish-checklist`
- **Pass:** Draft + FAQ + meta

### E24 — Pre-publish quick gate
- **Input:** "Quick publish check before I go live"
- **Route:** `publish-checklist`
- **Pass:** 12-point Ready/Fix/Not ready

### E25 — Entity profile
- **Input:** "Set up my brand entity for AI search"
- **Route:** `entity-profile` → `schema-helper`
- **Pass:** Entity doc + Organization schema draft

### E26 — Internal link plan
- **Input:** "Improve internal linking for my blog"
- **Route:** `internal-links-helper`
- **Pass:** Hub/spoke plan with anchors

---

## Track (E27–E31)

### E27 — AI citation protocol
- **Input:** "Does ChatGPT mention my site for [query]?"
- **Route:** `ai-citation-checker`
- **Must not:** Observed without test data
- **Pass:** Prompt × engine table

### E28 — Rank tracking setup
- **Input:** "Track these 20 keywords for my domain"
- **Route:** `rank-monitor`
- **Pass:** Tracking template with baseline column

### E29 — Performance snapshot
- **Input:** "Summarize my GSC export for last 28 days"
- **Route:** `performance-snapshot`
- **Must not:** Mix Estimated with Measured
- **Pass:** Top queries/pages + anomalies

### E30 — Alert thresholds
- **Input:** "Alert me if rankings drop 5 positions"
- **Route:** `change-alerts`
- **Must not:** Enable external alerts without confirmation
- **Pass:** Threshold spec document

### E31 — Save project memory
- **Input:** "Remember my site is example.com, niche is B2B SaaS"
- **Route:** `project-memory`
- **Must not:** Write memory without user confirmation
- **Pass:** Confirms capture path

---

## Orchestration (E32–E35)

### E32 — Deep orchestration
- **Input:** "Full exhaustive audit and fix plan --deep"
- **Route:** `searchhawk-auto --deep`
- **Must not:** Auto-publish to CMS
- **Pass:** Phase plan + summary

### E33 — Research command
- **Input:** `/searchhawk:research CRM software for SMBs`
- **Route:** discover chain
- **Pass:** Does not jump to writing

### E34 — Audit command full
- **Input:** `/searchhawk:audit example.com --full`
- **Route:** site + technical + content-quality-gate
- **Pass:** Multi-skill summary

### E35 — Boundary reject
- **Input:** "Write me a Python web scraper"
- **Route:** Decline — outside SearchHawk scope
- **Pass:** Polite pack-boundary note

---

## Risk gate index

| Gate | When |
|------|------|
| `ymyl` | Health, finance, legal |
| `publish_ready` | Before SHIP |
| `schema_truth` | JSON-LD |
| `geo_claim` | AI citation promises |
| `data_gap` | Missing metrics |
| `technical_index` | Crawl/index changes |
| `memory_write` | project-memory |
| `external_effect` | Alerts, outreach, CMS |

---

## Connector smoke tests

```bash
python3 scripts/connectors/onpage.py https://example.com
python3 scripts/connectors/robots.py https://example.com --check-ai-bots
python3 scripts/connectors/crawl.py https://example.com --max-pages 5 --max-depth 2 -q 2>/dev/null | python3 linkgraph.py -
python3 scripts/connectors/suggest.py "seo audit" --expand
python3 scripts/connectors/schema_lint.py https://example.com --pretty
python3 scripts/connectors/sitemap.py https://example.com --limit 50
python3 scripts/connectors/psi.py https://example.com
```

**Pipeline test (link graph):**
```bash
python3 scripts/connectors/crawl.py https://example.com --max-pages 10 --quiet 2>/dev/null > /tmp/sh-crawl.json
python3 scripts/connectors/linkgraph.py /tmp/sh-crawl.json --top 5
```

Expected: JSON stdout; linkgraph shows orphans/depth/pagerank summary.

---

## Skill smoke prompts (quick)

| Skill | Prompt |
|-------|--------|
| topic-keyword-finder | Keywords for vegan meal prep |
| site-search-audit | Quick audit example.com |
| content-quality-gate | Hawk-Trust gate on [URL] |
| schema-helper | FAQ schema for [URL] |
| searchhawk-auto | Help me get found in Google and AI search |
