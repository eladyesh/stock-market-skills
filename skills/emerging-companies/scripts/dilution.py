#!/usr/bin/env python3
"""Offline arithmetic on supplied inputs; no fetching or independent source verification."""
import argparse
import datetime as dt
import json
import math
import sys
from pathlib import Path

def number(obj, key, *, optional=False, minimum=None, positive=False):
    value = obj.get(key)
    if value is None and optional:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f'{key}: expected a finite number')
    value = float(value)
    if not math.isfinite(value):
        raise ValueError(f'{key}: expected a finite number')
    if positive and value <= 0:
        raise ValueError(f'{key}: must be positive')
    if minimum is not None and value < minimum:
        raise ValueError(f'{key}: must be >= {minimum}')
    return value

def date(value, label):
    try:
        return dt.date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError(f'{label}: expected YYYY-MM-DD') from None

def boolean(obj, key, default=False):
    value = obj.get(key, default)
    if not isinstance(value, bool):
        raise ValueError(f'{key}: expected boolean')
    return value

def ratio(a, b):
    return a / b if a is not None and b is not None and b > 0 else None

def dilution(data):
    old = number(data, 'pre_shares', positive=True)
    preprice = number(data, 'pre_price', positive=True)
    new = number(data, 'new_shares', positive=True)
    offer = number(data, 'offer_price', positive=True)
    fees = number(data, 'fees', minimum=0)
    gross = new * offer
    if fees > gross:
        raise ValueError('fees exceed gross proceeds')
    net = gross - fees
    total = old + new
    theoretical = (old * preprice + net) / total
    postprice = number(data, 'post_price', optional=True, positive=True)
    cash = number(data, 'pre_cash', optional=True, minimum=0)
    debt = number(data, 'pre_debt', optional=True, minimum=0)
    if (cash is None) != (debt is None):
        raise ValueError('provide pre_cash and pre_debt together')
    repayment = number({'debt_repaid': data.get('debt_repaid', 0)}, 'debt_repaid', minimum=0)
    if repayment and (debt is None or repayment > debt or repayment > cash + net):
        raise ValueError('debt repayment exceeds debt or available cash')
    out = {'post_shares': total, 'gross_proceeds': gross, 'net_proceeds': net,
           'share_count_expansion': new / old, 'old_holder_ownership_dilution': new / total,
           'theoretical_ex_issue_price': theoretical,
           'theoretical_price_change': theoretical / preprice - 1,
           'post_price_vs_theoretical': postprice / theoretical - 1 if postprice else None,
           'sources': data.get('sources', []),
           'note': 'Plain completed primary common issuance only. Constant pre-event business value is an assumption, not fair value.'}
    if cash is not None:
        out.update({'post_cash': cash + net - repayment, 'post_debt': debt - repayment,
                    'pre_enterprise_value': old * preprice + debt - cash,
                    'post_enterprise_value': total * postprice + debt - cash - net if postprice else None})
    return out

COMMANDS = {"dilution": dilution}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=COMMANDS)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    try:
        data = json.loads(args.input.read_text(encoding='utf-8'))
        result = COMMANDS[args.command](data)
        text = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding='utf-8')
        else:
            print(text, end='')
    except (ValueError, KeyError, TypeError, OSError, OverflowError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    return 0

if __name__ == "__main__":
    sys.exit(main())
