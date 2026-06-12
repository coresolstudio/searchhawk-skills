# Security Policy

## Supported versions

Only the latest release on `main` is supported. See [VERSIONS.md](VERSIONS.md).

## What this project does (threat surface)

- **Skill files** are static Markdown — they execute nothing by themselves.
- **Connector scripts** (`scripts/connectors/*.py`) are stdlib Python that fetch
  user-provided URLs over HTTPS. They send no telemetry and write only to the local
  working directory (e.g. `crawl.json`).
- **Optional MCP config** ([.mcp.json](.mcp.json)) declares a reference `fetch` server;
  installing or running it is always opt-in by the host.
- **No secrets are bundled.** Optional API keys (`PAGESPEED_API_KEY`) are read from the
  local environment only and never logged.

## Reporting a vulnerability

Please report security issues privately via
[GitHub Security Advisories](https://github.com/coresolstudio/searchhawk-skills/security/advisories/new)
("Report a vulnerability"). Do not open public issues for exploitable problems.

Include: affected file/script, reproduction steps, and impact. We aim to acknowledge
reports within 7 days.

## Guidance for users

- Review any skill's `SKILL.md` before installing — it is plain Markdown, fully auditable.
- Run connectors only against sites you are authorized to crawl; respect `robots.txt`
  (`robots.py` helps you check it).
- Treat MCP servers like any third-party dependency: install only what you trust.
