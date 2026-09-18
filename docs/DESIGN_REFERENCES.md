# Design references

Reviewed during the 2026-09-18 restructuring. These references inform the architecture and source semantics; the nine workflows are independently written. External projects are not runtime dependencies.

| Reference | What informed this repository |
| --- | --- |
| [Agent Skills specification](https://agentskills.io/specification) | A focused folder with SKILL.md metadata, progressive disclosure and local references/scripts |
| [Daily Stock Analysis product page](https://dsa.zhulinsen.tech/) | Multiple data-source routes and a structured distinction between price data, news context and conclusions |
| [DSA skill entry point](https://github.com/ZhuLinsen/daily_stock_analysis/blob/1168e316269baa38752a8901331a4d7aa8b1fd07/SKILL.md) and [English guide](https://github.com/ZhuLinsen/daily_stock_analysis/blob/1168e316269baa38752a8901331a4d7aa8b1fd07/docs/README_EN.md) | Reviewed the actual application-bound stock-analysis workflow; chose standalone research skills here rather than requiring its service/API/configuration |
| [AI Hedge Fund](https://github.com/virattt/ai-hedge-fund) | A comparable public example of separating investment-analysis perspectives; not a data source or performance endorsement |
| [EdgarTools](https://github.com/dgunning/edgartools) | Optional open-source tooling for filing work; this repository's instructions also support plain public retrieval |
| [SEC public APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) | Source discovery and historical XBRL data without a paid data subscription |
| [SEC Form 13F FAQ](https://www.sec.gov/rules-regulations/staff-guidance/division-investment-management-frequently-asked-questions/frequently-asked-questions-about-form-13f) | Holdings/reporting dates, security coverage, amendments, options treatment and units |
| [SEC insider bulletin](https://www.sec.gov/files/forms-3-4-5.pdf) | Insider transaction codes and the need to distinguish purchases from awards/exercises |
| [OIC options basics](https://www.optionseducation.org/optionsoverview/options-basics) / [Cboe statistics](https://www.cboe.com/markets/us/options/market-statistics) | Contract/activity terminology and the distinction between available aggregate data and a trade tape |
| [FINRA short-interest guidance](https://www.finra.org/investors/insights/short-interest) | Short interest and short-sale volume are different measurements |
| [ICI flow releases](https://www.ici.org/research/stats/flows) / [SAFE reserves](https://www.safe.gov.cn/en/ForexReserves/index.html) | Preserve dataset period/category and distinguish quantities from values |

DSA was read as an implementation example, not copied as a strategy. Its application configuration, model-provider keys, notification channels and scheduled jobs are not required or installed here. Source fallbacks, clear evidence boundaries and small standalone workflows fit this repository's stated purpose.

The catalog deliberately does not promise live free options tapes, complete social-platform coverage or universal three-year consensus access. Those capabilities depend on the available source in the execution environment.
