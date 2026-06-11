# Hawk-Authority Benchmark (HAF)

SearchHawk **35-item** domain and entity trust framework.

Score 0–2 per item. Veto items → UNTRUSTED.

## Veto items

| ID | Item |
|----|------|
| A-V01 | Known malware, phishing, or severe security warnings |
| A-V02 | Site impersonates another brand |
| A-V03 | Legal/compliance red flags on regulated topics without credentials |

## Authority signals (35)

**Identity (7):** About page · Contact visible · Physical address if local · Privacy policy · Terms · Consistent NAP · Logo/brand clarity

**Entity graph (7):** Organization schema · Wikidata/Wikipedia mention (if applicable) · Social profiles linked · sameAs consistency · Founders named · Industry affiliations · Google Business Profile (local)

**Reputation (7):** Reviews/testimonials authentic · Press or citations · Backlink quality sample · No toxic spam patterns (user data) · Domain age signal · HTTPS history · No mass duplicate content across domain

**Content trust (7):** Editorial standards · Correction policy · Author archive · Topic consistency · No scaled low-value pages · E-E-A-T on money pages · Clear ownership

**Technical trust (7):** robots.txt sane · sitemap present · No cloaking signals · Security headers · No spammy redirects · Core pages indexable · llms.txt or AI crawler policy considered

## Verdicts

- **TRUSTED**: no veto; normalized ≥ 70
- **CAUTIOUS**: no veto; 50–69 or missing key identity
- **UNTRUSTED**: any veto or score < 50
