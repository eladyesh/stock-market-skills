# Options Flow — זרימת קולים ופוטים

Find interesting option activity and explain what the available evidence actually says about contracts, premiums and possible direction.

This is a standalone Agent Skill. Read [SKILL.md](SKILL.md) for the agent workflow and [sources.md](references/sources.md) for the source map and retrieval queries. The instructions work with an assistant's available public search/page tools; no paid data subscription is required.

## Inputs and defaults

Optional underlying/watchlist, call/put filter, expiration/DTE window, observation period, size threshold and supplied tape/chain export. Defaults: latest completed session with five-session context.

User-supplied filters take precedence. Give a source file or ticker list when you want a defined universe. The assistant should state exactly which names, dates and data it managed to review. Output follows your language; the skill itself is written in English for reuse across hosts.

## What the skill does

Search public chains, exchange statistics, unusual-activity pages and reports; establish observation quality; normalize contracts and OI dates; compare historical activity; investigate spreads, rolls, event IV and alternative interpretations.

The search expands through relevant free source families, follows claims into primary documents and checks contrary evidence. It can use additional free sites beyond the catalog. Public access is checked at runtime; an inaccessible or paywalled page is not silently treated as verified data. It returns fewer results when evidence is insufficient.

## What you receive

Contract table with timestamp, data level, volume/OI, observed premium or labeled proxy, unusualness, directional confidence, event context and sources.

Material inputs retain links, observation and publication dates, accounting/data basis, units and confidence. Facts, third-party claims and model assumptions remain distinguishable. An illustrative example is not presented as a current market finding.

## Example requests

```text
$options-flow Investigate unusual DELL calls and puts today using public sources and label delayed data.
```

```text
$options-flow מצא פעילות פוטים חריגה השבוע והסבר האם אפשר לזהות קנייה או רק מחזור.
```

```text
$options-flow Analyze this chain export and separate unusual activity from verified trade-level flow.
```

## Worked interpretation (synthetic)

A call chain shows 5,000 contracts traded and 500 prior-session OI: volume/OI is 10×. The latest midpoint is $2, but there is no tape. $1 million from 5,000 × 100 × $2 is only a midpoint activity proxy; it is not verified premium spent, an opening trade, or proof of bullish buying.

These figures and names are teaching examples, not verified live transactions, forecasts or recommendations. Real ticker mentions in prompts demonstrate the request format only.

## Sources and boundaries

Free sources often lack reliable trade-level flow. Ask-side prints can suggest aggressor side but do not establish opening/closing or investor identity. A 13F option value is not paid premium.

The [source reference](references/sources.md) lists primary disclosures, discovery sites, example searches and source-specific caveats. Use free pages/datasets that are actually accessible; do not assume a commercial site's paid export is part of the workflow. Search broadly, but disclose the actual coverage rather than claiming every source was searched.

## Use on its own or with other skills

The skill contains its own core workflow and local references. Follow optional named-skill handoffs in SKILL.md only when those skills are installed and their output is needed. If absent, use the documented local fallback. No sibling directory or paid connector is required to understand this skill.

Copy the complete folder into the skill location supported by your assistant, or ask the assistant to read this folder's SKILL.md and follow it. In compatible hosts, invoke `$options-flow`; other hosts may use a skill picker or `@options-flow`. Merely cloning this repository does not activate skills in every client.
