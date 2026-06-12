# SearchHawk Connectors

Every skill runs at **Tier 1** with zero dependencies — paste data, WebFetch, or bundled scripts.

## Tier model

| Tier | Integration | Experience |
|------|-------------|----------|
| **1** | None + scripts below | URL fetch, paste, local Python |
| **2** | GSC, GA4, PSI API keys | Your authenticated data |
| **3** | MCP (Ahrefs, Semrush, etc.) | Full automation |

## MCP (Tier 3)

[.mcp.json](.mcp.json) ships a reference `fetch` server (`uvx mcp-server-fetch`) plus
official **remote HTTP MCP endpoints** for the major SEO platforms — auth happens
interactively (OAuth or API key) on first use, nothing runs locally:

| Vendor | Endpoint | Auth | Typical tools |
|--------|----------|------|---------------|
| Ahrefs | `https://api.ahrefs.com/mcp/mcp` | API key (Lite+ plan) | keywords, backlinks, site audit |
| Semrush | `https://mcp.semrush.com/v1/mcp` | OAuth / API key | organic & keyword research, backlinks |
| SE Ranking | `https://api.seranking.com/mcp` | OAuth / API key | keywords, AI-search visibility |
| SISTRIX | `https://api.sistrix.com/mcp` | OAuth / Bearer | domain, keyword, links, AI modules |
| SimilarWeb | `https://mcp.similarweb.com` | OAuth / key | traffic estimates, competitive intel |

MCP is never required — every skill runs at Tier 1 with pasted data. For free
first-party data via local MCP, add Google's official
[Analytics MCP](https://github.com/googleanalytics/google-analytics-mcp) (`pipx run analytics-mcp`)
or the community [GSC MCP](https://github.com/AminForou/mcp-gsc) with your own Google
credentials. Per-host setup: [docs/HOSTS.md](docs/HOSTS.md).

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
| **report_html.py** | `python3 scripts/connectors/report_html.py report.json` | Styled self-contained HTML report (cards, charts, recommendations) |

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
| performance-snapshot, change-alerts | psi.py (optional), report_html.py |

## Environment variables (optional)

`PAGESPEED_API_KEY` (PSI — recommended for automation), `AHREFS_API_KEY` (MCP) — never required for Tier 1.
