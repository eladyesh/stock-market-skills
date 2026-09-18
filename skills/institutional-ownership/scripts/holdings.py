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

def holdings(data):
    prior_date = date(data['prior_as_of'], 'prior_as_of')
    current_date = date(data['current_as_of'], 'current_as_of')
    filed_date = date(data['current_filed_at'], 'current_filed_at')
    if not prior_date < current_date <= filed_date:
        raise ValueError('require prior_as_of < current_as_of <= current_filed_at')
    complete_prior = boolean(data, 'complete_prior')
    complete_current = boolean(data, 'complete_current')
    def index(rows):
        output = {}
        for row in rows:
            key = tuple(row.get(k) for k in ('security_id', 'class', 'instrument'))
            if not all(isinstance(k, str) and k for k in key) or not row.get('source'):
                raise ValueError('holdings need security_id, class, instrument and source')
            if key in output:
                raise ValueError('duplicate holding: reconcile amendments and aggregate first')
            output[key] = {'shares': number(row, 'shares', minimum=0),
                           'value': number(row, 'value', minimum=0), 'source': row['source']}
        return output
    prior, current = index(data['prior']), index(data['current'])
    prior_value = sum(r['value'] for r in prior.values())
    current_value = sum(r['value'] for r in current.values())
    factors = data.get('prior_to_current_share_factors', {})
    rows = []
    for key in sorted(prior.keys() | current.keys()):
        p, c = prior.get(key), current.get(key)
        factor = number({'factor': factors.get(key[0], 1)}, 'factor', positive=True)
        ps = p['shares'] * factor if p else (0 if complete_prior else None)
        cs = c['shares'] if c else (0 if complete_current else None)
        change = cs - ps if ps is not None and cs is not None else None
        if ps is None:
            status = 'unknown_prior'
        elif cs is None:
            status = 'unknown_current'
        elif ps == 0 and cs > 0:
            status = 'newly_disclosed'
        elif cs == 0 and ps > 0:
            status = 'no_longer_disclosed'
        elif change > 0:
            status = 'increased_disclosed_quantity'
        elif change < 0:
            status = 'decreased_disclosed_quantity'
        else:
            status = 'unchanged_disclosed_quantity'
        rows.append({'security_id': key[0], 'class': key[1], 'instrument': key[2],
                     'prior_adjusted_shares': ps, 'current_shares': cs,
                     'share_change': change, 'share_change_fraction': ratio(change, ps),
                     'prior_disclosed_weight': ratio(p['value'], prior_value) if p else None,
                     'current_disclosed_weight': ratio(c['value'], current_value) if c else None,
                     'status': status, 'prior_source': p['source'] if p else None,
                     'current_source': c['source'] if c else None})
    return {'manager': data.get('manager'), 'prior_as_of': data['prior_as_of'],
            'current_as_of': data['current_as_of'], 'current_filed_at': data['current_filed_at'],
            'rows': rows, 'warnings': [
                'Changes in disclosed holdings, not verified trade dates/prices or current holdings.',
                'Weights use supplied disclosed tables, not fund NAV. Incomplete tables give partial weights.',
                'Confidential positions, manager overlap and corporate actions require source review.',
                'Values must already be in consistent units. Options are separate instruments.']}

COMMANDS = {"holdings": holdings}

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
