# Sector Flows — זרימת כסף לסקטורים

Investigate whether capital is entering or leaving sectors and identify listed companies with verified exposure to the themes.

This is a standalone Agent Skill. Read [SKILL.md](SKILL.md) for the agent workflow and [sources.md](references/sources.md) for the source map and retrieval queries. The instructions work with an assistant's available public search/page tools; no paid data subscription is required.

## Inputs and defaults

Optional sectors, region, fund universe, windows and flow/share/NAV/AUM exports. Defaults: US sector ETF panel and comparable one-week, one-month and three-month periods.

User-supplied filters take precedence. Give a source file or ticker list when you want a defined universe. The assistant should state exactly which names, dates and data it managed to review. Output follows your language; the skill itself is written in English for reuse across hosts.

## What the skill does

Prefer reported subscriptions/redemptions or creations; calculate transparent estimates only with adequate inputs; distinguish flows from performance/breadth; normalize by beginning AUM and avoid overlap; research real business beneficiaries.

The search expands through relevant free source families, follows claims into primary documents and checks contrary evidence. It can use additional free sites beyond the catalog. Public access is checked at runtime; an inaccessible or paywalled page is not silently treated as verified data. It returns fewer results when evidence is insufficient.

## What you receive

Sector/fund flow comparison with evidence level, dates, flow/AUM, persistence, relative-price context and coverage; candidate stocks with exposure, valuation, catalyst and optional verified breakout.

Material inputs retain links, observation and publication dates, accounting/data basis, units and confidence. Facts, third-party claims and model assumptions remain distinguishable. An illustrative example is not presented as a current market finding.

## Example requests

```text
$sector-flows Compare recent energy and technology fund flows using free public data and state which funds are covered.
```

```text
$sector-flows האם נכנס כסף לאנרגיה לאחרונה? הפרד זרימה אמיתית מעליית מחירים והצג מניות קשורות.
```

```text
$sector-flows Use this ETF NAV/share history to estimate creations and explain the assumptions.
```

## Worked interpretation (synthetic)

A synthetic unlevered ETF goes from one million to 1.1 million shares at $50 NAV, with no split: estimated primary creations are $5 million. A separate fund whose AUM rises 10% while its assets return 10% has no demonstrated inflow from those figures alone. The result represents the examined funds, not the entire sector.

These figures and names are teaching examples, not verified live transactions, forecasts or recommendations. Real ticker mentions in prompts demonstrate the request format only.

## Sources and boundaries

ETF exchange turnover is not creation flow. Broad-equity flow data are not sector detail. Fund mergers/distributions/FX can distort AUM residuals. Thematic baskets overlap, and gold bullion differs from miners.

The [source reference](references/sources.md) lists primary disclosures, discovery sites, example searches and source-specific caveats. Use free pages/datasets that are actually accessible; do not assume a commercial site's paid export is part of the workflow. Search broadly, but disclose the actual coverage rather than claiming every source was searched.

## Use on its own or with other skills

The skill contains its own core workflow and local references. Follow optional named-skill handoffs in SKILL.md only when those skills are installed and their output is needed. If absent, use the documented local fallback. No sibling directory or paid connector is required to understand this skill.

Copy the complete folder into the skill location supported by your assistant, or ask the assistant to read this folder's SKILL.md and follow it. In compatible hosts, invoke `$sector-flows`; other hosts may use a skill picker or `@sector-flows`. Merely cloning this repository does not activate skills in every client.
