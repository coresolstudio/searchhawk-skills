# SearchHawk State Model

Project memory uses three tiers:

| Tier | Path | TTL | Contents |
|------|------|-----|----------|
| **HOT** | `memory/hot-cache.md` | Session + 7 days | Active URL, keyword set, last verdict |
| **WARM** | `memory/{category}/` | Project lifetime | Dated skill outputs |
| **COLD** | `memory/archive/` | Permanent | Compressed monthly rollups |

## Write paths

| Category | Path |
|----------|------|
| Research | `memory/research/{skill}/` |
| Audits | `memory/audits/{skill}/` |
| Content | `memory/content/` |
| Monitoring | `memory/monitoring/` |
| Decisions | `memory/decisions.md` (user-approved only) |
| Open loops | `memory/open-loops.md` |

## Provenance

Decision entries require `approved_by: user | skill_inferred | migrated`.

Auditors ignore `skill_inferred` decisions for verdict purposes.
