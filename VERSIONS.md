# Versions

Release state for SearchHawk Skills. The latest entry is what ships on `main`.

## 2.4.0 — Multi-host & MCP compatibility (2026-06-12)

- `AGENTS.md` + `CLAUDE.md` so any agents.md-reading host (Cursor, Codex, Copilot,
  Windsurf, Gemini CLI, Abacus AI, …) understands the repo natively
- `.mcp.json` — optional reference `fetch` MCP server for MCP-facilitating providers
- `docs/HOSTS.md` — per-host install guide (Cursor, Claude Code, Claude.ai web, Codex,
  Windsurf, Copilot, Gemini CLI, Abacus AI, generic MCP hosts)
- Governance docs: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `PRIVACY.md`,
  `VERSIONS.md`
- GitHub issue/PR templates

## 2.3.1 — Claude.ai upload packaging (2026-06-11)

- `package.sh` — generates one upload-ready zip per skill (single top-level folder,
  `SKILL.md` inside, referenced connectors bundled)
- Prebuilt zips shipped in `dist/` for no-terminal installs
- README: "Claude.ai (web) upload" section

## 2.3.0 — Initial public release (2026-06-11)

- 25 skills across Router / Discover / Diagnose / Decide / Improve / Track / Protocol
- 5 slash commands under the `/searchhawk:` namespace
- Hawk-Trust (60-item) content gate · Hawk-Authority (35-item) domain trust gate
- 8 stdlib Python connectors (onpage, suggest, crawl, linkgraph, robots, schema_lint,
  sitemap, psi)
- 25 worked example reports · 35 eval scenarios
- `install.sh` for Cursor (`--all` adds Claude Code) · `marketplace.json` manifest

## Versioning policy

- **Major** — breaking changes to skill names, command namespace, or frameworks
- **Minor** — new skills, new docs/integrations, connector additions
- **Patch** — fixes and content refinements

Individual skills carry their own `version` in `SKILL.md` frontmatter.
