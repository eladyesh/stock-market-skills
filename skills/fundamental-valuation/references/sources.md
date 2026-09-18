# Sources and retrieval — fundamental valuation

## Search ladder

1. Establish reported facts from issuer IR, audited statements and official filings.
2. Look for dated management guidance, investor-day targets and capital-market-day slides, including reconciliation tables.
3. Search several free forecast/financial sites and public analyst summaries for each needed future year.
4. Cross-check economically important estimates against recent company developments and independent evidence.
5. Keep any remaining year unknown; build a separately labeled scenario only with disclosed assumptions.

| Source | Useful public material | Limits |
| --- | --- | --- |
| [SEC EDGAR](https://www.sec.gov/edgar/search/) | 10-K, 10-Q, 20-F, 6-K, 8-K exhibits, prospectuses, proxies | Historical actuals and disclosed management outlook; not a consensus database |
| [SEC XBRL APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | CompanyFacts, submissions and bulk data, no API key | Standard entity-level tags; no stock quote or complete custom/segment coverage |
| Issuer IR and exchange announcements | Earnings releases, presentations, guidance, share/debt notes | Management targets are not independent consensus |
| [Stock Analysis](https://stockanalysis.com/) | Public financials, estimates and analyst pages; e.g. symbol `/forecast/` | Number of visible forecast years varies; some detail is gated |
| [Yahoo Finance](https://finance.yahoo.com/) | Analysis, financials, statistics and historical prices | Forecast horizon and basis vary; public access can change |
| [MarketScreener](https://www.marketscreener.com/) | Public financial/forecast tables where readable | Some cells/history require login or payment |
| [Investing.com](https://www.investing.com/) / [Nasdaq](https://www.nasdaq.com/) | Public estimates and dated earnings/analyst articles | Verify period, publisher and delayed data |
| [Finviz](https://finviz.com/) | Discovery filters and snapshot ratios | Forward EPS or growth fields do not supply three annual common-income forecasts |
| [Macrotrends](https://www.macrotrends.net/) | Public historical comparisons where available | Historical series are not forecasts |
| [MAYA](https://maya.tase.co.il/) / [MAGNA](https://www.magna.isa.gov.il/), [HKEXnews](https://www.hkexnews.hk/), [FCA NSM](https://www.fca.org.uk/markets/primary-markets/regulatory-disclosures/national-storage-mechanism) | Local filings for international coverage | Normalize currency, GAAP/IFRS and fiscal calendars |
| [FRED](https://fred.stlouisfed.org/), [Damodaran data](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/data.html) | Rates, sector valuation/return context | Dated aggregate context, not a replacement for live peers or forecasts |

Search examples: `"<issuer>" "FY2029" revenue net income`, `"<issuer>" "investor day" targets`, `"<ticker>" analyst estimates revenue EPS`, `"<issuer>" guidance revised`. Replace years dynamically; never anchor the skill to these example years. Check conflicting or pessimistic outlooks as well as optimistic ones.

SEC endpoints: `https://data.sec.gov/submissions/CIK##########.json`, `https://data.sec.gov/api/xbrl/companyfacts/CIK##########.json`. Use real configured contact identity, current fair-access rules, caching and incremental/bulk data for large screens. Respect denied access and use available page retrieval/IR alternatives.

Normalize duration versus instant contexts, fiscal years, restated versus originally available facts and unit multipliers. Derive standalone quarters from cumulative YTD values before building TTM. Do not sum overlapping annual/YTD values, mix entity and segment facts, or backtest against facts published after the test date. Optional libraries such as [EdgarTools](https://github.com/dgunning/edgartools) and [yfinance](https://github.com/ranaroussi/yfinance) are not required; verify their current APIs and access terms before use.
