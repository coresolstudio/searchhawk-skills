# Contributing to SearchHawk Skills

Thanks for helping make SearchHawk Skills better. This guide covers everything from a
typo fix to a brand-new skill.

## Ground rules

- Skill content is **zero-dependency Markdown**. No build steps, no npm, no pip packages.
- Connector scripts are **Python stdlib only** and must degrade gracefully (clear error
  messages, no hard crashes on network failures).
- Tier 1 must always work: every skill has to function with nothing but a URL and
  pasted data.
- Brand names are fixed: SearchHawk Skills, Hawk-Trust, Hawk-Authority, the
  `/searchhawk:` command namespace, and individual skill names.

## Adding or changing a skill

1. **One folder per skill** under the right phase directory
   (`discover/`, `diagnose/`, `decide/`, `improve/`, `track/`, `protocol/`,
   `cross-cutting/`).
2. **`SKILL.md`** with YAML frontmatter:

   ```yaml
   ---
   name: my-skill-name
   description: >
     One- or two-line description of what the skill does and when to use it.
   version: "1.0.0"
   license: MIT
   compatibility: "Cursor, Claude Code, Agent Skills hosts"
   when_to_use: "Trigger conditions in one sentence."
   ---
   ```

3. **Follow the skill contract** (`references/skill-contract.md`): Quick Start →
   Skill Contract → Handoff Summary → Data Sources → Instructions → Reference
   Materials → Next Best Skill.
4. **Worked example**: include `references/example-report.md` showing realistic output.
5. **Register it**: add the path to `marketplace.json` and the skill table in
   `README.md`.
6. **Evals**: add at least one routing scenario to `evals/searchhawk-scenarios.md`.
7. **Repackage**: run `./package.sh` so `dist/` stays in sync.

## Pull request checklist

- [ ] `SKILL.md` frontmatter has `name` and `description` (required by upload hosts)
- [ ] Skill follows the shared contract sections
- [ ] `references/example-report.md` included or updated
- [ ] `marketplace.json` + README table updated
- [ ] Eval scenario added/updated
- [ ] `./package.sh` run; `dist/` zips refreshed
- [ ] `VERSIONS.md` entry added under "Unreleased"

## Commit style

Short imperative subject lines, e.g. `Add serp-volatility skill to track phase.`

## Questions

Open a [GitHub issue](https://github.com/coresolstudio/searchhawk-skills/issues) or see
the docs at [seometahawk.com/searchhawk-skills](https://seometahawk.com/searchhawk-skills/).
