# Short Candidates — מועמדות למחקר שורט

Find overvaluation paired with deteriorating evidence and a plausible catalyst, and assess the opposing thesis and costs of being wrong.

This is a standalone Agent Skill. Read [SKILL.md](SKILL.md) for the agent workflow and [sources.md](references/sources.md) for the source map and retrieval queries. The instructions work with an assistant's available public search/page tools; no paid data subscription is required.

## Inputs and defaults

Optional ticker/universe, sector, catalyst window, valuation assumptions and dated borrow/short-interest data. Default catalyst horizon: 3–12 months.

User-supplied filters take precedence. Give a source file or ticker list when you want a defined universe. The assistant should state exactly which names, dates and data it managed to review. Output follows your language; the skill itself is written in English for reuse across hosts.

## What the skill does

Investigate financial quality and implied expectations; construct downside and adverse-upside cases; verify catalysts and negative news; interpret put evidence cautiously; inspect crowding, borrow availability, recalls, costs and squeeze risk.

The search expands through relevant free source families, follows claims into primary documents and checks contrary evidence. It can use additional free sites beyond the catalog. Public access is checked at runtime; an inaccessible or paywalled page is not silently treated as verified data. It returns fewer results when evidence is insufficient.

## What you receive

Research-ready bearish cases, valuation-only watchlist and rejected names; fair value, catalyst/timing, adverse upside, dated short interest, borrow gaps, long-side argument and falsification conditions.

Material inputs retain links, observation and publication dates, accounting/data basis, units and confidence. Facts, third-party claims and model assumptions remain distinguishable. An illustrative example is not presented as a current market finding.

## Example requests

```text
$short-candidates Find overvalued stocks with a concrete negative catalyst and show the strongest long argument for each.
```

```text
$short-candidates מצא מועמדות לשורט, קשר להערכת שווי, חדשות שליליות ופוטים, ובדוק סיכון לסקוויז.
```

```text
$short-candidates Investigate this short-seller report against company filings and the issuer’s response; distinguish allegations from findings.
```

## Worked interpretation (synthetic)

Entry $100 and a $70 cover imply 30% gross decline. Assuming one year of 20% borrow cost on initial notional and $2 dividends owed leaves roughly 8% before other costs under that simplified assumption. Borrow availability is still unknown. A rise to $200 instead loses 100% of initial notional before costs.

These figures and names are teaching examples, not verified live transactions, forecasts or recommendations. Real ticker mentions in prompts demonstrate the request format only.

## Sources and boundaries

High valuation alone is not a catalyst. Short volume is not short interest. Free pages rarely prove executable borrow terms. Short stock has theoretically unbounded loss; puts have separate expiry, premium and volatility economics.

The [source reference](references/sources.md) lists primary disclosures, discovery sites, example searches and source-specific caveats. Use free pages/datasets that are actually accessible; do not assume a commercial site's paid export is part of the workflow. Search broadly, but disclose the actual coverage rather than claiming every source was searched.

## Use on its own or with other skills

The skill contains its own core workflow and local references. Follow optional named-skill handoffs in SKILL.md only when those skills are installed and their output is needed. If absent, use the documented local fallback. No sibling directory or paid connector is required to understand this skill.

Copy the complete folder into the skill location supported by your assistant, or ask the assistant to read this folder's SKILL.md and follow it. In compatible hosts, invoke `$short-candidates`; other hosts may use a skill picker or `@short-candidates`. Merely cloning this repository does not activate skills in every client.
