#!/usr/bin/env python3
"""Offline three-year growth screening and dilution-aware P/E scenarios.

No data retrieval, source verification, fair-multiple selection or trading.
All money and share quantities must use the same scale (e.g. millions).
"""
import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path

EXTERNAL = {"company_guidance", "dated_consensus", "individual_analyst_estimate"}
KINDS = EXTERNAL | {"reported_actual", "derived_estimate", "model_scenario", "unknown"}


def number(value, label, *, positive=False, nullable=False):
    if value is None and nullable:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{label}: expected a finite number")
    if positive and value <= 0:
        raise ValueError(f"{label}: must be positive")
    return float(value)


def date(value, label):
    try:
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label}: expected YYYY-MM-DD") from None


def metric(record, key, as_of):
    item = record.get(key)
    if item is None:
        return {"value": None, "kind": "unknown", "basis": None, "source": None,
                "source_date": None, "metadata_complete": False}
    if not isinstance(item, dict):
        raise ValueError(f"{key}: expected a metric object or null")
    value = number(item.get("value"), key, nullable=True)
    kind = item.get("kind", "unknown")
    if kind not in KINDS:
        raise ValueError(f"{key}: unknown evidence kind")
    source_date = item.get("source_date")
    if source_date and date(source_date, key + ".source_date") > as_of:
        raise ValueError(f"{key}: source was published after as_of")
    complete = all(isinstance(item.get(k), str) and item[k].strip()
                   for k in ("source", "source_date", "basis"))
    return {"value": value, "kind": kind, "basis": item.get("basis"),
            "source": item.get("source"), "source_date": source_date,
            "metadata_complete": complete}


def analyze(data):
    as_of = date(data["as_of"], "as_of")
    quote_date = date(data["quote_as_of"], "quote_as_of")
    if quote_date > as_of:
        raise ValueError("quote_as_of must not be after as_of")
    if not data.get("currency") or not data.get("unit"):
        raise ValueError("currency and common money/share unit are required")
    price = number(data["price"], "price", positive=True)
    shares0 = number(data["current_shares"], "current_shares", positive=True)
    cap = number(data["market_cap"], "market_cap", positive=True)
    if not math.isclose(price * shares0, cap, rel_tol=0.01):
        raise ValueError("market_cap differs by over 1% from price × current_shares; reconcile class/ADR/units")
    threshold = number(data.get("growth_threshold", .10), "growth_threshold")
    if threshold < 0:
        raise ValueError("growth_threshold must be nonnegative")
    strict = data.get("strict_growth", False)
    if not isinstance(strict, bool):
        raise ValueError("strict_growth must be boolean")
    forecasts = data.get("forecasts")
    if not isinstance(forecasts, list) or len(forecasts) != 3:
        raise ValueError("forecasts must contain exactly three consecutive fiscal years")
    records = [data["base"]] + forecasts
    periods, parsed = [], []
    for i, record in enumerate(records):
        year = record.get("fiscal_year")
        if isinstance(year, bool) or not isinstance(year, int):
            raise ValueError("fiscal_year must be an integer")
        end = date(record["fiscal_end"], "fiscal_end")
        if i and (year != records[i-1]["fiscal_year"] + 1 or
                  not 330 <= (end - periods[-1]).days <= 400):
            raise ValueError("require consecutive comparable annual fiscal periods")
        if i == 0 and end > as_of:
            raise ValueError("base year must be completed by as_of")
        periods.append(end)
        parsed.append({key: metric(record, key, as_of) for key in ("revenue", "net_income")})
    if any(parsed[0][k]["kind"] != "reported_actual" for k in ("revenue", "net_income")):
        raise ValueError("FY0 must contain reported actual revenue and common net income")
    if parsed[0]["revenue"]["value"] is None or parsed[0]["revenue"]["value"] <= 0:
        raise ValueError("FY0 revenue must be positive")
    if parsed[0]["net_income"]["value"] is None:
        raise ValueError("FY0 common net income is required")

    rows = []
    numerical_pass = True
    complete = True
    comparable = True
    positive_income = parsed[0]["net_income"]["value"] > 0
    externally_supported = all(parsed[0][k]["metadata_complete"] for k in ("revenue", "net_income"))
    for i in range(1, 4):
        row = {"fiscal_year": records[i]["fiscal_year"], "fiscal_end": records[i]["fiscal_end"]}
        for key in ("revenue", "net_income"):
            prev, cur = parsed[i-1][key], parsed[i][key]
            same_basis = prev["basis"] is not None and prev["basis"] == cur["basis"]
            comparable &= same_basis
            complete &= cur["value"] is not None
            supported = cur["kind"] in EXTERNAL and cur["metadata_complete"]
            externally_supported &= supported
            if key == "net_income" and cur["value"] is not None:
                positive_income &= cur["value"] > 0
            growth = None
            if same_basis and prev["value"] is not None and prev["value"] > 0 and cur["value"] is not None:
                growth = cur["value"] / prev["value"] - 1
            passed = None if growth is None else (
                growth > threshold and not math.isclose(growth, threshold, abs_tol=1e-12, rel_tol=0)
                if strict else growth >= threshold or math.isclose(growth, threshold, abs_tol=1e-12, rel_tol=0))
            numerical_pass &= passed is True
            row[key] = {**cur, "yoy_growth": growth, "passes_threshold": passed,
                        "externally_supported_metadata": supported}
        rows.append(row)
    if not complete:
        status = "incomplete_forecasts"
    elif not comparable:
        status = "incompatible_accounting_bases"
    elif not positive_income:
        status = "turnaround_or_nonpositive_income"
    elif not numerical_pass:
        status = "fails_annual_growth_screen"
    elif not externally_supported:
        status = "model_or_unverified_metadata_match"
    else:
        status = "externally_supported_metadata_match"

    cagrs = {}
    for key in ("revenue", "net_income"):
        first, last = parsed[0][key]["value"], parsed[3][key]["value"]
        same = all(p[key]["basis"] == parsed[0][key]["basis"] for p in parsed)
        cagrs[key] = ((last / first) ** (1/3) - 1
                      if same and first is not None and last is not None and min(first, last) > 0 else None)

    cases = data.get("scenarios", [])
    if not isinstance(cases, list):
        raise ValueError("scenarios must be an array")
    scenario_results, seen = [], set()
    for case in cases:
        name = case.get("name")
        if not isinstance(name, str) or not name or name in seen:
            raise ValueError("scenario names must be nonempty and unique")
        seen.add(name)
        target_date = date(case["target_date"], "target_date")
        years = (target_date - quote_date).days / 365.25
        if years <= 0:
            raise ValueError("target_date must be later than quote_as_of")
        income = number(case["future_net_income"], "future_net_income")
        shares = number(case["future_shares"], "future_shares", positive=True)
        pe = number(case["fair_pe"], "fair_pe", positive=True)
        if not case.get("multiple_rationale") or not case.get("assumptions"):
            raise ValueError("each scenario needs multiple_rationale and operating/share assumptions")
        equity = pe * income if income > 0 else None
        target = equity / shares if equity is not None else None
        ratio = equity / cap if equity is not None else None
        scenario_results.append({
            "name": name, "target_date": case["target_date"], "years_from_quote": years,
            "future_net_income": income, "future_shares": shares, "fair_pe": pe,
            "future_equity_value": equity, "equity_value_ratio": ratio,
            "aggregate_equity_change": ratio - 1 if ratio is not None else None,
            "future_price": target, "per_share_price_return": target / price - 1 if target is not None else None,
            "annualized_price_return": (target / price) ** (1 / years) - 1 if target is not None else None,
            "multiple_rationale": case["multiple_rationale"], "assumptions": case["assumptions"],
            "pe_applicable": income > 0,
        })
    return {"as_of": data["as_of"], "quote_as_of": data["quote_as_of"], "currency": data["currency"],
            "unit": data["unit"], "screen_status": status, "growth_threshold": threshold,
            "strict_growth": strict, "annual_growth": rows, "three_year_cagr": cagrs,
            "scenarios": scenario_results,
            "limitations": ["Source metadata are supplied, not independently verified by this calculator.",
                            "Estimate freshness, financial normalization and fair multiples require research.",
                            "Scenarios are assumptions; future equity value is not discounted present fair value.",
                            "Price returns exclude dividends, taxes, fees and FX; no trade recommendation."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        print(json.dumps(analyze(data), ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
