---
name: stock-opportunity-scanner
description: Discover listed-stock opportunities from free public sources. Use for fundamental screens, good-results/bad-price divergences, hedge-fund holding changes, insider purchases, moats and supply bottlenecks, recent IPOs, post-dilution selloffs, and three-year growth/valuation screens. Distinguish private startup watchlists from investable stocks.
---

# Stock Opportunity Scanner

Find evidence-backed research candidates on demand. Use free public sources and user files; do not call metered financial-data connectors, enroll in services, or create scheduled tasks unless separately requested. Use English by default; follow an explicit request for another language.

## Scope and mode

Use the requested market, universe, horizon and exclusions. Otherwise start with US-listed operating common stocks and ADRs, a three-year horizon, and up to five finalists. Include smaller and recently listed businesses when evidence supports them. State defaults briefly. Do not silently narrow a global request to the US.

Use an attached or explicitly referenced list as the universe. A CSV with prices and market caps is not a source of fundamentals or forecasts. Preserve it, check its date and exclude ETFs, preferreds, rights, warrants and SPAC shells unless requested. Resolve issuer, exchange, class, ADR ratio, currency and corporate actions.

Read the relevant sections of [references/modes.md](references/modes.md):

| Mode | Intent |
| --- | --- |
| `earnings-gap` | Improving results/guidance alongside a price fall |
| `fund-accumulation` | New or increased disclosed holdings of active managers |
| `insider-buying` | Executives/directors committing their own capital |
| `moat-bottleneck` | Durable competitive advantage or scarce supply-chain capability |
| `ipo-emerging` | Recent listings and young public businesses approaching scale |
| `post-dilution` | Financing-related selloffs versus the actual economic dilution |
| `growth-value` | Operating/per-share growth at a supportable valuation |

For a general scan search all seven modes for leads, deduplicate issuers, and deepen the strongest. Modes are alternative discovery routes, not seven mandatory conditions for every stock. Keep profitable compounders, turnarounds and speculative emerging companies in separate comparison groups. Do not exclude all young companies for lacking profits.

## Free-source execution

Read [references/sources.md](references/sources.md) before acquisition. Start with available public search/page retrieval; the skill must work without package installation or API keys. Secondary screeners/articles may discover candidates; verify advanced ideas in original filings and issuer IR.

Use structured SEC downloads or an available EdgarTools installation when scale justifies it and access works. Follow fair-access rules with a real configured contact identity. If shell networking or a site blocks access, stop that route and use public retrieval/IR with clear source labels. Never bypass restrictions, repeatedly retry the same denial, or interpret blocked access as no results.

Use reported actuals, company guidance and labeled model scenarios when consensus is unavailable. Never invent estimates, analyst counts, holdings, transaction prices, historical expectations or missing periods. Free sources do not imply complete coverage.

1. Record scan date, price timestamps, universe, modes and lookbacks. Adjustable defaults: earnings 90 days; insiders 180 days; financing 180 days; IPOs 36 months; fund holdings the last two publicly available quarter-ends.
2. Build a lead ledger from actual retrievals. For a broad web scan aim for 15–25 distinct leads before deepening 5–10; adapt to narrow requests or data access. These are working budgets, not full-market coverage. For a file, report actual fundamental coverage and the unreviewed portion; never say every row was analyzed if it was not.
3. For each advanced lead obtain latest results, comparable prior results, balance-sheet/share-count context, current price and the source proving the trigger. Prefer two consecutive periods when testing durability. Record URL, publication date, fiscal period, units and accounting basis. Distinguish event, transaction, filing and holding dates.
4. Normalize periods, currency, shares and corporate actions. Do not sum cumulative YTD cash flows as quarters or EPS across inconsistent share bases. Separate GAAP/IFRS from adjusted metrics, recurring earnings from one-offs, FCF from SBC, and business growth from per-share growth. Do not merge incompatible XBRL tags or entity/segment facts.
5. Validate the mode-specific trigger and the strongest alternative explanation: weak guidance, peak-cycle profit, dilution, financing stress, customer loss, governance or prior overvaluation. A falling price and a good headline are only a lead.
6. Calculate valuation and, where supportable, three annual forecast periods with bear/base/bull assumptions. Use [references/math-inputs.md](references/math-inputs.md) and `scripts/research_math.py`. This offline helper computes supplied inputs; it does not fetch/verify sources or predict returns. Change operating/share assumptions as well as multiples across scenarios.
7. Rank by evidence, business durability, valuation under conservative assumptions, catalysts and downside. Use High/Medium/Low confidence and research-priority buckets, not invented precision. Missing-price or unproven-exposure names stay on the watchlist. Return fewer than requested when justified.

## Output

Default to an English chat comparison with direct source links and short finalist notes. Use the user's chosen format. Create a file only if requested or materially useful, following the environment's persistent-file workflow; never write research outputs into this skill's folder.

Include:

- Coverage: universe supplied, leads discovered, companies with verified fundamentals, names deeply reviewed, gaps and as-of date.
- Compact table: ticker/exchange, mode, price/date, verified trigger, revenue/EPS growth with periods and source type, relevant multiple, three-year valuation range, risk and confidence. Move detailed forecasts below the table for mobile readability.
- For top names: why now; possible market misjudgment labeled as inference; moat/management evidence; catalyst; strongest rejection argument; thesis falsifier; unverified items.
- Forecasts: current actuals plus each next fiscal year for revenue, net income attributable to common, diluted EPS and relevant cash-flow/per-share figures. Add common book equity and book value per share when supportable/relevant. Distinguish book equity, market cap and estimated fair equity value. Clarify whether "net worth" means book equity or an estimated equity valuation rather than silently substituting one meaning.
- When ownership matters: manager/insider name, class/instrument, quantity/change, holding/transaction date, filing date and original link, with reporting limitations.
- A few rejected false positives and concrete rejection reasons for broad scans.

Present research candidates; distinguish speculative, valuation-gated and evidence-incomplete ideas.

## Existing skills

Keep this skill self-contained. For requested deeper work, if Public Equity Investing is installed, discover/read its current `earnings-deep-dive`, `event-driven-analyzer`, `comps-valuation`, `three-statement-model-builder`, `long-short-pitch` or `idea-generation` as relevant. Preserve the free-public-source constraint. Do not require a paid connector or hardcode a plugin version.

## Invocation examples

- `@stock-opportunity-scanner Run a broad scan for up to five stocks with a three-year horizon, using free public sources.`
- `@stock-opportunity-scanner Screen the attached universe for falling prices despite improving results; state how many companies you actually reviewed.`
- `@stock-opportunity-scanner Find disclosed fund accumulation and insider purchases, with transaction and filing dates.`
- `@stock-opportunity-scanner Find IPOs from the past two years and post-dilution selloffs; separate profitable businesses from young loss-making companies.`
- `@stock-opportunity-scanner Find supply bottlenecks in power infrastructure for data centers and build three-year scenarios.`
