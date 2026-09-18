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

def insiders(data):
    seen, accepted, excluded = set(), [], []
    for row in data['transactions']:
        ident = row.get('economic_transaction_id')
        if not isinstance(ident, str) or not ident:
            raise ValueError('economic_transaction_id required for deduplication')
        reason = None
        if ident in seen:
            reason = 'duplicate_economic_transaction'
        seen.add(ident)
        if reason is None and row.get('code') != 'P':
            reason = 'not_purchase_code_P'
        if reason is None and row.get('instrument') not in {'COMMON', 'SHARE'}:
            reason = 'not_common_share_purchase'
        if reason is not None:
            excluded.append({'economic_transaction_id': ident, 'reason': reason})
            continue
        shares = number(row, 'shares', minimum=0)
        price = number(row, 'price', minimum=0)
        if shares == 0 or price == 0:
            excluded.append({'economic_transaction_id': ident, 'reason': 'no_positive_cash_purchase'})
            continue
        missing = [k for k in ('issuer', 'owner', 'transaction_date', 'filing_date', 'source') if not row.get(k)]
        if row.get('transaction_date') and row.get('filing_date'):
            if date(row['filing_date'], 'filing_date') < date(row['transaction_date'], 'transaction_date'):
                raise ValueError('filing date precedes transaction date')
        notes = boolean(row, 'notes_reviewed')
        venue = row.get('venue') if notes and row.get('venue') in {'open_market', 'private'} else 'unknown'
        accepted.append({**row, 'cash_value': shares * price, 'venue': venue,
                         'ready_for_primary_source_assertion': not missing and notes,
                         'missing_fields': missing,
                         'note': 'Code P includes private purchases; independent owners and actual notes still require review.'})
    return {'purchase_candidates': accepted, 'excluded': excluded,
            'note': 'Candidate arithmetic and supplied metadata only; no independent filing verification.'}

COMMANDS = {"insiders": insiders}

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
