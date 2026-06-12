# Privacy

SearchHawk Skills is designed to be privacy-first.

## What the skill pack collects

**Nothing.** There is no telemetry, no analytics, no phone-home of any kind — in the
skills, the commands, the installer, or the connector scripts.

## What stays on your machine

- All audit inputs and outputs (pasted GSC/GA4 exports, crawl results, reports).
- Project memory created by `protocol/project-memory` (plain local files).
- Optional API keys (`PAGESPEED_API_KEY`) read from your environment and used only for
  the request you trigger.

## Network requests the connectors make

Connector scripts contact only the targets you specify:

| Script | Talks to |
|--------|----------|
| `onpage.py`, `crawl.py`, `robots.py`, `schema_lint.py`, `sitemap.py` | The URL/site you pass in |
| `suggest.py` | Google Autocomplete endpoint (unofficial) |
| `psi.py` | Google PageSpeed Insights API |

No request includes anything beyond the URL/keyword you provide and standard HTTP headers.

## Your AI assistant is its own party

When you run these skills inside Cursor, Claude, Codex, Abacus AI, or any other host,
the content you share is processed under **that provider's** privacy policy. This
project adds no additional data flows on top.

## Questions

Open an issue or reach us via [coresolstudio.com](https://coresolstudio.com/).
