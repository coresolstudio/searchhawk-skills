# SearchHawk Connectors

Every skill runs at **Tier 1** with zero dependencies — paste data, WebFetch, or bundled scripts.

## Tier model

| Tier | Integration | Experience |
|------|-------------|----------|
| **1** | None + scripts below | URL fetch, paste, local Python |
| **2** | GSC, GA4, PSI API keys | Your authenticated data |
| **3** | MCP (Ahrefs, Semrush, etc.) | Full automation |

## MCP (Tier 3)

[.mcp.json](.mcp.json) ships an optional reference `fetch` server (`uvx mcp-server-fetch`)
so MCP hosts — Claude Code/Desktop, Abacus AI, LibreChat, and others — can pull live page
data when the Python connectors can't run. Add your own SEO MCP servers (Ahrefs, Semrush,
GSC) to the same file for full Tier 3 automation; skills reference them via the
`~~category` placeholders below. Per-host setup: [docs/HOSTS.md](docs/HOSTS.md).

## Bundled scripts (stdlib Python)

Run from repository root. See [scripts/connectors/README.md](scripts/connectors/README.md).

| Script | Command | Purpose |
|--------|---------|---------|
| **onpage.py** | `python3 scripts/connectors/onpage.py <url>` | Title, meta, H1/H2, canonical, JSON-LD types |
| **suggest.py** | `python3 scripts/connectors/suggest.py "seed" --expand` | Google Autocomplete ideas (⚠️ unofficial) |
| **crawl.py** | `python3 scripts/connectors/crawl.py <url> --max-pages 20` | Same-host BFS crawl records |
| **linkgraph.py** | `python3 scripts/connectors/linkgraph.py crawl.json` | Orphans, depth, internal PageRank |
| **robots.py** | `python3 scripts/connectors/robots.py <url> --check-ai-bots` | robots.txt + AI bot flags |
| **schema_lint.py** | `python3 scripts/connectors/schema_lint.py <url>` | JSON-LD extract + validate |
| **sitemap.py** | `python3 scripts/connectors/sitemap.py <url>` | Sitemap index, llms.txt URL discovery |
| **psi.py** | `python3 scripts/connectors/psi.py <url>` | PageSpeed Insights + Core Web Vitals |

## Placeholder categories

Skills use `~~category` placeholders — swap for your tool or free alternative:

| Placeholder | Paid examples | Free alternative |
|-------------|---------------|------------------|
| `~~SEO tool` | Ahrefs, Semrush | GSC export + suggest.py |
| `~~search console` | GSC | GSC API / CSV paste |
| `~~analytics` | GA4 | GA4 export |
| `~~page speed tool` | GTmetrix | psi.py (PageSpeed Insights) |
| `~~AI monitor` | Otterly | ai-citation-checker protocol |

## Skill → script map

| Skill | Scripts |
|-------|---------|
| topic-keyword-finder | suggest.py |
| site-search-audit, technical-site-check | crawl.py, robots.py, onpage.py, sitemap.py, psi.py |
| page-audit | onpage.py, psi.py |
| internal-links-helper | crawl.py → linkgraph.py |
| schema-helper | schema_lint.py |
| performance-snapshot, change-alerts | psi.py (optional) |

## Environment variables (optional)

`PAGESPEED_API_KEY` (PSI — recommended for automation), `AHREFS_API_KEY` (MCP) — never required for Tier 1.
