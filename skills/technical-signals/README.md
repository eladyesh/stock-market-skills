# Technical Signals — איתותים טכניים

Find reproducible moving-average crosses, 52-week extremes, 10% daily moves and unusual volume from dated price and volume observations.

This is a standalone Agent Skill. Read [SKILL.md](SKILL.md) for the agent workflow and [sources.md](references/sources.md) for the source map and retrieval queries. The instructions work with an assistant's available public search/page tools; no paid data subscription is required.

## Inputs and defaults

Optional universe, exchange, session, liquidity filters, moving-average windows and OHLCV export. Defaults: completed regular-session daily bars, SMA50/200, a 252-prior-session high/low proxy and 20-prior-session relative volume.

User-supplied filters take precedence. Give a source file or ticker list when you want a defined universe. The assistant should state exactly which names, dates and data it managed to review. Output follows your language; the skill itself is written in English for reuse across hosts.

## What the skill does

Get consistently split-adjusted OHLCV; validate dates/ranges and corporate actions; recompute triggers including the prior session; exclude today from baselines; label short histories and provisional intraday observations.

The search expands through relevant free source families, follows claims into primary documents and checks contrary evidence. It can use additional free sites beyond the catalog. Public access is checked at runtime; an inaccessible or paywalled page is not silently treated as verified data. It returns fewer results when evidence is insufficient.

## What you receive

Ticker/session table with exact trigger values, prior/current SMA, volume ratio, history coverage, liquidity, invalidation level and sources. Technical interpretation stays separate from fundamentals and news.

Material inputs retain links, observation and publication dates, accounting/data basis, units and confidence. Facts, third-party claims and model assumptions remain distinguishable. An illustrative example is not presented as a current market finding.

## Example requests

```text
$technical-signals Has DELL crossed its 200-day moving average in the latest completed session? Show both session values.
```

```text
$technical-signals מצא מניות עם תנועה של לפחות 10% ביום, מחזור חריג ושיא או שפל 52 שבועות.
```

```text
$technical-signals Analyze this OHLCV file and flag missing history instead of estimating unavailable indicators.
```

## Worked interpretation (synthetic)

Yesterday’s close $99 was below yesterday’s SMA200 $100; today’s close $102 is above today’s SMA200 $100.1: a new upward cross. Being above the average on both days is not a new cross. A current 2,000-share volume against the prior 20-day average of 1,000 is 2×.

These figures and names are teaching examples, not verified live transactions, forecasts or recommendations. Real ticker mentions in prompts demonstrate the request format only.

## Sources and boundaries

A split can mimic a price crash in unadjusted data. Total-return adjusted closes cannot be mixed with raw highs/lows. Intraday volume cannot be compared directly with completed-day volume. Signals do not establish an investment edge.

The [source reference](references/sources.md) lists primary disclosures, discovery sites, example searches and source-specific caveats. Use free pages/datasets that are actually accessible; do not assume a commercial site's paid export is part of the workflow. Search broadly, but disclose the actual coverage rather than claiming every source was searched.

## Use on its own or with other skills

The skill contains its own core workflow and local references. Follow optional named-skill handoffs in SKILL.md only when those skills are installed and their output is needed. If absent, use the documented local fallback. No sibling directory or paid connector is required to understand this skill.

Copy the complete folder into the skill location supported by your assistant, or ask the assistant to read this folder's SKILL.md and follow it. In compatible hosts, invoke `$technical-signals`; other hosts may use a skill picker or `@technical-signals`. Merely cloning this repository does not activate skills in every client.

## Offline calculator

Run from this skill folder with Python 3.10 or later; only the standard library is needed:

```bash
python3 scripts/signals.py examples/bars.json
```

The input is synthetic and the script only computes supplied data. It does not fetch or authenticate sources, choose investment assumptions, or place orders. Fractions such as `0.10` mean 10%. Monetary amounts and shares must use consistent scales; preserve the source and period metadata in real research.

See [calculator inputs and limits](references/calculator.md) for the schema and supported operations.
