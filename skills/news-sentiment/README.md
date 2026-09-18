# News Sentiment — חדשות וסנטימנט

Discover stocks in the news and social conversation, verify the actual claims, and separate attention, tone and business significance.

This is a standalone Agent Skill. Read [SKILL.md](SKILL.md) for the agent workflow and [sources.md](references/sources.md) for the source map and retrieval queries. The instructions work with an assistant's available public search/page tools; no paid data subscription is required.

## Inputs and defaults

Optional ticker/cashtag, company/speaker, market, language, theme, time window and news/social corpus. Defaults: 24-hour fresh events plus seven-day context.

User-supplied filters take precedence. Give a source file or ticker list when you want a defined universe. The assistant should state exactly which names, dates and data it managed to review. Output follows your language; the skill itself is written in English for reuse across hosts.

## What the skill does

Search issuer/official sources, public news and accessible social posts; resolve names; find originals and corrections; cluster duplicate stories; classify factual status and tone; quantify only a defined, comparable sample.

The search expands through relevant free source families, follows claims into primary documents and checks contrary evidence. It can use additional free sites beyond the catalog. Public access is checked at runtime; an inaccessible or paywalled page is not silently treated as verified data. It returns fewer results when evidence is insufficient.

## What you receive

Favorable, adverse, mixed and unverified event groups with original URLs/dates, attention/sample coverage, business impact, matching-window price reaction where supportable and counterevidence.

Material inputs retain links, observation and publication dates, accounting/data basis, units and confidence. Facts, third-party claims and model assumptions remain distinguishable. An illustrative example is not presented as a current market finding.

## Example requests

```text
$news-sentiment Why is BE attracting attention? Verify the company and distinguish sample observations from X-wide trends.
```

```text
$news-sentiment בדוק את הטענה שטראמפ אמר לקנות Dell: מצא מקור מקורי, תאריך והקשר.
```

```text
$news-sentiment Rank this week’s positive and negative stock catalysts, deduplicating repeated wire stories and old reposts.
```

## Worked interpretation (synthetic)

Ten articles repeat one press release and three accounts repost the same screenshot. This is one underlying company event plus an unverified social claim, not thirteen independent confirmations. Without a comparable accessible X corpus, report observed discussion rather than a platform-wide mention surge.

These figures and names are teaching examples, not verified live transactions, forecasts or recommendations. Real ticker mentions in prompts demonstrate the request format only.

## Sources and boundaries

Search-result counts are not mention volume. Viral claims, satire, translation and impersonation require context. Positive tone does not prove material earnings impact, undervaluation or causality for a price move.

The [source reference](references/sources.md) lists primary disclosures, discovery sites, example searches and source-specific caveats. Use free pages/datasets that are actually accessible; do not assume a commercial site's paid export is part of the workflow. Search broadly, but disclose the actual coverage rather than claiming every source was searched.

## Use on its own or with other skills

The skill contains its own core workflow and local references. Follow optional named-skill handoffs in SKILL.md only when those skills are installed and their output is needed. If absent, use the documented local fallback. No sibling directory or paid connector is required to understand this skill.

Copy the complete folder into the skill location supported by your assistant, or ask the assistant to read this folder's SKILL.md and follow it. In compatible hosts, invoke `$news-sentiment`; other hosts may use a skill picker or `@news-sentiment`. Merely cloning this repository does not activate skills in every client.
