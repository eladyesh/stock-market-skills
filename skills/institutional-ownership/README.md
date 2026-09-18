# Institutional Ownership — קרנות, בנקים ורוכשים גדולים

Trace large disclosed holdings changes and notable buyers across funds, banks, public officials and sovereign reserves, while keeping analyst views separate from purchases.

This is a standalone Agent Skill. Read [SKILL.md](SKILL.md) for the agent workflow and [sources.md](references/sources.md) for the source map and retrieval queries. The instructions work with an assistant's available public search/page tools; no paid data subscription is required.

## Inputs and defaults

Optional manager (including Situational Awareness), ticker, manager panel, official, bank, country/asset, date range and channel. Defaults: two latest public fund quarters plus 90 days of news.

User-supplied filters take precedence. Give a source file or ticker list when you want a defined universe. The assistant should state exactly which names, dates and data it managed to review. Output follows your language; the skill itself is written in English for reuse across hosts.

## What the skill does

Verify legal filer identity; retrieve original and amended tables; compare split-adjusted quantities by class/instrument; investigate significant changes; use separate official/analyst/sovereign disclosure routes.

The search expands through relevant free source families, follows claims into primary documents and checks contrary evidence. It can use additional free sites beyond the catalog. Public access is checked at runtime; an inaccessible or paywalled page is not silently treated as verified data. It returns fewer results when evidence is insufficient.

## What you receive

Separate channel tables showing holding/transaction date, filing date, quantities or reported amount ranges, disclosed weights, change type, limitations and source links.

Material inputs retain links, observation and publication dates, accounting/data basis, units and confidence. Facts, third-party claims and model assumptions remain distinguishable. An illustrative example is not presented as a current market finding.

## Example requests

```text
$institutional-ownership What are Situational Awareness’s latest publicly disclosed holdings, and what changed from the prior quarter?
```

```text
$institutional-ownership מה קנו לאחרונה קרנות גידור ואנשי ממשל? הפרד דיווחי החזקות, עסקאות והמלצות של Goldman Sachs.
```

```text
$institutional-ownership Has China added to official gold reserves recently? Compare quantities, not only dollar values.
```

## Worked interpretation (synthetic)

A 13F holding rises from 100 to 200 shares while a 2-for-1 split occurs: adjusted quantity is unchanged. A new call row stays separate. A Goldman Sachs Buy reiteration is an analyst opinion. Higher dollar gold reserves with unchanged ounces show no verified increase in reported gold quantity.

These figures and names are teaching examples, not verified live transactions, forecasts or recommendations. Real ticker mentions in prompts demonstrate the request format only.

## Sources and boundaries

13F is delayed, partial and generally omits short stock positions. Public-official disclosures often report ranges. Bank holdings can represent client or market-making activity. No channel implies complete live positions.

The [source reference](references/sources.md) lists primary disclosures, discovery sites, example searches and source-specific caveats. Use free pages/datasets that are actually accessible; do not assume a commercial site's paid export is part of the workflow. Search broadly, but disclose the actual coverage rather than claiming every source was searched.

## Use on its own or with other skills

The skill contains its own core workflow and local references. Follow optional named-skill handoffs in SKILL.md only when those skills are installed and their output is needed. If absent, use the documented local fallback. No sibling directory or paid connector is required to understand this skill.

Copy the complete folder into the skill location supported by your assistant, or ask the assistant to read this folder's SKILL.md and follow it. In compatible hosts, invoke `$institutional-ownership`; other hosts may use a skill picker or `@institutional-ownership`. Merely cloning this repository does not activate skills in every client.

## Offline calculator

Run from this skill folder with Python 3.10 or later; only the standard library is needed:

```bash
python3 scripts/holdings.py holdings examples/holdings.json
```

The input is synthetic and the script only computes supplied data. It does not fetch or authenticate sources, choose investment assumptions, or place orders. Fractions such as `0.10` mean 10%. Monetary amounts and shares must use consistent scales; preserve the source and period metadata in real research.
