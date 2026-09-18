# Stock Market Skills

**Nine independent, source-driven skills for finding stocks and investigating investment ideas with free public information.**

מאגר לקריאה, שימוש והוספת סקילים למחקר מניות: בעלי עניין, אופציות, שווי, מוסדיים, חברות צעירות, טכני, סקטורים, שורט וסנטימנט. אפשר להשתמש בכל סקיל בנפרד ולבקש תשובות בעברית או באנגלית.

This repository is a collection of research workflows for AI assistants that support Agent Skills, or can read and follow Markdown instructions. It is designed to help discover candidates, check the evidence, and evaluate what a price implies. Each skill includes its own `SKILL.md`, detailed README, source reference, examples and UI metadata. Five skills also include optional offline Python calculators.

The instructions search across relevant free filings, company reports, datasets, news, screeners and public discussions. No paid financial-data feed is required. Availability, timeliness and forecast coverage are checked on each run; a skill is not itself a live data service or a trading system.

## Skill catalog

| # | Skill | Main question | Guide / agent instructions |
| --- | --- | --- | --- |
| 1 | **Insider Buying** | Which officers, directors or significant holders are buying with their own capital? | [README](skills/insider-buying/README.md) · [SKILL](skills/insider-buying/SKILL.md) |
| 2 | **Options Flow** | Which calls or puts show unusual activity, and what direction can the evidence support? | [README](skills/options-flow/README.md) · [SKILL](skills/options-flow/SKILL.md) |
| 3 | **Fundamental Valuation** | Which stocks have three years of double-digit revenue and common-income growth at a defensible valuation? | [README](skills/fundamental-valuation/README.md) · [SKILL](skills/fundamental-valuation/SKILL.md) |
| 4 | **Institutional Ownership** | What have funds, banks, officials and other large buyers publicly disclosed? | [README](skills/institutional-ownership/README.md) · [SKILL](skills/institutional-ownership/SKILL.md) |
| 5 | **Emerging Companies** | Which recent IPOs or young companies have meaningful traction and a credible profit path? | [README](skills/emerging-companies/README.md) · [SKILL](skills/emerging-companies/SKILL.md) |
| 6 | **Technical Signals** | Which stocks show new moving-average crosses, extremes or unusual price/volume behavior? | [README](skills/technical-signals/README.md) · [SKILL](skills/technical-signals/SKILL.md) |
| 7 | **Sector Flows** | Where are fund flows moving, and which listed businesses have relevant exposure? | [README](skills/sector-flows/README.md) · [SKILL](skills/sector-flows/SKILL.md) |
| 8 | **Short Candidates** | Where do valuation, deteriorating evidence and a catalyst support a bearish research case? | [README](skills/short-candidates/README.md) · [SKILL](skills/short-candidates/SKILL.md) |
| 9 | **News Sentiment** | Which stocks are attracting attention, what happened, and is the claim verified? | [README](skills/news-sentiment/README.md) · [SKILL](skills/news-sentiment/SKILL.md) |

## Read and use a skill

1. Open a skill's README to see inputs, outputs, worked interpretations and example requests.
2. Give an assistant the complete skill folder or its `SKILL.md` with access to the linked local references. For example: “Read `skills/insider-buying/SKILL.md` and follow it to investigate recent director purchases.”
3. For installation, copy/import the **whole folder** into the skill location supported by your client. Installation and discovery differ by client; cloning a repo does not automatically activate skills everywhere.
4. In hosts supporting `$skill-name`, invoke it as below. Other hosts may expose a picker or `@skill-name` syntax. The workflow also works when the assistant reads the file directly.

```bash
git clone https://github.com/eladyesh/stock-market-skills.git
cd stock-market-skills
```

```text
$insider-buying Find meaningful CEO/CFO purchases in the last 90 days.
$options-flow Investigate unusual calls and puts in DELL and label the data quality.
$fundamental-valuation Find stocks with at least 10% revenue AND net-income growth in EACH of the next three fiscal years.
$institutional-ownership Compare Situational Awareness's latest publicly disclosed portfolio with its prior filing.
$emerging-companies Find young loss-making public companies approaching profitability and model financing needs.
$technical-signals Scan for fresh SMA200 crosses, 52-week extremes and at least 2× normal volume.
$sector-flows Compare recent energy and technology fund flows and identify exposed companies.
$short-candidates Find overvalued stocks with a credible catalyst and show the strongest opposing case.
$news-sentiment Explain why BE is in the news and distinguish verified events from social rumors.
```

```text
$fundamental-valuation מצא מניות עם צמיחה דו־ספרתית בהכנסות וברווח הנקי בכל אחת משלוש השנים הבאות. הצג מקורות, מכפיל הוגן, שווי עתידי ותשואה למניה לאחר דילול.
$institutional-ownership מה Situational Awareness מחזיקה לפי הדיווח האחרון? הפרד החזקות רבעוניות, רכישות מאומתות והמלצות אנליסטים.
$news-sentiment בדוק את הטענה שטראמפ אמר לקנות Dell. מצא מקור מקורי, תאריך והקשר.
```

For a reproducible screen, include a ticker list/CSV, market, time window and exclusions. The assistant reports how many securities it could actually analyze. A quote-only CSV is a starting universe, not a source of fundamentals or estimates.

## Combine research without mixing evidence

| Starting observation | Useful next investigation |
| --- | --- |
| Management buys shares | Insider Buying → Fundamental Valuation |
| Unusual calls/puts | Options Flow → News Sentiment → Fundamental Valuation |
| A fund discloses a new stake | Institutional Ownership → Fundamental Valuation |
| Young company approaches break-even | Emerging Companies → Fundamental Valuation scenario mode |
| Sector receives reported inflows | Sector Flows → verified business exposure → Technical Signals / Fundamental Valuation |
| High valuation and adverse catalyst | Short Candidates → Fundamental Valuation + News Sentiment + Options Flow |

These are optional handoffs. Each skill contains a standalone fallback and keeps local references inside its own folder. Installing one does not require installing all nine.

## What “free-source research” means

The source maps include SEC EDGAR and its public APIs, issuer IR and prospectuses, official ownership/disclosure systems, free portions of forecast and screening sites, exchange/OCC/FINRA data, ETF issuer data, public news and accessible social posts. They also cover local markets and special channels such as OGE/House/Senate disclosures and China's official reserve reports. Sources are examples, not a closed whitelist.

Research follows material leads across multiple relevant source families and searches for contradictory evidence. It records actual source/period coverage, missing fields and access limits. It does not promise that every website is searchable, that a free page contains three forecast years, or that a social sample represents a whole platform. Free public data does not mean free unlimited API access; paid exports, logins and subscriptions are not assumed.

| Evidence | Correct interpretation |
| --- | --- |
| Form 4 code P | Purchase candidate; verify whether open market or private |
| 13F | Dated disclosed portfolio snapshot, usually delayed; not complete live holdings |
| Bank Buy rating | Analyst opinion; not proof that the bank purchased shares |
| Option-chain volume | Activity; not necessarily opening buys or directional flow |
| SEC financial statements | Reported actuals and sometimes disclosed guidance; not automatic analyst consensus |
| ETF price/AUM rise | May reflect returns; not automatically net inflow |
| FINRA short-sale volume | Trading activity; not outstanding short interest |
| Public social posts | Observed sample; no platform-wide trend without suitable coverage |

See [research standards](docs/RESEARCH_STANDARD.md) for provenance, coverage and source handling.

## Three-year valuation in practice

The growth screen checks **each** next fiscal year's revenue and common-net-income change, not just CAGR. It separates externally supported estimates from modeled or missing years and treats loss-to-profit cases as turnarounds.

For profitable companies:

```text
future equity value = fair P/E × future common net income
equity-value ratio = future equity value / current market cap
aggregate equity change = equity-value ratio − 1
future price = future equity value / future diluted valuation shares
per-share price return = future price / current price − 1
```

The fair multiple must be justified with comparable businesses, history and operating economics. The workflows include current/forward P/E, EV-based measures, cash conversion, balance sheet, EBITDA, TTM, margins and dilution where applicable. Sector-specific valuation replaces unsuitable P/E rules for banks, REITs and loss-making businesses. Future value and discounted present value remain distinct.

## Offline examples and checks

Calculators use Python 3.10+ and the standard library. They only process supplied inputs; they do not search the internet, authenticate sources, choose a fair multiple or place trades. All checked-in numerical examples are synthetic.

```bash
python3 skills/insider-buying/scripts/insiders.py insiders skills/insider-buying/examples/insiders.json
python3 skills/institutional-ownership/scripts/holdings.py holdings skills/institutional-ownership/examples/holdings.json
python3 skills/emerging-companies/scripts/dilution.py dilution skills/emerging-companies/examples/dilution.json
python3 skills/fundamental-valuation/scripts/valuation.py skills/fundamental-valuation/examples/valuation.json
python3 skills/technical-signals/scripts/signals.py skills/technical-signals/examples/bars.json
python3 -m unittest discover -s tests -v
```

For repository-format and local-link validation, install the development-only dependency if needed:

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_repo.py
```

Arithmetic tests verify financial/data-handling behavior, not an investment edge or the truth of external forecasts. See [validation scope](docs/VALIDATION.md).

## Add a skill or improve a source

This is a repository for reading, using **and contributing** research skills. Add a focused folder under `skills/`, keep it independently usable, provide a detailed README with examples and source limits, and update this catalog. See [CONTRIBUTING.md](CONTRIBUTING.md).

The former all-in-one `stock-opportunity-scanner` has been replaced by these nine focused skills. Its prior version remains in Git history; see [migration map](docs/MIGRATION.md) for where its modes and calculators moved.

## Design references

The design was informed by [Daily Stock Analysis](https://dsa.zhulinsen.tech/), its [repository and skill entry point](https://github.com/ZhuLinsen/daily_stock_analysis/blob/main/SKILL.md), the [Agent Skills specification](https://agentskills.io/specification) and other public research tooling. See [design notes and sources](docs/DESIGN_REFERENCES.md). The workflows here are independently written and do not require the DSA application, its keys or its notification system.
