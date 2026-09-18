#!/usr/bin/env python3
"""Compute defined daily technical signals from supplied completed-session OHLCV.

No network access, exchange-calendar verification, adjustment repair or trade advice.
"""
import argparse
import datetime as dt
import json
import math
import statistics
import sys
from pathlib import Path


def finite(value, field, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{field}: expected a finite number")
    if (positive and value <= 0) or (not positive and value < 0):
        raise ValueError(f"{field}: invalid negative or zero value")
    return float(value)


def analyze(data):
    for field in ("symbol", "exchange", "currency", "timezone", "source", "retrieved_at"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            raise ValueError(f"{field} is required")
    if data.get("session") != "regular" or data.get("completed") is not True:
        raise ValueError("calculator supports completed regular sessions only")
    if data.get("price_basis") != "split_adjusted" or data.get("volume_basis") != "split_adjusted":
        raise ValueError("supply consistently split-adjusted OHLC and volume; dividend-adjusted close is not supported")
    bars = data.get("bars")
    if not isinstance(bars, list) or len(bars) < 2:
        raise ValueError("at least two OHLCV bars are required")
    prior = None
    normalized = []
    for bar in bars:
        try:
            day = dt.date.fromisoformat(bar["date"])
        except (TypeError, ValueError, KeyError):
            raise ValueError("bar date must be YYYY-MM-DD") from None
        if prior is not None and day <= prior:
            raise ValueError("bar dates must be unique and ascending")
        prior = day
        row = {k: finite(bar[k], k, positive=True) for k in ("open", "high", "low", "close")}
        row["volume"] = finite(bar["volume"], "volume")
        if row["low"] > min(row["open"], row["close"]) or row["high"] < max(row["open"], row["close"]):
            raise ValueError("OHLC range is inconsistent")
        normalized.append(row)
    try:
        as_of = dt.date.fromisoformat(data["as_of"])
    except (ValueError, TypeError, KeyError):
        raise ValueError("as_of must be YYYY-MM-DD") from None
    if prior > as_of:
        raise ValueError("bars include a session after as_of")
    last, prev = normalized[-1], normalized[-2]
    closes = [b["close"] for b in normalized]
    result = {"symbol": data["symbol"], "as_of": data["as_of"], "session_date": bars[-1]["date"],
              "price": last["close"], "bar_count": len(bars), "source": data["source"],
              "price_basis": data["price_basis"], "volume_basis": data["volume_basis"],
              "daily_return": last["close"] / prev["close"] - 1,
              "moving_averages": {}, "signals": [], "unavailable": []}
    for window in (50, 200):
        current = statistics.mean(closes[-window:]) if len(closes) >= window else None
        previous = statistics.mean(closes[-window-1:-1]) if len(closes) >= window+1 else None
        cross_up = cross_down = None
        if previous is not None:
            cross_up = prev["close"] <= previous and last["close"] > current
            cross_down = prev["close"] >= previous and last["close"] < current
            if cross_up:
                result["signals"].append(f"cross_above_sma{window}")
            if cross_down:
                result["signals"].append(f"cross_below_sma{window}")
        else:
            result["unavailable"].append(f"sma{window}_cross_requires_{window+1}_bars")
        result["moving_averages"][str(window)] = {
            "previous": previous, "current": current, "cross_up": cross_up, "cross_down": cross_down}
    volume_base = statistics.mean(b["volume"] for b in normalized[-21:-1]) if len(bars) >= 21 else None
    rvol = last["volume"] / volume_base if volume_base is not None and volume_base > 0 else None
    result.update({"prior_20_mean_volume": volume_base, "relative_volume": rvol})
    if rvol is None:
        result["unavailable"].append("relative_volume_needs_20_prior_sessions_with_positive_mean_volume")
    elif rvol >= 2:
        result["signals"].append("relative_volume_at_least_2x")
    large_move = abs(result["daily_return"]) >= .10 or math.isclose(abs(result["daily_return"]), .10, abs_tol=1e-12, rel_tol=0)
    if large_move:
        result["signals"].append("daily_move_at_least_10pct")
    extremes = {"window": "252 prior sessions", "prior_high": None, "prior_low": None,
                "prior_close_high": None, "prior_close_low": None,
                "new_intraday_high": None, "new_intraday_low": None,
                "new_closing_high": None, "new_closing_low": None}
    if len(bars) >= 253:
        history = normalized[-253:-1]
        extremes.update({"prior_high": max(b["high"] for b in history),
                         "prior_low": min(b["low"] for b in history),
                         "prior_close_high": max(b["close"] for b in history),
                         "prior_close_low": min(b["close"] for b in history)})
        extremes.update({"new_intraday_high": last["high"] > extremes["prior_high"],
                         "new_intraday_low": last["low"] < extremes["prior_low"],
                         "new_closing_high": last["close"] > extremes["prior_close_high"],
                         "new_closing_low": last["close"] < extremes["prior_close_low"]})
        for key in ("new_intraday_high", "new_intraday_low", "new_closing_high", "new_closing_low"):
            if extremes[key]:
                result["signals"].append(key + "_252_session_proxy")
    else:
        result["unavailable"].append("252_prior_session_extremes_require_253_bars")
    result["extremes"] = extremes
    result["limitations"] = ["Caller must verify real exchange sessions, missing bars, adjustments and source authenticity.",
                             "252 prior sessions are a defined proxy, not an exact calendar 52-week window.",
                             "Signals are descriptive; no backtested profitability or order execution is implied."]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        print(json.dumps(analyze(json.loads(args.input.read_text(encoding="utf-8"))),
                         ensure_ascii=False, indent=2, allow_nan=False))
        return 0
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
