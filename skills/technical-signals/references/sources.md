# Sources and retrieval — technical signals

| Source | Free route | Limit |
| --- | --- | --- |
| Exchange/issuer corporate-action notices | Official actions and calendars | Necessary for splits, consolidations and halts |
| [Yahoo Finance history](https://finance.yahoo.com/) | Available historical symbol pages / user exports | Delays and adjustment defaults vary; check actual field definitions |
| [Stooq](https://stooq.com/) | Public historical series where provided | Market coverage, adjustment method and timing must be checked |
| [Nasdaq](https://www.nasdaq.com/) | Symbol history, movers and market activity | Data may be delayed, limited or temporarily unavailable |
| [Finviz](https://finviz.com/) | Public technical screens | Discovery rather than a verified historical signal |
| [TradingView](https://www.tradingview.com/) | Public charts/screens available without a paid plan | Do not imply access to restricted exports or full-universe history |
| [Barchart](https://www.barchart.com/) | Public highs/lows and movers | Limited rows/history; check regular versus extended sessions |
| User OHLCV CSV/JSON | Export with provider and date metadata | Validate units, completeness, split/volume adjustments |
| [yfinance](https://github.com/ranaroussi/yfinance) | Optional existing open-source client | Unofficial Yahoo client; verify current API/terms, adjustment flags and live access |

Queries: `<market> stocks above 200 day moving average <date>`, `"<ticker>" historical prices`, `"<ticker>" stock split`, `<market> unusual volume <date>`. Recompute the candidate's signal from dated bars. A source reporting “52-week high” may use a calendar-year rather than a 252-session window; preserve that distinction.

SEC filings and 13F are not OHLCV feeds. If reliable bars cannot be obtained, return reported/unverified leads separately, without verified trigger percentages or levels. No live connector is assumed by the calculator.
