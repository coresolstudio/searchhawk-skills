# Report Templates by Audience

One reporting shape everywhere: **metric table → what changed → why it matters → next action.**

| Convention | Rule |
|------------|------|
| Status | `On track` · `Watch` · `Off track` · `N/A` |
| Delta | Absolute + percentage when possible |
| Missing input | `Not yet evaluated` + pointer to next-best skill |
| Source tag | Every metric: Measured / User-provided / Estimated |

## Executive (default)

Lead with outcomes; keep to one screen. Trends + actions, no methodology.

```markdown
# Search Performance — [domain] · [period]
**Overall:** [Excellent/Good/Watch/Critical]

| Metric | Current | Previous | Δ | Status |
|--------|---------|----------|---|--------|
| Organic clicks | | | | |
| Keywords top 10 | | | | |
| AI citations | | | | |

**Wins:** … · **Watch:** … · **Action required:** …
```

## Technical

Add causes, owners, and evidence. Include crawl/CWV data, per-URL deltas,
and the script or export each figure came from.

```markdown
## Anomalies
| Observed change | Evidence | Likely cause (corroborated?) | Owner | Next skill |
|-----------------|----------|------------------------------|-------|------------|
```

## Client

Executive shape plus: period-over-period narrative in plain language, work
completed this period, work planned next period, and a glossary for any
metric a non-SEO reader would not know.

## HTML rendering

All three audiences render through the same generator:

```bash
python3 scripts/connectors/report_html.py --sample > report.json
python3 scripts/connectors/report_html.py report.json -o report.html
```

Payload fields map 1:1 to the sections above: `metrics` (cards), `highlights`
(wins/watch/actions), `sections` (tables, bar charts, text), `recommendations`
(priority/action/impact/owner/skill). Set `"status": "not-evaluated"` on any
section without data.
