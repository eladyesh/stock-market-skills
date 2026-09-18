# Sources and retrieval — large buyers

| Source | Public route | Appropriate use |
| --- | --- | --- |
| [SEC EDGAR](https://www.sec.gov/edgar/search/) / [13F FAQ](https://www.sec.gov/rules-regulations/staff-guidance/division-investment-management-frequently-asked-questions/frequently-asked-questions-about-form-13f) | 13F-HR/A, SC 13D/G/A, cover and information tables | Legal entity, period and security-level disclosed holdings |
| [SEC adviser search](https://adviserinfo.sec.gov/) | Public adviser identity records | Resolve manager/entity identity; not portfolio evidence |
| [WhaleWisdom](https://whalewisdom.com/) | Free public fund/stock pages where available | Discovery; history, bulk downloads or tools may be paid |
| [Dataroma](https://www.dataroma.com/) / [Holdings Channel](https://www.holdingschannel.com/) | Available public selected-manager pages | Curated coverage, not every fund; check originals |
| Fund/manager websites | Shareholder letters, periodic reports, dated interviews | Stated strategy, selected positions and context |
| [House disclosures](https://disclosures-clerk.house.gov/FinancialDisclosure) | Public transaction/annual reports | Congress, not executive-branch coverage |
| [Senate disclosures](https://efdsearch.senate.gov/search/) | Official public search subject to access/use conditions | Transactions, ranges, ownership and dates |
| [US OGE](https://www.oge.gov/) | Public financial disclosures and access instructions | Covered executive-branch officials; some records require a request |
| [Capitol Trades](https://www.capitoltrades.com/) / [Quiver Quantitative](https://www.quiverquant.com/) | Free visible political-trade pages | Secondary discovery, not complete/current official proof |
| Bank public research / named news reports | Accessible dated analyst comments | Analyst opinions; no proof of balance-sheet transactions |
| [SAFE reserves](https://www.safe.gov.cn/en/ForexReserves/index.html) / [PBOC](http://www.pbc.gov.cn/en/) | Official reserve releases | China's reported reserve quantities versus values |
| [IMF data](https://data.imf.org/) / [World Gold Council](https://www.gold.org/goldhub/data) | Available official series and research | Check country coverage, revisions and disclosure lag |
| [HKEXnews](https://www.hkexnews.hk/), [FCA NSM](https://www.fca.org.uk/markets/primary-markets/regulatory-disclosures/national-storage-mechanism), local fund/exchange sites | Original substantial-owner or portfolio disclosures | Jurisdiction-specific timing and thresholds |

Queries: `"<manager legal name>" "13F-HR"`, `"Situational Awareness" holdings filing`, `"<issuer>" "SC 13D"`, `"<bank>" "<ticker>" upgrade <date>`, `"<official>" periodic transaction report`, `"SAFE" official reserve assets gold <month>`. Resolve the legal name before narrowing to a CIK. Search enough recent periods to distinguish persistent accumulation from one-time changes.

Use [SEC APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces) for filing discovery when available. Extract the original information table, honoring amendments, unit changes and fair-access rules. Never net stock and underlying-option amounts into an invented total exposure. A holdings aggregator is not a live holdings feed.
