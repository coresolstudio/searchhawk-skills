# Example: Entity Profile

**Brand:** Homebrew Beans · **Domain:** homebrewbeans.com · **Date:** 2026-06-11

## Canonical Entity

| Field | Value |
|-------|-------|
| **Name** | Homebrew Beans |
| **Type** | Organization (e-commerce + editorial) |
| **Description** | Independent coffee gear reviews and espresso guides for home baristas. |
| **Founded** | 2019 (visible on About page) |
| **HQ** | Austin, TX (NAP on contact page) |

## Name Variants

- Homebrew Beans ✓ (primary)
- Home Brew Beans ✗ (inconsistent in one guest post)
- HBB — avoid in schema; use full name

## sameAs Profiles

| Platform | URL | Status |
|----------|-----|--------|
| YouTube | youtube.com/@homebrewbeans | ✓ linked from site |
| Instagram | instagram.com/homebrewbeans | ✓ |
| Wikidata | — | ✗ not claimed |
| LinkedIn | — | ✗ missing |

## Schema Template (Organization)

```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Homebrew Beans",
  "url": "https://homebrewbeans.com",
  "logo": "https://homebrewbeans.com/logo.png",
  "sameAs": [
    "https://www.youtube.com/@homebrewbeans",
    "https://www.instagram.com/homebrewbeans"
  ]
}
```

## Gap List

| Gap | Priority | Fix |
|-----|----------|-----|
| No Wikidata / KG entity | HIGH | Create item + cite official site |
| Author entities thin | MED | Person schema on 3 lead authors |
| Inconsistent brand spelling off-site | MED | Outreach + `entity-profile` refresh |

## Handoff Summary

- **Status:** DONE
- **Recommended next skill:** `schema-helper` → `ai-friendly-content-optimizer`
