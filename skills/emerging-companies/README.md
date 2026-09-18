# Emerging Companies — סטארטאפים וחברות צעירות

Find recent IPOs and young public businesses with measurable traction or profit inflections, and maintain a separate private-startup watchlist.

This is a standalone Agent Skill. Read [SKILL.md](SKILL.md) for the agent workflow and [sources.md](references/sources.md) for the source map and retrieval queries. The instructions work with an assistant's available public search/page tools; no paid data subscription is required.

## Inputs and defaults

Optional sectors, countries, listing lookback, loss tolerance, business milestone, cash-runway constraints and user universe. Default IPO lookback: 36 months, with justified older emerging businesses allowed.

User-supplied filters take precedence. Give a source file or ticker list when you want a defined universe. The assistant should state exactly which names, dates and data it managed to review. Output follows your language; the skill itself is written in English for reuse across hosts.

## What the skill does

Verify listing status and prospectus; assess customers, unit economics, moat and supply bottlenecks; model burn/runway and financing needs; reconcile share instruments and dilution; connect milestones to valuation scenarios.

The search expands through relevant free source families, follows claims into primary documents and checks contrary evidence. It can use additional free sites beyond the catalog. Public access is checked at runtime; an inaccessible or paywalled page is not silently treated as verified data. It returns fewer results when evidence is insufficient.

## What you receive

Listed profitable/scaling companies, listed loss-making/pre-revenue names, pending IPOs and private startups in separate groups, with traction, funding risks, milestones, bear/base/bull and sources.

Material inputs retain links, observation and publication dates, accounting/data basis, units and confidence. Facts, third-party claims and model assumptions remain distinguishable. An illustrative example is not presented as a current market finding.

## Example requests

```text
$emerging-companies Find recent AI-infrastructure IPOs with a credible path to profitability and compare their valuations.
```

```text
$emerging-companies אילו חברות צעירות הפסדיות מתקרבות לרווחיות? בדוק תזרים, גיוס נוסף ודילול.
```

```text
$emerging-companies Find new private startups attracting attention and separately identify listed beneficiaries with material verified exposure.
```

## Worked interpretation (synthetic)

A synthetic company has $30 million unrestricted cash and burns $5 million each quarter: historical runway is roughly six quarters. If break-even is two years away, it needs a financing scenario. A 20% share-count increase lowers existing holders’ ownership by 16.67%, before considering cash added and value per share.

These figures and names are teaching examples, not verified live transactions, forecasts or recommendations. Real ticker mentions in prompts demonstrate the request format only.

## Sources and boundaries

A private funding round does not create a tradeable ticker. LOIs and TAM slides are not revenues. Negative-to-positive income has no ordinary meaningful P/E or CAGR. Lockup expiry and a registration shelf do not themselves issue shares.

The [source reference](references/sources.md) lists primary disclosures, discovery sites, example searches and source-specific caveats. Use free pages/datasets that are actually accessible; do not assume a commercial site's paid export is part of the workflow. Search broadly, but disclose the actual coverage rather than claiming every source was searched.

## Use on its own or with other skills

The skill contains its own core workflow and local references. Follow optional named-skill handoffs in SKILL.md only when those skills are installed and their output is needed. If absent, use the documented local fallback. No sibling directory or paid connector is required to understand this skill.

Copy the complete folder into the skill location supported by your assistant, or ask the assistant to read this folder's SKILL.md and follow it. In compatible hosts, invoke `$emerging-companies`; other hosts may use a skill picker or `@emerging-companies`. Merely cloning this repository does not activate skills in every client.

## Offline calculator

Run from this skill folder with Python 3.10 or later; only the standard library is needed:

```bash
python3 scripts/dilution.py dilution examples/dilution.json
```

The input is synthetic and the script only computes supplied data. It does not fetch or authenticate sources, choose investment assumptions, or place orders. Fractions such as `0.10` mean 10%. Monetary amounts and shares must use consistent scales; preserve the source and period metadata in real research.
