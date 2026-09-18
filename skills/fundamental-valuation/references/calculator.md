# Offline valuation calculator

Run `python3 scripts/valuation.py examples/valuation.json` from this skill directory. Python 3.10+; standard library only. The helper reports annual growth coverage and supplied P/E cases; it does not fetch data, independently verify source URLs, normalize statements or estimate the fair multiple.

## Schema

| Field | Meaning |
| --- | --- |
| `as_of`, `quote_as_of` | YYYY-MM-DD analysis and quote dates; quote cannot be later |
| `currency`, `unit` | Currency and common scale for money and shares, e.g. USD / millions |
| `price`, `current_shares`, `market_cap` | Positive inputs; cap must reconcile to price × shares within 1% |
| `growth_threshold`, `strict_growth` | Fraction, default 0.10; strict comparison optional, default inclusive |
| `base` | Latest reported full-year fiscal year/end, revenue and common net income |
| `forecasts` | Exactly three consecutive comparable fiscal-year records after base |
| `scenarios` | Optional array of terminal P/E cases with unique names |

Each period has `fiscal_year` (integer label), `fiscal_end` (YYYY-MM-DD), and `revenue` / `net_income` metric objects. Each metric object contains `value`, `kind`, `basis`, `source` and `source_date`. `value` can be null for missing forecasts; the whole forecast metric can also be null. The base must have positive revenue and a known common-net-income actual. Supported kinds: `reported_actual`, `company_guidance`, `dated_consensus`, `individual_analyst_estimate`, `derived_estimate`, `model_scenario`, `unknown`. Source dates after the analysis date are rejected.

Keep basis labels identical only for genuinely comparable figures. Adjusted net income against GAAP base income should not pass without a researched reconciliation. Caller must convert currency/scale consistently. A fiscal year may have ended but still be an estimate until reported; the caller establishes which is the latest reported base.

Each P/E scenario contains `name`, `target_date`, `future_net_income`, `future_shares`, `fair_pe`, `multiple_rationale`, and `assumptions`. Nonpositive future income produces null P/E valuation, not a negative target price. This simplified helper handles terminal common-equity P/E only: use a separate explicit model for EV bridges, DCF, multi-class rights or dividends. Align `future_net_income` to the intended target multiple's fiscal period in the stated assumptions.

## Interpretation

`externally_supported_metadata_match` means all six annual growth comparisons passed and caller-supplied metadata describe compatible external estimates. It does **not** mean the program opened or verified them. `model_or_unverified_metadata_match` is separate. Other statuses identify missing periods, incompatible accounting bases, nonpositive/turnaround income or a failed annual test.

The calculator returns the future-equity/current-cap ratio, ratio minus one, future price, per-share price return and annualized price return using actual days/365.25. It rejects nonfinite inputs and inconsistent periods/capitalization. It prints JSON; errors go to stderr with exit status 2. The checked-in input is explicitly fictional and labels all forward values as model scenarios.
