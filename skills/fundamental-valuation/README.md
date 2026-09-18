# Fundamental Valuation — צמיחה והערכת שווי

Discover stocks with double-digit revenue and common-net-income growth in each of the next three fiscal years and compare a defensible future valuation with today’s market capitalization and per-share price.

This is a standalone Agent Skill. Read [SKILL.md](SKILL.md) for the agent workflow and [sources.md](references/sources.md) for the source map and retrieval queries. The instructions work with an assistant's available public search/page tools; no paid data subscription is required.

## Inputs and defaults

Optional ticker/universe, market, minimum annual growth, fiscal horizon, sector restrictions and source files. Default annual threshold: at least 10%, with positive starting common net income; specify strictly above if desired.

User-supplied filters take precedence. Give a source file or ticker list when you want a defined universe. The assistant should state exactly which names, dates and data it managed to review. Output follows your language; the skill itself is written in English for reuse across hosts.

## What the skill does

Collect actual financial statements and multiple free forecast sources; label every forecast by period/basis/source; test all six annual growth conditions; justify peer/historical multiples; build bear/base/bull and dilution-aware scenarios.

The search expands through relevant free source families, follows claims into primary documents and checks contrary evidence. It can use additional free sites beyond the catalog. Public access is checked at runtime; an inaccessible or paywalled page is not silently treated as verified data. It returns fewer results when evidence is insufficient.

## What you receive

Supported growth matches, incomplete/model-dependent candidates and rejected/turnaround names; FY0–FY3 forecast provenance; current/forward ratios; fair-multiple rationale; equity-value ratio and per-share/annualized returns.

Material inputs retain links, observation and publication dates, accounting/data basis, units and confidence. Facts, third-party claims and model assumptions remain distinguishable. An illustrative example is not presented as a current market finding.

## Example requests

```text
$fundamental-valuation Find stocks with at least 10% revenue and common-net-income growth in EACH of the next three fiscal years.
```

```text
$fundamental-valuation מצא מניות לפי תחזיות לשלוש שנים, קבע טווח מכפיל הוגן וחשב שווי עתידי מול שווי שוק.
```

```text
$fundamental-valuation Value this loss-making company using scenarios, keeping it separate from profitable growth-screen matches.
```

## Worked interpretation (synthetic)

Current price $10 × 100 million shares = $1 billion market cap. Future common income $150 million × fair P/E 12 = $1.8 billion future equity value: a 1.8× ratio and 80% aggregate increase. With 120 million future shares, target price is $15 and per-share upside is 50%. These are future scenario values, not discounted fair value today.

These figures and names are teaching examples, not verified live transactions, forecasts or recommendations. Real ticker mentions in prompts demonstrate the request format only.

## Sources and boundaries

Three-year CAGR does not guarantee 10% growth in every year. SEC actuals and 13F are not consensus forecasts. Missing free FY3 estimates remain missing; model scenarios are useful but kept separate. Multiples differ by sector and accounting basis.

The [source reference](references/sources.md) lists primary disclosures, discovery sites, example searches and source-specific caveats. Use free pages/datasets that are actually accessible; do not assume a commercial site's paid export is part of the workflow. Search broadly, but disclose the actual coverage rather than claiming every source was searched.

## Use on its own or with other skills

The skill contains its own core workflow and local references. Follow optional named-skill handoffs in SKILL.md only when those skills are installed and their output is needed. If absent, use the documented local fallback. No sibling directory or paid connector is required to understand this skill.

Copy the complete folder into the skill location supported by your assistant, or ask the assistant to read this folder's SKILL.md and follow it. In compatible hosts, invoke `$fundamental-valuation`; other hosts may use a skill picker or `@fundamental-valuation`. Merely cloning this repository does not activate skills in every client.

## Offline calculator

Run from this skill folder with Python 3.10 or later; only the standard library is needed:

```bash
python3 scripts/valuation.py examples/valuation.json
```

The input is synthetic and the script only computes supplied data. It does not fetch or authenticate sources, choose investment assumptions, or place orders. Fractions such as `0.10` mean 10%. Monetary amounts and shares must use consistent scales; preserve the source and period metadata in real research.

See [calculator inputs and limits](references/calculator.md) for the schema and supported operations.
