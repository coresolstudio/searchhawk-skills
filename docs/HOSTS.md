# Host Setup Guide

SearchHawk Skills works on three integration paths. Pick the row that matches your tool.

| Path | How it works | Who uses it |
|------|--------------|-------------|
| **A. Agent Skills** | Host auto-discovers `SKILL.md` folders | Cursor, Claude Code, Claude.ai, skills.sh hosts |
| **B. AGENTS.md context** | Agent reads [AGENTS.md](../AGENTS.md) and routes via `searchhawk-auto` | Codex, Copilot, Windsurf, Gemini CLI, Jules, and other agents.md-aware tools |
| **C. MCP + instructions** | Skills loaded as instructions/knowledge; optional [.mcp.json](../.mcp.json) fetch server for live URLs | Abacus AI, Claude Desktop, LibreChat, Open WebUI, any MCP-facilitating provider |

Tier 1 always works on every path: paste a URL or GSC/GA4 export and run the skill as
written. The bundled Python connectors and MCP servers are optional accelerators.

---

## Cursor

```bash
git clone https://github.com/coresolstudio/searchhawk-skills.git
cd searchhawk-skills && chmod +x install.sh && ./install.sh
```

Symlinks all 25 skills into `~/.cursor/skills`. Restart Cursor, then try
`Audit https://example.com for SEO, AEO, and GEO`.

No-terminal alternative: **Settings → Rules → Add Rule → Remote Rule (GitHub)** and paste
the repo URL.

## Claude Code

```bash
./install.sh --all   # installs to ~/.claude/skills (and ~/.cursor/skills)
```

The repo also ships [CLAUDE.md](../CLAUDE.md) (auto-read when working inside the repo)
and [.mcp.json](../.mcp.json) (optional `fetch` server, opt-in on first use).

## Claude.ai (web)

Download any prebuilt zip from [`dist/`](../dist/) →
**Settings → Capabilities → Skills → Upload skill**. One zip per skill; connectors are
bundled inside. Regenerate zips with `./package.sh`.

## Codex CLI / GitHub Copilot / Windsurf / Gemini CLI

These agents read **[AGENTS.md](../AGENTS.md)** automatically when you open the cloned
repo. Two options:

1. **Work inside the repo** — clone it, open it, and ask for any SEO/AEO/GEO task; the
   agent routes via `cross-cutting/searchhawk-auto/SKILL.md`.
2. **Bring skills to your project** — copy the skill folders you need into your
   project (e.g. `.github/instructions/`, Windsurf rules, or your agent's context dir)
   and reference them from your project's `AGENTS.md`.

## Abacus AI (ChatLLM / CodeLLM / DeepAgent)

Abacus AI products support MCP and custom instructions — use path C:

1. **As knowledge/instructions:** upload the relevant `SKILL.md` files (or the per-skill
   zips from `dist/`) as custom instructions or knowledge documents for your assistant.
   Start with `searchhawk-auto` so the assistant can route between skills.
2. **MCP (optional):** register the reference fetch server from [.mcp.json](../.mcp.json)
   (`uvx mcp-server-fetch`) in the MCP settings so the assistant can pull live page data
   instead of asking you to paste HTML.
3. **CodeLLM / DeepAgent:** clone the repo into the workspace — both read `AGENTS.md`
   for repository guidance.

## Any other MCP-facilitating provider

If your tool can (a) accept Markdown instructions and (b) optionally connect MCP servers,
SearchHawk Skills works:

1. Load `cross-cutting/searchhawk-auto/SKILL.md` plus the skills you need as
   instructions/knowledge.
2. Optionally add the `fetch` MCP server from [.mcp.json](../.mcp.json) — or any
   SEO MCP server (Ahrefs, Semrush, GSC) for Tier 3 automation; placeholder mapping is
   documented in [CONNECTORS.md](../CONNECTORS.md).
3. Where the host can execute Python, the stdlib connectors in `scripts/connectors/`
   replace most paste steps.

---

## Verification checklist (any host)

1. Ask: `Research keywords for home espresso machines` → the host should engage
   `topic-keyword-finder` (or route there via `searchhawk-auto`).
2. Ask: `Run the publish checklist on [URL]` → expect the 12-point gate with a verdict.
3. If skills don't trigger, confirm the host can see the skill files and that the
   `SKILL.md` frontmatter (`name`, `description`) is intact.
