---
name: schema-helper
description: >
  Use when generating or validating JSON-LD: FAQ, HowTo, Article, Organization,
  BreadcrumbList, LocalBusiness. Runs schema_lint.py when validating live URLs.
  Not for invisible FAQ markup — schema must match visible page content.
version: "2.1.0"
when_to_use: "Schema markup, JSON-LD, structured data, FAQ schema, rich results prep."
argument-hint: "<url-or-content> [--type FAQ|Article|Organization|...]"
metadata:
  product: SearchHawk Skills
---

# Schema Helper

Produce accurate JSON-LD aligned with visible content.

## Supported types

Organization · Article/BlogPosting · FAQPage · HowTo · BreadcrumbList · LocalBusiness · WebPage

## Workflow

1. Read visible page content (WebFetch or user paste)
2. Draft JSON-LD matching on-page facts only
3. **Validate:** `python3 scripts/connectors/schema_lint.py <url>` or `--html file`
4. Fix missing required properties from lint report
5. Note FAQ/HowTo deprecation warnings — AEO value remains; rich results limited

## Rules

- Never invent ratings, prices, or FAQ answers not on the page
- FAQ schema Q&A must match visible text exactly

## Next Best Skill

`publish-checklist` → `content-quality-gate` for publish gate
