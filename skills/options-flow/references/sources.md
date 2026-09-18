# Sources and retrieval — options

| Source | Free route | Limits to carry into the report |
| --- | --- | --- |
| [Cboe statistics](https://www.cboe.com/markets/us/options/market-statistics) | Public market statistics and dated releases | Broad totals are not a single-stock trade tape |
| [OCC market data](https://www.theocc.com/market-data/market-data-reports) | Public volume / open-interest reports | Check dataset coverage, timestamp and units |
| [OIC options basics](https://www.optionseducation.org/optionsoverview/options-basics) | OCC educational material | Contract mechanics; not live flow |
| [Nasdaq option chains](https://www.nasdaq.com/) | Symbol option-chain pages when accessible | Delays, incomplete fields and access limitations |
| [Yahoo Finance](https://finance.yahoo.com/) | Symbol options pages | Snapshot, unofficial programmatic access, usually no aggressor tape |
| [Barchart unusual activity](https://www.barchart.com/options/unusual-activity/stocks) | Available public rows | Export/history/filters can require a subscription; do not assume full access |
| [ChartExchange](https://chartexchange.com/) | Available public symbol option pages | Verify field definitions, scope and update time |
| [Benzinga](https://www.benzinga.com/) / exchange or provider public articles | Freely readable unusual-options reports | Provider characterization is an attributed secondary claim |
| [Unusual Whales](https://unusualwhales.com/) public posts | Public commentary only | Paid flow feeds are not a free dependency |
| [SEC EDGAR](https://www.sec.gov/edgar/search/) / issuer IR | Results, material events, institutional option holdings | No anonymous current trade-level flow |

Search: `"<ticker>" "unusual options" <date>`, `"<ticker>" "put volume"`, `"<ticker>" "call sweep" <date>`, `"<issuer>" earnings date`. Inspect the source rather than repeating headline sentiment. Add alternative free sources when they contribute missing contract-level evidence.

A 13F put/call row does not usually supply strike, expiry, paid premium, execution time or a complete net hedge. Report it in institutional ownership, with quarter-end and filing dates. Do not derive option premium from 13F reported underlying-security value.

For a user-provided tape, document provider, timezone, cancellations/corrections and aggregation method before calculating. No credentials or paid platform are required to produce a clearly bounded public-source investigation.
