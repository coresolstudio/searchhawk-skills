# SearchHawk Skills

**SearchHawk Skills v2.3** — SEO · AEO · GEO for AI assistants

Original skill pack with **25 skills**, **5 commands**, Hawk-Trust / Hawk-Authority benchmarks, **8 connector scripts**, **35 eval scenarios**, **25 example reports**, and project memory.

[![Version](https://img.shields.io/badge/version-2.3.0-orange)]()
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-25-blue)]()

## Quick start

```bash
git clone https://github.com/creativehassan/searchhawk-skills.git
cd searchhawk-skills
chmod +x install.sh && ./install.sh
```

Restart Cursor. Try:

```text
/searchhawk:auto audit https://example.com
Research keywords for [topic]
What should I fix first on my site?
Run Hawk-Trust quality gate on [URL]
```

## Skills (25)

| Phase | Skills |
|-------|--------|
| **Router** | `searchhawk-auto`, `publish-checklist` |
| **Discover** | `topic-keyword-finder`, `serp-reviewer`, `competitor-snapshot`, `content-gap-finder` |
| **Diagnose** | `site-search-audit`, `page-audit`, `technical-site-check` |
| **Decide** | `fix-priority-ranker` |
| **Improve** | `search-content-writer`, `answer-content-optimizer`, `ai-friendly-content-optimizer`, `meta-tags-helper`, `schema-helper`, `internal-links-helper`, `content-updater` |
| **Track** | `rank-monitor`, `ai-citation-checker`, `performance-snapshot`, `change-alerts` |
| **Protocol** | `content-quality-gate` (Hawk-Trust 60), `domain-trust-check` (Hawk-Authority 35), `entity-profile`, `project-memory` |

## Commands

| Command | Use for |
|---------|---------|
| `/searchhawk:auto` | Natural-language router |
| `/searchhawk:research` | Keywords, SERP, competitors, gaps |
| `/searchhawk:audit` | Site/page/technical/quality/trust |
| `/searchhawk:create` | Write, optimize, meta, schema |
| `/searchhawk:track` | Rankings, AI citations, reports |

## Frameworks

| Framework | Items | Skill |
|-----------|-------|-------|
| **Hawk-Trust (HTF)** | 60 | `content-quality-gate` |
| **Hawk-Authority (HAF)** | 35 | `domain-trust-check` |

See [references/hawk-trust-benchmark.md](references/hawk-trust-benchmark.md).

## Architecture

```text
Discover → Diagnose → Decide → Improve → Track
              ↓
     content-quality-gate + domain-trust-check
              ↓
         project-memory
```

## Connectors & scripts

Tier 1 works with URL + paste only. Bundled stdlib scripts:

```bash
python3 scripts/connectors/onpage.py https://example.com
python3 scripts/connectors/suggest.py "your topic" --expand
python3 scripts/connectors/crawl.py https://example.com --max-pages 20 --quiet > crawl.json
python3 scripts/connectors/linkgraph.py crawl.json --top 10
python3 scripts/connectors/schema_lint.py https://example.com --pretty
python3 scripts/connectors/sitemap.py https://example.com --limit 100
python3 scripts/connectors/psi.py https://example.com
```

See [CONNECTORS.md](CONNECTORS.md) and [scripts/connectors/README.md](scripts/connectors/README.md).

## Eval scenarios

Test routing and quality after skill changes: [evals/searchhawk-scenarios.md](evals/searchhawk-scenarios.md) (**35 scenarios**)

## Install

```bash
./install.sh          # Cursor (~/.cursor/skills)
./install.sh --all    # Cursor + Claude
```

## License

MIT — see [LICENSE](LICENSE).
