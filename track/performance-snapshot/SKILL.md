---
name: performance-snapshot
description: >
  Use to summarize traffic and search performance from GA4/GSC exports — trends,
  top pages, queries, anomalies — and to generate a styled HTML stakeholder
  report (executive, technical, or client audience).
version: "2.1.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
homepage: "https://seometahawk.com/searchmetahawk-skills"
when_to_use: "Performance report, traffic summary, GSC report, monthly report, stakeholder dashboard, report for my boss/client."
argument-hint: "<domain> [--period range] [--html] [--audience executive|technical|client]"
metadata:
  product: SearchHawk Skills
  tagline: "SEO · AEO · GEO for AI assistants"
---

# Performance Snapshot

Summarizes search performance from pasted GA4/GSC exports or connected tools, and
optionally renders a **self-contained styled HTML report** for stakeholders.

## Skill Contract

- **Reads:** current + prior-period metrics (traffic, queries, rankings, AI citations),
  report audience, date range.
- **Writes:** markdown summary in chat, and — when asked — an HTML report file.
- **Done when:** every in-scope section is present or marked "Not yet evaluated",
  every metric is source-tagged, and anomalies carry a recommended next skill.

## Decision Gates

**Stop and ask when:** no reporting period or comparison period can be determined —
offer (1) last 28 days vs prior 28, (2) last calendar month vs prior, (3) custom range.

**Continue silently when:** a section's data is missing — mark it "Not yet evaluated"
and move on. Never fabricate a metric. Audience not stated — default to executive.

## Source tagging

Label every metric **Measured** (export/API/script), **User-provided**, or
**Estimated** (model inference). Never present an estimate as measured. Separate an
observed change from its plausible explanation — corroborate before stating a cause.

## Instructions

1. **Parameters** — domain, period, comparison period, audience, data freshness.
2. **Executive summary** — overall rating, wins, watch areas, required actions.
3. **Metrics at a glance** — clicks, impressions, CTR, top-10 keywords, AI citations;
   each with prior value and delta.
4. **Top queries / landing pages** — tables with period-over-period deltas.
5. **Anomalies** — observed change, likely cause (corroborated), next skill.
6. **Recommendations** — action, priority, expected impact, owner, next skill.

### HTML report option

When the user wants a shareable/"beautiful" report, build a JSON payload and render it:

```bash
python3 scripts/connectors/report_html.py --sample > report.json   # payload schema
# fill report.json with real, source-tagged data, then:
python3 scripts/connectors/report_html.py report.json -o report.html
python3 scripts/connectors/report_html.py report.json --theme dark
```

The output is a single HTML file (inline CSS + SVG charts, no external assets) —
safe to email, attach, or host. Metric cards auto-compute deltas from
`value`/`previous`; use `"delta"`/`"direction"` keys to override. Mark missing
sections `"status": "not-evaluated"` rather than omitting them.

Optional CWV baseline: `python3 scripts/connectors/psi.py <url>`.

## Reference Materials

- [example-report.md](references/example-report.md)
- [report-templates.md](references/report-templates.md) — audience templates (executive / technical / client)

## Next Best Skill

Decaying page found → `content-updater` · recurring monitoring → `change-alerts` ·
prioritize fixes → `fix-priority-ranker` · save findings → `project-memory`
