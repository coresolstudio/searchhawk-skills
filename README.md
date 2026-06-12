# SearchHawk Skills

**25 skills. 5 commands. SEO · AEO · GEO for AI assistants.**

[![Website](https://img.shields.io/badge/website-seometahawk.com-blue)](https://seometahawk.com/searchmetahawk-skills)
[![GitHub Stars](https://img.shields.io/github/stars/coresolstudio/searchhawk-skills?style=flat)](https://github.com/coresolstudio/searchhawk-skills)
[![Version](https://img.shields.io/badge/version-2.4.0-orange)](VERSIONS.md)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Last Commit](https://img.shields.io/github/last-commit/coresolstudio/searchhawk-skills)](https://github.com/coresolstudio/searchhawk-skills/commits/main)
[![Skills](https://img.shields.io/badge/skills-25-purple)]()
[![Cursor](https://img.shields.io/badge/Cursor-compatible-black)](https://cursor.com)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-compatible-purple)](https://claude.ai/download)

Companion skill pack for the [SEO MetaHawk](https://seometahawk.com/) ecosystem — plan, audit, improve, and track search visibility across **traditional search (SEO)**, **answer engines (AEO)**, and **AI search (GEO)**.

**Docs & install guide:** [seometahawk.com/searchmetahawk-skills](https://seometahawk.com/searchmetahawk-skills)

---

## What is SearchHawk Skills?

SearchHawk Skills is an original Agent Skills library for Cursor, Claude Code, and any Agent Skills–compatible host. Every skill is zero-dependency Markdown with optional stdlib Python connectors — no API keys required for Tier 1 workflows.

| Pillar | What it covers |
|--------|----------------|
| **SEO** | Rankings, on-page, technical crawl, internal links |
| **AEO** | Featured snippets, PAA, voice, direct-answer blocks |
| **GEO** | AI citations, entity signals, cite-worthy content |

Quality gates use **Hawk-Trust (60 items)** for content and **Hawk-Authority (35 items)** for domain trust — original frameworks built for multi-surface search in 2026.

---

## Quick start

| Tool | Install |
|------|---------|
| **Cursor** | `git clone` + `./install.sh` — or Settings → Rules → Remote Rule (GitHub) |
| **Claude Code** | `git clone` + `./install.sh --all` |
| **Claude.ai (web)** | Download a zip from [`dist/`](dist/) → Settings → Capabilities → Skills → Upload skill |
| **Codex / Copilot / Windsurf / Gemini CLI** | Clone the repo — agents read [AGENTS.md](AGENTS.md) automatically |
| **Abacus AI & other MCP hosts** | Load skills as instructions + optional [.mcp.json](.mcp.json) fetch server — see [docs/HOSTS.md](docs/HOSTS.md) |

```bash
git clone https://github.com/coresolstudio/searchhawk-skills.git
cd searchhawk-skills
chmod +x install.sh && ./install.sh
```

Restart Cursor (or your Agent Skills host), then try:

```text
/searchhawk:auto audit https://example.com
Research keywords for home espresso machines
What should I fix first on my site?
Run Hawk-Trust quality gate on [URL]
```

**Single-skill install:** symlink any folder under `discover/`, `diagnose/`, etc. into your host's skills directory.

**Full per-host guide** (Cursor, Claude, Codex, Windsurf, Copilot, Gemini CLI, Abacus AI, generic MCP hosts): [docs/HOSTS.md](docs/HOSTS.md)

---

## Operating model

Every skill follows the same contract: Quick Start → Skill Contract → Handoff Summary → Data Sources → Instructions → Reference Materials → Next Best Skill.

Four protocol skills form the quality layer:

| Protocol skill | Role |
|----------------|------|
| `content-quality-gate` | Hawk-Trust 60-item publish gate |
| `domain-trust-check` | Hawk-Authority 35-item trust gate |
| `entity-profile` | Canonical brand/person entity for GEO |
| `project-memory` | HOT/WARM/COLD session memory |

Shared references: [skill-contract.md](references/skill-contract.md) · [state-model.md](references/state-model.md) · [auditor-runbook.md](references/auditor-runbook.md)

---

## Skills (25)

| Phase | Skills |
|-------|--------|
| **Router** | `searchhawk-auto`, `publish-checklist` |
| **Discover** | `topic-keyword-finder`, `serp-reviewer`, `competitor-snapshot`, `content-gap-finder` |
| **Diagnose** | `site-search-audit`, `page-audit`, `technical-site-check` |
| **Decide** | `fix-priority-ranker` |
| **Improve** | `search-content-writer`, `answer-content-optimizer`, `ai-friendly-content-optimizer`, `meta-tags-helper`, `schema-helper`, `internal-links-helper`, `content-updater` |
| **Track** | `rank-monitor`, `ai-citation-checker`, `performance-snapshot`, `change-alerts` |
| **Protocol** | `content-quality-gate`, `domain-trust-check`, `entity-profile`, `project-memory` |

---

## Commands

Five slash commands, organized by intent:

| Command | Use for |
|---------|---------|
| `/searchhawk:auto` | Natural-language router — smallest useful skill chain |
| `/searchhawk:research` | Keywords, SERP, competitors, content gaps |
| `/searchhawk:audit` | Site/page/technical audit + quality & trust gates |
| `/searchhawk:create` | Write, optimize, meta tags, schema, refresh |
| `/searchhawk:track` | Rankings, AI citations, performance, alerts |

Daily work normally starts with `/searchhawk:auto`. Use the named commands when you already know the mode.

Command files: [commands/](commands/)

---

## Recommended workflow

```text
Discover → Diagnose → Decide → Improve → Track
              ↓
     content-quality-gate + domain-trust-check
              ↓
         project-memory
```

1. **Discover:** `topic-keyword-finder` → `serp-reviewer` → `content-gap-finder`
2. **Diagnose:** `site-search-audit` → `technical-site-check` → `fix-priority-ranker`
3. **Improve:** `search-content-writer` → `answer-content-optimizer` → `publish-checklist`
4. **Track:** `rank-monitor` → `ai-citation-checker` → `performance-snapshot`

For publish-ready content, always run `content-quality-gate` before shipping.

---

## Connectors (Tier 1 — no API keys)

Bundled stdlib Python scripts. See [CONNECTORS.md](CONNECTORS.md).

| Script | Purpose |
|--------|---------|
| `onpage.py` | Title, meta, H1/H2, canonical, JSON-LD |
| `suggest.py` | Google Autocomplete keyword ideas |
| `crawl.py` | Same-host BFS crawl |
| `linkgraph.py` | Orphans, depth, internal PageRank |
| `robots.py` | robots.txt + AI bot flags |
| `schema_lint.py` | JSON-LD validation |
| `sitemap.py` | Sitemap / llms.txt discovery |
| `psi.py` | PageSpeed Insights + Core Web Vitals |

```bash
python3 scripts/connectors/onpage.py https://example.com
python3 scripts/connectors/crawl.py https://example.com --max-pages 20 --quiet > crawl.json
python3 scripts/connectors/linkgraph.py crawl.json --top 10
python3 scripts/connectors/sitemap.py https://example.com --limit 100
python3 scripts/connectors/psi.py https://example.com   # optional PAGESPEED_API_KEY
```

---

## Frameworks

| Framework | Items | Skill |
|-----------|-------|-------|
| **Hawk-Trust (HTF)** | 60 | `content-quality-gate` |
| **Hawk-Authority (HAF)** | 35 | `domain-trust-check` |

Benchmarks: [hawk-trust-benchmark.md](references/hawk-trust-benchmark.md) · [hawk-authority-benchmark.md](references/hawk-authority-benchmark.md)

---

## Eval scenarios

Regression tests for routing and quality: [evals/searchhawk-scenarios.md](evals/searchhawk-scenarios.md) (**35 scenarios**)

---

## Project docs

| Doc | Purpose |
|-----|---------|
| [AGENTS.md](AGENTS.md) | Repo guidance for any agents.md-aware AI tool |
| [CLAUDE.md](CLAUDE.md) | Claude Code-specific notes |
| [docs/HOSTS.md](docs/HOSTS.md) | Per-host setup: Cursor, Claude, Codex, Windsurf, Copilot, Gemini CLI, Abacus AI, MCP hosts |
| [CONNECTORS.md](CONNECTORS.md) | Tier model, bundled scripts, MCP config |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to add or change a skill |
| [VERSIONS.md](VERSIONS.md) | Release history |
| [SECURITY.md](SECURITY.md) | Threat surface + vulnerability reporting |
| [PRIVACY.md](PRIVACY.md) | Zero-telemetry policy, connector network behavior |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community standards |

---

## Install

```bash
./install.sh          # Cursor (~/.cursor/skills)
./install.sh --all    # Cursor + Claude Code
```

### Claude.ai (web) upload

Claude.ai's **Upload skill** dialog requires one zip per skill with `SKILL.md` in a single top-level folder.

**No terminal needed:** download any prebuilt zip from [`dist/`](dist/) and upload it via **Claude → Settings → Capabilities → Skills → Upload skill**.

Or regenerate the zips yourself:

```bash
./package.sh                    # all 25 skills → dist/
./package.sh site-search-audit  # one skill
```

Connector scripts referenced by a skill (e.g. `onpage.py`) are bundled into its zip automatically, so each upload is self-contained.

---

## Disclaimer

These skills assist SEO, AEO, and GEO workflows but do not guarantee rankings, AI citations, traffic, legal compliance, or business outcomes. Verify recommendations with qualified professionals before relying on them for major strategy or legal decisions.

---

## License

MIT License — see [LICENSE](LICENSE). Same permissive license as [SEO MetaHawk](https://seometahawk.com/).

---

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=coresolstudio/searchhawk-skills&type=Date)](https://star-history.com/#coresolstudio/searchhawk-skills&Date)

---

<p align="center">
  Built by <a href="https://coresolstudio.com">Coresol Studio</a> ·
  <a href="https://seometahawk.com/">SEO MetaHawk</a> ·
  <a href="https://seometahawk.com/searchmetahawk-skills">SearchHawk Skills docs</a>
</p>
