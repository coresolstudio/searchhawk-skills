---
name: internal-links-helper
description: >
  Use for internal link architecture: orphan pages, hub/spoke structure, anchor
  text, click depth, PageRank-style priority. Uses crawl.py + linkgraph.py. Not
  for external backlinks.
version: "2.1.0"
when_to_use: "Internal linking, orphan pages, site architecture, link equity."
argument-hint: "<domain> [--top N]"
metadata:
  product: SearchHawk Skills
---

# Internal Links Helper

## Connector pipeline

```bash
python3 scripts/connectors/crawl.py https://example.com --max-pages 50 --quiet > crawl.json
python3 scripts/connectors/linkgraph.py crawl.json --top 15
```

## Instructions — 5 phases

1. **Crawl** — same-host BFS (or use user sitemap export)
2. **Graph** — orphans, deep pages (>3 clicks), depth histogram, top PageRank URLs
3. **Hub map** — identify pillar pages from high in-degree + strategic value
4. **Recommendations** — source URL → target URL + anchor text
5. **Priority table** — impact (orphan rescue, depth reduction) × effort

See [references/link-patterns.md](references/link-patterns.md) and [example-report.md](references/example-report.md).

## Next Best Skill

`fix-priority-ranker` for ordered implementation list
