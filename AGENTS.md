# AGENTS.md — SearchHawk Skills

Guidance for AI coding agents (Cursor, Codex, Copilot, Windsurf, Gemini CLI, Abacus AI, and any
agent that reads `AGENTS.md`) working in or with this repository.

## What this repository is

SearchHawk Skills is an Agent Skills library: **25 skills + 5 slash commands** for SEO
(traditional search), AEO (answer engines), and GEO (AI search). Every skill is plain Markdown
with YAML frontmatter — no build step, no runtime dependencies. Optional stdlib Python
connectors live in `scripts/connectors/`.

- Homepage: https://seometahawk.com/searchhawk-skills/
- Publisher: Coresol Studio · MIT license
- Version state: see [VERSIONS.md](VERSIONS.md)

## Repository map

| Path | Contents |
|------|----------|
| `cross-cutting/` | `searchhawk-auto` (router), `publish-checklist` |
| `discover/` | Keyword, SERP, competitor, and gap research skills |
| `diagnose/` | Site, page, and technical audit skills |
| `decide/` | `fix-priority-ranker` |
| `improve/` | Content writing and optimization skills |
| `track/` | Rankings, AI citations, performance, alerts |
| `protocol/` | Quality gates: Hawk-Trust (60), Hawk-Authority (35), entity, memory |
| `commands/` | `/searchhawk:*` slash command definitions |
| `references/` | Shared contracts: skill-contract, state-model, auditor-runbook, benchmarks |
| `scripts/connectors/` | Stdlib Python: onpage, suggest, crawl, linkgraph, robots, schema_lint, sitemap, psi |
| `evals/` | 35 routing/quality regression scenarios |
| `dist/` | Prebuilt per-skill zips for web uploads (regenerate with `./package.sh`) |
| `docs/` | Host setup guides (see [docs/HOSTS.md](docs/HOSTS.md)) |

## How to route work

1. **Any search-visibility goal without a named skill** → start with
   `cross-cutting/searchhawk-auto/SKILL.md` and follow its chain selection.
2. **Named intent** → go straight to that skill's `SKILL.md`. Skills declare
   `when_to_use` in frontmatter.
3. Every skill follows the same contract (see `references/skill-contract.md`):
   Quick Start → Skill Contract → Handoff Summary → Data Sources → Instructions →
   Reference Materials → Next Best Skill. Honor handoff summaries between skills.
4. Before declaring content publish-ready, run `protocol/content-quality-gate`
   (Hawk-Trust 60) — verdicts are SHIP / FIX / BLOCK.

## Data tiers

| Tier | Needs | Notes |
|------|-------|-------|
| 1 | Nothing — URL + pasted data + bundled scripts | Default; always works |
| 2 | GSC / GA4 exports, optional `PAGESPEED_API_KEY` | User-supplied data |
| 3 | MCP tools (see [.mcp.json](.mcp.json) and [CONNECTORS.md](CONNECTORS.md)) | Optional automation |

Run connectors from the repository root, e.g.
`python3 scripts/connectors/onpage.py https://example.com`.

## Conventions for edits

- Each skill is one folder: `SKILL.md` (frontmatter: `name`, `description`, `version`,
  `license`, `when_to_use`) plus `references/` including a worked `example-report.md`.
- Skill content must stay zero-dependency Markdown. Python connectors must remain
  stdlib-only (no pip installs).
- New or changed skills: update `marketplace.json`, the README skill table,
  `evals/searchhawk-scenarios.md`, and regenerate `dist/` via `./package.sh`.
- Keep brand names exact: SearchHawk Skills, SEO MetaHawk, Hawk-Trust, Hawk-Authority,
  `/searchhawk:` command namespace. Do not rename skills or frameworks.
- See [CONTRIBUTING.md](CONTRIBUTING.md) for the full checklist.
