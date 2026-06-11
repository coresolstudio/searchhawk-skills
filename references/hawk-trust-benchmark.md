# Hawk-Trust Benchmark (HTF)

SearchHawk **60-item** content quality framework. Covers SEO, AEO, and GEO in one gate.

Score each item 0–2: **0** fail · **1** partial · **2** pass. Veto items force BLOCK regardless of total.

## Veto items (any 0 → BLOCK)

| ID | Item |
|----|------|
| V01 | Primary claim is false or unsupported on YMYL topics |
| V02 | No visible author or brand attribution on advice content |
| V03 | Schema claims contradict visible page content |
| V04 | Deceptive intent (bait, hidden affiliate, fake urgency) |

## T — Title & technical on-page (8)

T01 Title unique and descriptive · T02 Title length 50–60 chars · T03 Meta description present · T04 Meta 150–160 chars · T05 One H1 · T06 Logical H2/H3 · T07 Canonical correct · T08 Indexable (no accidental noindex)

## R — Reader value (8)

R01 Answers search intent in first screen · R02 Sufficient depth for topic · R03 Original insight or experience · R04 Examples or evidence · R05 Updated dates where relevant · R06 Readable structure · R07 No thin doorway patterns · R08 Internal links to related content

## U — Unique expertise (8)

U01 Named expert or practitioner · U02 Credentials or experience shown · U03 First-hand signals ("we tested", case data) · U04 Methodology explained · U05 Limitations acknowledged · U06 Sources cited for facts · U07 Contact or About path · U08 No generic AI slop patterns

## S — Snippet & answer readiness (AEO) (12)

S01 Question-phrased headings · S02 40–60 word direct answers · S03 Definition pattern ("X is…") · S04 List/step content where appropriate · S05 Table comparisons where appropriate · S06 FAQ section visible · S07 FAQ matches schema if used · S08 PAA-style subquestions · S09 Conversational phrasing · S10 Speakable-friendly short sentences · S11 No answer buried below fluff · S12 Featured-snippet format matches SERP type

## H — Hawk AI-cite readiness (GEO) (12)

H01 Entity named consistently · H02 Clear brand/person in opening · H03 Factual density (stats, names, dates) · H04 Quotable definition blocks · H05 Organization/Article schema accurate · H06 External authoritative citations · H07 Unique data or perspective · H08 Topic fully covered · H09 No contradictions with known facts · H10 Trust page linked · H11 SameAs/social entity links · H12 Clean extractable headings

## M — Media & markup (12)

M01 Image alt text · M02 OG tags · M03 Twitter cards · M04 Valid JSON-LD syntax · M05 Breadcrumbs where needed · M06 Mobile viewport · M07 HTTPS · M08 No broken internal links (sample) · M09 hreflang if multilingual · M10 Video transcript if video-led · M11 Accessible link text · M12 No keyword stuffing

## Scoring

- **Raw score**: sum of non-veto items (max 112) → normalize to 100
- **SHIP**: no veto 0s, normalized ≥ 75, no S/H section average below 1.0
- **FIX**: no veto 0s, score 55–74 or weak S/H section
- **BLOCK**: any veto 0

See [auditor-runbook.md](auditor-runbook.md) for cap rules and handoff fields.
