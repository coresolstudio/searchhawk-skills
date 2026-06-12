# CLAUDE.md — SearchHawk Skills

Claude Code-specific guidance. General agent guidance lives in [AGENTS.md](AGENTS.md) —
read that first; this file only covers Claude-specific behavior.

## Using the skills

- **Installed skills** (`./install.sh --all` → `~/.claude/skills`): Claude Code discovers
  each skill automatically; describe a goal in plain language or invoke a
  `/searchhawk:*` command if commands are exposed.
- **Working inside this repo**: treat each `*/SKILL.md` as the authoritative instruction
  set for its task. Route via `cross-cutting/searchhawk-auto/SKILL.md` when the user
  doesn't name a skill.

## Claude.ai (web) uploads

Per-skill upload zips live in `dist/` (single top-level folder + `SKILL.md`, connectors
bundled). Regenerate with `./package.sh` after any skill change.

## MCP

[.mcp.json](.mcp.json) declares an optional `fetch` MCP server for hosts where the
Python connectors can't run. It is optional — Tier 1 (paste + bundled scripts) always
works without it. See [CONNECTORS.md](CONNECTORS.md) for the tier model.

## Editing rules

- Skills stay zero-dependency Markdown; connectors stay stdlib Python.
- After skill changes: update `marketplace.json`, README table, evals, and re-run
  `./package.sh`. Full checklist in [CONTRIBUTING.md](CONTRIBUTING.md).
- Never rename skills, commands, or the Hawk-Trust / Hawk-Authority frameworks.
