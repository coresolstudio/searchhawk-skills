---
name: domain-trust-check
description: >
  Use for domain and entity trust: authority signals, identity, reputation, technical trust. Runs 35-item Hawk-Authority benchmark. Not for single-page content — use content-quality-gate.
version: "2.0.0"
license: MIT
compatibility: "Cursor, Claude Code, Agent Skills hosts"
homepage: "https://github.com/searchhawk/skills"
when_to_use: "Domain authority audit, trust check, site credibility."
argument-hint: "<domain>"
allowed-tools: WebFetch
class: auditor
metadata:
  product: SearchHawk Skills
  tagline: "SEO · AEO · GEO for AI assistants"
---

# Domain Trust Check

Hawk-Authority (HAF) 35-item gate.

## When This Must Trigger

- New site assessment, YMYL, reputation concerns, GEO entity setup

## Instructions

1. Crawl identity pages: About, Contact, Privacy, key templates
2. Score [hawk-authority-benchmark.md](../../references/hawk-authority-benchmark.md)
3. Verdict: TRUSTED / CAUTIOUS / UNTRUSTED
4. Entity recommendations → `entity-profile`

## Next Best Skill

`entity-profile` for fixes.
