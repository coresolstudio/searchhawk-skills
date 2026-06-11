---
name: search-content-writer
description: >
  Use when writing SEO-structured content: blog posts, guides, landing pages with
  headings, intent match, FAQ sections, and internal link suggestions. Not for
  snippet-only rewrites — use answer-content-optimizer.
version: "2.0.0"
license: MIT
when_to_use: "Write SEO content, blog post, article draft, landing page copy."
argument-hint: "<topic-or-brief> [--type article|landing|guide]"
metadata:
  product: SearchHawk Skills
---

# Search Content Writer

Produce rank-ready drafts with AEO/GEO hooks built in.

## Skill Contract

- **Done when**: full markdown draft + meta block + 3+ internal link suggestions + FAQ section
- **Primary next skill**: `answer-content-optimizer`

## Instructions — 8 phases

1. **Scope** — keyword, intent, audience, word count
2. **Outline** — H1/H2/H3 aligned to SERP (use `serp-reviewer` if needed)
3. **Intro** — answer intent in 100 words
4. **Body** — scannable sections, examples, no filler
5. **FAQ** — 3–5 PAA-style questions
6. **Links** — internal anchor suggestions
7. **Meta** — title + description draft
8. **Risks** — flag YMYL, missing evidence, thin sections

See [writing-checklist.md](references/writing-checklist.md).

## Next Best Skill

`answer-content-optimizer` → `content-quality-gate`
