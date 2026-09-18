# Stock Market Skills

Reusable AI research skills for finding and investigating stock-market opportunities with free public information.

The first skill, **Stock Opportunity Scanner**, combines seven discovery methods with source checks, three-year valuation scenarios, and five deterministic Python calculation commands. Run it manually whenever you want to investigate a market, a theme, a watchlist, or a specific event.

**No paid financial-data subscription or API key is required for the core workflow.** Your AI assistant still needs public web access for current research. The calculation helper runs entirely offline, while AI subscriptions, inference, and hosting may have their own costs.

## Contents

- [Available skills](#available-skills)
- [Quick start](#quick-start)
- [Seven discovery modes](#seven-discovery-modes)
- [Example research prompts](#example-research-prompts)
- [What a scan returns](#what-a-scan-returns)
- [Free data sources and coverage](#free-data-sources-and-coverage)
- [Run the Python examples](#run-the-python-examples)
- [Calculation details](#calculation-details)
- [Repository structure](#repository-structure)
- [Validation and contributions](#validation-and-contributions)

## Available skills

| Skill | Purpose | Entry point |
| --- | --- | --- |
| Stock Opportunity Scanner | Discover, investigate, and compare equity research candidates across fundamentals, ownership, events, and valuation | [SKILL.md](skills/stock-opportunity-scanner/SKILL.md) |

Each skill lives in its own folder under `skills/`, so additional skills can be added independently.

## Quick start

### Use the skill with an AI assistant

1. Clone or download this repository.
2. Give your assistant access to the complete `skills/stock-opportunity-scanner/` folder, including its references and script.
3. Ask the assistant to read `SKILL.md` and follow it for your research request.
4. Enable the assistant's public web search/page retrieval. Enable Python execution if you want it to use the bundled arithmetic helper.

A first prompt:

```text
Use the Stock Opportunity Scanner skill in skills/stock-opportunity-scanner/.
Find up to five US-listed stocks worth researching over a three-year horizon.
Use free public sources and all seven discovery modes. Explain the current
valuation, evidence behind each signal, downside risks, and what would
invalidate each thesis. State how many companies you actually reviewed.
```

The assistant performs source discovery and judgment. The Python script performs arithmetic on inputs already collected and checked. Running the script alone does not launch an internet stock search.

### Codex

Use the skill installer to install `skills/stock-opportunity-scanner` from this repository, or place the complete skill folder in a supported local skills location such as `.agents/skills/` within your working repository. Then invoke it with `$stock-opportunity-scanner`.

For example, from a clone of this repository on a Unix-like system:

```bash
mkdir -p .agents/skills
cp -R skills/stock-opportunity-scanner .agents/skills/
```

Run this copy command once; inspect an existing destination before replacing it. If you edit the source skill later, update the installed copy deliberately.

### ChatGPT Work

When the skill has been installed in your account, type `@` and select **Stock Opportunity Scanner**. Uploading or linking a repository does not itself guarantee installation; use the skill-management capabilities available in your environment to install the folder. For distribution across supported ChatGPT surfaces, a skill can also be packaged in a plugin.

See the [official skill documentation](https://learn.chatgpt.com/docs/build-skills) for current installation and invocation behavior. Documentation and default output are in English; you can explicitly request another output language.

## Seven discovery modes

| Mode | Starting signal | What the research must establish |
| --- | --- | --- |
| `earnings-gap` | A falling share price alongside improving results | Whether guidance, cash conversion, expectations, or earlier overvaluation explain the decline |
| `fund-accumulation` | Newly disclosed or increased holdings of active managers | Comparable quantities, reporting dates, corporate actions, amendments, and the manager's mandate |
| `insider-buying` | Officers or directors committing capital | The actual transaction type, purchase terms, economic owner, size, and significance |
| `moat-bottleneck` | A difficult-to-replace product, capability, or supply constraint | Evidence of durable advantage and its contribution to issuer revenue, margins, or returns |
| `ipo-emerging` | Recent listings or young public companies approaching scale | Commercial milestones, unit economics, liquidity, cash runway, and dilution exposure |
| `post-dilution` | A selloff around an equity financing | Economic dilution after cash proceeds, financing terms, use of funds, and further funding needs |
| `growth-value` | Strong operating and per-share growth | A supportable valuation, sustainable economics, and realistic forward assumptions |

Modes are alternative discovery routes. A stock does not need to pass all seven. Profitable compounders, turnarounds, and speculative emerging businesses are compared separately.

Default scope is US-listed operating common stocks and ADRs, up to five finalists, and a three-year horizon. A request can change the region, universe, sector, size, exclusions, number of results, or horizon.

Default discovery windows are 90 days for earnings, 180 days for insider transactions and financing, 36 months for IPOs, and the last two publicly available quarter-ends for fund holdings. These are adjustable research settings, not optimized trading signals.

## Example research prompts

Use `@stock-opportunity-scanner` in a supporting ChatGPT skill selector, `$stock-opportunity-scanner` in Codex, or name the skill directly in your assistant.

### Good results, weak stock price

```text
Find companies whose shares fell at least 15% over the past three months
despite improving revenue, recurring operating profit, and cash conversion.
Check the latest guidance and starting valuation. Show the strongest
explanation for why the market may be right to mark each stock down.
```

### Fund accumulation and insider purchases

```text
Find companies with increasing disclosed ownership by several independent
active managers. Name the managers and show quarter-end and filing dates.
Then look for actual officer or director purchases. Keep stock holdings,
options, share awards, and company buybacks separate.
```

### Moats and supply bottlenecks

```text
Investigate power infrastructure bottlenecks for data centers. Find listed
suppliers with hard-to-replace capabilities, and connect the opportunity to
disclosed orders, revenue, or margins. Test competing capacity, substitution,
customer concentration, and whether the current price already reflects growth.
```

### IPOs and emerging businesses

```text
Find companies listed in the last two years that are approaching commercial
scale. Compare paid deployments, repeat orders, gross-profit growth, cash
runway, and fully diluted share counts. Separate profitable companies from
loss-making businesses that may need another financing round.
```

### Post-dilution opportunities

```text
Find stocks that fell after a completed equity raise in the past six months.
Calculate net proceeds, ownership dilution, and a cash-adjusted theoretical
post-issue price. Check whether the financing supports per-share growth or
merely delays financial distress.
```

### Three-year growth and valuation

```text
Find businesses with a credible path to double-digit revenue and diluted-EPS
growth over three years. Show annual bear, base, and bull assumptions for
revenue, margins, shares, and valuation. Separate company guidance, dated
analyst consensus, and your own model scenarios.
```

### Work from a supplied universe

```text
Screen the attached stock list using earnings-gap and growth-value modes.
Preserve the original file, verify fresh prices and financials for finalists,
and report the reviewed portion and remaining coverage gaps. Do not describe
a partial review as a complete scan of the file.
```

For private startups, request a separate private-company watchlist. The skill checks listing status and does not invent a tradable ticker or imply access to private shares.

## What a scan returns

A completed research run should contain:

1. **Scope and coverage:** as-of date, universe, modes, actual companies reviewed, and missing data.
2. **Candidate comparison:** ticker/exchange, current price and timestamp, evidenced trigger, growth, relevant valuation, risk, and confidence.
3. **Finalist analysis:** why now, possible market misjudgment, moat and management evidence, catalyst, strongest rejection argument, and thesis falsifier.
4. **Scenarios:** current actuals and the next three fiscal years of revenue, income attributable to common shareholders, diluted EPS, and relevant per-share metrics.
5. **Ownership evidence:** named manager/insider, instrument, quantity, transaction/holding date, filing date, and original source.
6. **Rejected leads:** concrete reasons apparent opportunities did not survive scrutiny.

Book equity and book value per share are included when relevant and supported by an explicit equity bridge. They remain distinct from market capitalization, enterprise value, and an estimated fair equity value.

Results are research priorities. The skill may return fewer than five names, put a candidate on a watchlist, or leave a valuation question open when evidence is insufficient. It does not place trades.

## Free data sources and coverage

| Source | Useful for | Main limitation |
| --- | --- | --- |
| [SEC EDGAR APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | Filing histories and standardized financial facts | Requires normalization; does not include prices, consensus, or every custom KPI |
| Issuer investor-relations pages | Results, guidance, presentations, and prospectuses | Company-defined metrics and management claims need interpretation |
| [SEC ownership disclosures](https://www.sec.gov/edgar/search/) | 13F holdings, Form 4 transactions, and other ownership reports | Reporting dates and scope differ; disclosure is not a live complete trading book |
| [FCA National Storage Mechanism](https://www.fca.org.uk/markets/primary-markets/regulatory-disclosures/national-storage-mechanism) and [HKEX announcements](https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=en) | Relevant international issuer and ownership disclosures | Coverage must be established for each jurisdiction |
| [EdgarTools](https://github.com/dgunning/edgartools), optional | Parsing SEC filings in Python | The library must be available in the host; its hosted service is a separate product |
| [yfinance](https://ranaroussi.github.io/yfinance/), optional | Public price histories | Unofficial provider interface, subject to terms, limits, and availability |

The core workflow can use public web retrieval without either optional package. Neither package nor a paid data connector is bundled or installed automatically.

Important interpretation rules:

- 13F reports are generally due within 45 days after quarter-end and do not provide a complete global or net portfolio. Increased market value alone does not establish buying. See the [SEC 13F FAQ](https://www.sec.gov/rules-regulations/staff-guidance/division-investment-management-frequently-asked-questions/frequently-asked-questions-about-form-13f).
- Insider purchase code P can include private purchases. Grants, exercises, tax withholding, and company buybacks are different transactions.
- A year-over-year improvement is not an earnings beat without comparable pre-release consensus.
- Revenue growth does not ensure EPS growth when share issuance outpaces profit growth.
- A negative-to-positive EPS transition has no meaningful conventional positive-base CAGR.
- Banks, insurers, REITs, and industrial companies need different valuation and leverage measures.
- Fresh market prices, matching fiscal periods, currencies, share classes, and corporate actions must be checked before comparing multiples.

A web-based run is a bounded research process. Exhaustive numerical screening of thousands of companies requires a structured dataset, acquisition work, normalization, and actual coverage checks. The skill reports the scope it completed.

## Run the Python examples

Requirements: **Python 3.10 or later**. The helper uses only the standard library. All files in `examples/` are explicitly synthetic and contain no real investment signals.

Run these commands from the repository root:

```bash
python3 skills/stock-opportunity-scanner/scripts/research_math.py screen examples/stock-opportunity-scanner/screen.json
python3 skills/stock-opportunity-scanner/scripts/research_math.py forecast examples/stock-opportunity-scanner/forecast.json
python3 skills/stock-opportunity-scanner/scripts/research_math.py dilution examples/stock-opportunity-scanner/dilution.json
python3 skills/stock-opportunity-scanner/scripts/research_math.py holdings examples/stock-opportunity-scanner/holdings.json
python3 skills/stock-opportunity-scanner/scripts/research_math.py insiders examples/stock-opportunity-scanner/insiders.json
```

To save a result:

```bash
python3 skills/stock-opportunity-scanner/scripts/research_math.py forecast examples/stock-opportunity-scanner/forecast.json --output output/forecast.json
```

Input definitions and assumptions are documented in [math-inputs.md](skills/stock-opportunity-scanner/references/math-inputs.md). The command exits with code 2 and an error message for rejected input.

## Calculation details

| Command | Output | Key boundary |
| --- | --- | --- |
| `screen` | Growth rates, valuation ratios, leverage where appropriate, relative returns, discovery flags | Calculates supplied rows; no data collection or overall buy score |
| `forecast` | Annual revenue, profit, diluted-share proxy, EPS, optional book equity, and terminal P/E valuation | Explicit assumptions; terminal losses have no P/E price target |
| `dilution` | Proceeds, share expansion, ownership dilution, theoretical post-issue price, and pro-forma EV | Plain completed primary common-share offerings only |
| `holdings` | Split-adjusted disclosed quantity changes and disclosed-table weights | Requires reconciled identifiers, amendments, units, and manager overlap |
| `insiders` | Cash-purchase candidates and exclusions | Notes and economic-owner identity still need source verification |

### Units and assumptions

- Rates use decimal fractions: `0.15` means 15%.
- Keep monetary and share units consistent. Money and shares both in millions produce a correct per-share amount.
- Missing values are omitted or `null`; they are not assumed to be zero.
- Forecast arrays contain one value per fiscal year.
- A full research run uses bear/base/bull cases, even though the helper accepts one case for focused arithmetic.
- Forecast returns are price-only and exclude dividends.
- Forecast shares are a simplified diluted-share proxy. A full financial model must distinguish weighted-average EPS shares from end-period valuation shares.
- Source fields retain supplied provenance. The helper does not independently verify the source or its contents.

### A dilution example

The synthetic offering example starts with 100 million shares at $20 and issues 20 million shares at $12, with $4 million of fees:

- Net proceeds: `20 × 12 − 4 = $236 million`.
- Share-count expansion: `20 / 100 = 20%`.
- Old-holder ownership dilution: `20 / 120 = 16.67%`.
- Theoretical post-issue price: `(100 × 20 + 236) / 120 = $18.6333`.

At a supplied post-event quote of $16, the price is 14.13% below that theoretical figure. This is a useful question for research, not proof of undervaluation: the calculation holds pre-event business value constant.

The forecast example demonstrates another failure mode: 15% annual profit growth with 20% annual share growth produces approximately **4.17% annual EPS decline**.

## Repository structure

| Path | Contents |
| --- | --- |
| [skills/stock-opportunity-scanner/SKILL.md](skills/stock-opportunity-scanner/SKILL.md) | Main workflow and discovery routing |
| [skills/stock-opportunity-scanner/references/modes.md](skills/stock-opportunity-scanner/references/modes.md) | Detailed checks for all seven modes |
| [skills/stock-opportunity-scanner/references/sources.md](skills/stock-opportunity-scanner/references/sources.md) | Public-source strategy and coverage limitations |
| [skills/stock-opportunity-scanner/references/math-inputs.md](skills/stock-opportunity-scanner/references/math-inputs.md) | Calculation input contracts |
| [skills/stock-opportunity-scanner/scripts/research_math.py](skills/stock-opportunity-scanner/scripts/research_math.py) | Offline calculation CLI |
| [skills/stock-opportunity-scanner/agents/openai.yaml](skills/stock-opportunity-scanner/agents/openai.yaml) | Display name, default prompt, and invocation metadata |
| [examples/stock-opportunity-scanner/](examples/stock-opportunity-scanner/) | Five synthetic JSON inputs |
| [tests/test_research_math.py](tests/test_research_math.py) | Financial arithmetic and interpretation regression checks |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Guidance for adding and maintaining skills |

## Validation and contributions

Run the tests from the repository root:

```bash
python3 -m unittest discover -s tests -v
```

The checks cover economic versus ownership dilution, EPS decline despite revenue growth, loss-making valuation, split adjustments, incomplete holdings tables, duplicate records, and the separation of grants from purchases. They validate calculation behavior, not stock-selection performance or investment returns.

To add another skill, create `skills/<skill-name>/SKILL.md` with its own focused workflow and only the references/scripts it needs. Add a row to the skill catalog above and provide runnable synthetic examples for executable helpers. See [CONTRIBUTING.md](CONTRIBUTING.md).

Public Equity Investing can optionally support deeper earnings analysis, valuation models, and full investment theses when installed in the host. That plugin is not included in this repository and is not required for the scanner.
