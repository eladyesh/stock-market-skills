# Offline technical calculator

Run `python3 scripts/signals.py examples/bars.json`. Python 3.10+; standard library only.

## Input

Required metadata: `symbol`, `exchange`, `currency`, `timezone`, `source`, `retrieved_at`, `as_of` (YYYY-MM-DD), `session: "regular"`, `completed: true`, `price_basis: "split_adjusted"`, `volume_basis: "split_adjusted"`. Provide `bars` in ascending unique session-date order, each with `date`, `open`, `high`, `low`, `close`, and `volume`.

The caller must establish source authenticity, exchange calendar, completeness, adjustment method and whether the bar is final. The calculator rejects malformed OHLC, future bars, nonfinite/negative inputs, duplicate or unordered dates, partial sessions and a dividend-adjusted close basis. It cannot infer or repair splits and cannot prove that a caller's adjustment label is accurate.

## Output and exact coverage

- Close-to-close daily return and an absolute move at least 10%.
- SMA50 and SMA200, with previous/current averages and a two-session price-cross test. Current average needs N closes; a new cross needs N+1.
- Current volume divided by the mean of the **20 prior sessions**. Zero mean or missing history gives null, not infinity. Default unusual-volume threshold is 2×.
- New high/low versus 252 **prior** sessions, separately for intraday highs/lows and closing prices. This requires 253 bars and is a 252-session proxy for 52 weeks, not exact calendar 52-week history.
- `unavailable` flags for insufficient history; null indicator does not mean no signal.

The script does not implement RSI, ATR, golden/death crosses, live intraday baselines, liquidity filters, event-calendar checks or relative benchmark returns. Calculate these separately if requested and sourced, or report the gap. It prints JSON and returns status 2 with JSON stderr on invalid input.

The synthetic fixture uses a fictional symbol and weekday dates, not a validated exchange calendar. Its final price/volume jump demonstrates crossings and baselines. Do not reuse its metadata as proof of a real current trading signal.
