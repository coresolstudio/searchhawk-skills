# SearchHawk Product API

Natural-language routing for SearchHawk commands.

## Command mapping

| Command | Intent |
|---------|--------|
| `/searchhawk:auto` | Infer mode from goal |
| `/searchhawk:research` | Discover phase skills |
| `/searchhawk:audit` | Diagnose + protocol gates |
| `/searchhawk:create` | Improve phase skills |
| `/searchhawk:track` | Track phase + memory |

## Scenario families

| Family | Example | Chain |
|--------|---------|-------|
| site-audit | "audit my site" | site-search-audit → fix-priority-ranker |
| page-fix | "fix this URL" | page-audit → fix-priority-ranker → improve skill |
| keyword-start | "keywords for X" | topic-keyword-finder → serp-reviewer |
| write | "write post about X" | topic-keyword-finder → search-content-writer → publish-checklist |
| ai-check | "does AI cite me" | ai-citation-checker |
| publish | "ready to publish?" | content-quality-gate |

## Risk gates

- Publish-ready requires content-quality-gate SHIP
- YMYL requires domain-trust-check
- No guaranteed outcomes language

## Boundary

Non-search requests → decline politely.
