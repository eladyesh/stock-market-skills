# Insider Buying — רכישות בעלי עניין

Find officers, directors and significant holders committing their own money, verify each purchase, and distinguish a meaningful cluster from compensation or duplicate reports.

This is a standalone Agent Skill. Read [SKILL.md](SKILL.md) for the agent workflow and [sources.md](references/sources.md) for the source map and retrieval queries. The instructions work with an assistant's available public search/page tools; no paid data subscription is required.

## Inputs and defaults

Optional ticker/universe, market, transaction and filing windows, minimum cash purchase, officer/director filters and cluster window. Defaults: 90 days of transactions and a 30-day cluster window.

User-supplied filters take precedence. Give a source file or ticker list when you want a defined universe. The assistant should state exactly which names, dates and data it managed to review. Output follows your language; the skill itself is written in English for reuse across hosts.

## What the skill does

Locate leads across filings and free screeners; inspect Form 4 tables and footnotes; resolve amendments and related entities; calculate cash committed and stake changes; examine repeat buyers and contrary business news.

The search expands through relevant free source families, follows claims into primary documents and checks contrary evidence. It can use additional free sites beyond the catalog. Public access is checked at runtime; an inaccessible or paywalled page is not silently treated as verified data. It returns fewer results when evidence is insufficient.

## What you receive

Issuer shortlist plus buyer-level transaction records, cash values, purchase venue, independent buyer count, original links, timing and excluded false positives.

Material inputs retain links, observation and publication dates, accounting/data basis, units and confidence. Facts, third-party claims and model assumptions remain distinguishable. An illustrative example is not presented as a current market finding.

## Example requests

```text
$insider-buying Find meaningful CEO/CFO purchases in the last 90 days and show independent buying clusters.
```

```text
$insider-buying בדוק רכישות בעלי עניין ב-DELL והפרד רכישות מהקצאות ומימוש אופציות.
```

```text
$insider-buying Scan Israeli issuer disclosures for director purchases; use the actual local reports.
```

## Worked interpretation (synthetic)

A director buys 1,000 shares at $12 in a private placement: $12,000 of cash committed. A second report by the same controlled entity counts once. A grant of 5,000 shares for $0 is excluded. Code P alone does not establish an open-market purchase.

These figures and names are teaching examples, not verified live transactions, forecasts or recommendations. Real ticker mentions in prompts demonstrate the request format only.

## Sources and boundaries

13F describes institutional holdings, not management transactions. An old purchase disclosed today is not a purchase today. Foreign/local reporting regimes and free screener coverage vary.

The [source reference](references/sources.md) lists primary disclosures, discovery sites, example searches and source-specific caveats. Use free pages/datasets that are actually accessible; do not assume a commercial site's paid export is part of the workflow. Search broadly, but disclose the actual coverage rather than claiming every source was searched.

## Use on its own or with other skills

The skill contains its own core workflow and local references. Follow optional named-skill handoffs in SKILL.md only when those skills are installed and their output is needed. If absent, use the documented local fallback. No sibling directory or paid connector is required to understand this skill.

Copy the complete folder into the skill location supported by your assistant, or ask the assistant to read this folder's SKILL.md and follow it. In compatible hosts, invoke `$insider-buying`; other hosts may use a skill picker or `@insider-buying`. Merely cloning this repository does not activate skills in every client.

## Offline calculator

Run from this skill folder with Python 3.10 or later; only the standard library is needed:

```bash
python3 scripts/insiders.py insiders examples/insiders.json
```

The input is synthetic and the script only computes supplied data. It does not fetch or authenticate sources, choose investment assumptions, or place orders. Fractions such as `0.10` mean 10%. Monetary amounts and shares must use consistent scales; preserve the source and period metadata in real research.
