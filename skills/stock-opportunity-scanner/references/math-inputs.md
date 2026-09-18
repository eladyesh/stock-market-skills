# Offline calculation inputs

Run `python3 scripts/research_math.py COMMAND INPUT.json --output OUTPUT.json` relative to the skill. Omit `--output` to print. Commands: `screen`, `forecast`, `dilution`, `holdings`, `insiders`. Use research scratch paths, not the installed skill folder. Python standard library only, no network/key/package requirement.

Supply verified inputs and retain their source records. The helper calculates; it does not retrieve or verify. Rates are decimals (0.15 = 15%), missing is null/omitted, and money/shares must have compatible units. Money and shares both in millions yield the correct price per share.

## screen

Input object: `as_of` date and `rows` list. Each row needs `ticker`; optional `sector`, `sources` and numerical fields:

`price`, `price_as_of`, `revenue_start`, `revenue_end`, `history_years`, `eps_start`, `eps_end`, `fcf`, `market_cap`, `net_debt`, `ebitda`, `shares_start`, `shares_end`, `price_return`, `benchmark_return`, `revenue_yoy`, `operating_profit_yoy`, `eps_forward`, `forecast_basis`.

Use annual/TTM EPS for `eps_end` when calculating trailing P/E, and comparable annual revenue/EPS endpoints for CAGR. Ensure equal return windows and correct market-cap dates. `forecast_basis` is `company_guidance`, `dated_consensus` or `model_scenario`. Financial/REIT sectors do not receive industrial leverage calculations. Missing price date suppresses price-based ratios. Missing sources are flagged. Output contains metrics and discovery flags, not an overall score or a recommendation. Check freshness yourself.

## forecast

Required: `base_year`, positive `revenue`, `net_income` attributable to common, positive `shares`, positive `price`, named `scenarios`. Optional `book_equity` is common equity. Each scenario needs equal-length annual arrays `revenue_growth`, `net_margin`, `share_growth`; optional positive `exit_pe`. Terminal losses have no P/E target.

For book-equity projections, also provide all four annual arrays `dividends`, `buybacks`, `net_equity_issuance`, `oci`. Zero must be an explicit assumption. Include relevant share-compensation equity credits in the reconciled equity movements without double counting. Diluted shares here are a scenario proxy; a full model separates weighted-average EPS shares from end-period valuation shares and issuance/buyback timing.

Synthetic example, not a security or real forecast:

```json
{
  "base_year": 2026, "revenue": 1000, "net_income": 100,
  "shares": 100, "price": 20, "book_equity": 500,
  "scenarios": {
    "base": {
      "revenue_growth": [0.15, 0.13, 0.10],
      "net_margin": [0.11, 0.12, 0.13],
      "share_growth": [0.02, 0.02, 0.02], "exit_pe": 18,
      "dividends": [0, 0, 0], "buybacks": [0, 0, 0],
      "net_equity_issuance": [5, 5, 5], "oci": [0, 0, 0]
    }
  }
}
```

Use bear/base/bull for a full screen; one case is allowed for a focused calculation. Years are fiscal labels. Projected returns are price-only, exclude dividends and are not predictions/consensus. Conventional income/EPS CAGR is null for nonpositive endpoints. The main skill still needs a supported valuation method for loss-making companies beyond this P/E helper.

## dilution

Required: `pre_shares`, `pre_price`, `new_shares`, `offer_price`, `fees`. Optional `post_price`. Optional `pre_cash` and `pre_debt` must be supplied together; `debt_repaid` defaults to zero. Fees are total money, not a rate. Use completed primary common issuance only.

Output distinguishes share expansion from old-holder dilution and computes theoretical ex-issue price with net cash proceeds. This holds pre-event business value fixed and is not intrinsic value. Cash/debt are pre-financing; do not count proceeds already in cash twice. Model secondary sales, warrants, convertibles and partly used ATMs separately.

## holdings

Required: `prior_as_of`, `current_as_of`, `current_filed_at`, `prior`/`current` lists. Optional `manager`, booleans `complete_prior`/`complete_current` (default false), and `prior_to_current_share_factors` mapping security ID to known split factors.

Each position needs `security_id`, `class`, `instrument` (e.g. SHARE/PUT/CALL), nonnegative `shares`/`value`, and `source`. Normalize monetary units first. Reconcile amendments, identifiers, overlapping managers and corporate actions before input; the helper rejects duplicate security/class/instrument rows. Missing positions are unknown unless that public table is declared complete. Complete public tables can still omit confidential positions.

Output compares adjusted quantities, not execution prices or trade timing. Weights are fractions of the supplied disclosed table, not fund NAV; incomplete tables yield partial weights. Newly disclosed does not prove newly purchased.

## insiders

Input: `transactions` list. Each row needs `economic_transaction_id`, `issuer`, `owner`, `code`, `instrument`, `shares`, `price`, `transaction_date`, `filing_date`, `source`. Optional `role`, `venue`, `plan_10b5_1`, boolean `notes_reviewed`.

Positive common-share code-P acquisitions are candidates. Duplicate economic IDs, grants/exercises/sales, derivatives and zero-price records are excluded. Only reviewed notes support a known `venue` of `open_market` or `private`; otherwise venue is unknown. Missing source/identity/dates or unreviewed notes prevent assertion readiness. A true readiness flag records supplied checks; it is not independent verification. Resolve amendments and joint owners before claiming a cluster.
