#!/usr/bin/env python3
"""Offline arithmetic for sourced stock research; never fetches or verifies data."""
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


def cagr(start, end, years):
    if start is None or end is None or years is None or min(start, end, years) <= 0:
        return None
    return (end / start) ** (1 / years) - 1


def ratio(a, b):
    return a / b if a is not None and b is not None and b > 0 else None


def vector(obj, key, n=None, floor=None):
    values = obj.get(key)
    if not isinstance(values, list) or not values or (n is not None and len(values) != n):
        raise ValueError(f'{key}: expected a nonempty array of matching length')
    result = [number({'x': v}, 'x') for v in values]
    if floor is not None and any(v <= floor for v in result):
        raise ValueError(f'{key}: every value must exceed {floor}')
    return result


def screen(data):
    as_of = date(data['as_of'], 'as_of')
    outputs = []
    for row in data['rows']:
        if not row.get('ticker'):
            raise ValueError('every screen row needs ticker')
        get = lambda k: number(row, k, optional=True)
        vals = {k: get(k) for k in (
            'revenue_start', 'revenue_end', 'history_years', 'eps_start', 'eps_end',
            'shares_start', 'shares_end', 'price', 'market_cap', 'fcf', 'net_debt',
            'ebitda', 'price_return', 'benchmark_return', 'revenue_yoy',
            'operating_profit_yoy', 'eps_forward')}
        flags, warnings = [], []
        rc = cagr(vals['revenue_start'], vals['revenue_end'], vals['history_years'])
        ec = cagr(vals['eps_start'], vals['eps_end'], vals['history_years'])
        sc = cagr(vals['shares_start'], vals['shares_end'], vals['history_years'])
        if rc is not None and rc >= .10:
            flags.append('double_digit_revenue_history')
        if ec is not None and ec >= .10:
            flags.append('double_digit_eps_history')
        if vals['eps_start'] is not None and vals['eps_end'] is not None and ec is None:
            warnings.append('EPS CAGR not meaningful for nonpositive endpoints or missing horizon')
        if (vals['price_return'] is not None and vals['price_return'] <= -.10
                and vals['revenue_yoy'] is not None and vals['revenue_yoy'] >= .10
                and vals['operating_profit_yoy'] is not None and vals['operating_profit_yoy'] > 0):
            flags.append('earnings_gap_lead_requires_event_guidance_and_valuation_checks')
        price_ok = bool(row.get('price_as_of'))
        if price_ok:
            if date(row['price_as_of'], 'price_as_of') > as_of:
                raise ValueError('price_as_of is later than scan as_of')
        else:
            warnings.append('Missing price_as_of: suppress price-based multiples/yield')
        if vals['price'] is not None and vals['price'] <= 0:
            raise ValueError('price must be positive')
        sector = str(row.get('sector', '')).lower()
        financial = any(term in sector for term in ('bank', 'insurance', 'financial', 'reit', 'real estate'))
        forward_basis = row.get('forecast_basis')
        basis_ok = forward_basis in {'company_guidance', 'dated_consensus', 'model_scenario'}
        if vals['eps_forward'] is not None and not basis_ok:
            warnings.append('Missing/invalid forecast_basis: suppress forward P/E')
        if not row.get('sources'):
            warnings.append('Missing sources: arithmetic only, not verified research')
        excess = None
        if vals['price_return'] is not None and vals['benchmark_return'] is not None:
            excess = vals['price_return'] - vals['benchmark_return']
            warnings.append('Relative return assumes caller verified identical return windows/basis')
        outputs.append({
            'ticker': row['ticker'], 'sources': row.get('sources', []),
            'price_as_of': row.get('price_as_of'), 'revenue_cagr': rc, 'eps_cagr': ec,
            'shares_cagr': sc,
            'trailing_pe': ratio(vals['price'], vals['eps_end']) if price_ok else None,
            'forward_pe': ratio(vals['price'], vals['eps_forward']) if price_ok and basis_ok else None,
            'forecast_basis': forward_basis,
            'fcf_yield': ratio(vals['fcf'], vals['market_cap']) if price_ok else None,
            'net_debt_ebitda': None if financial else ratio(vals['net_debt'], vals['ebitda']),
            'relative_price_return': excess, 'discovery_flags': flags, 'warnings': warnings,
        })
    return {'as_of': data['as_of'], 'rows_computed': len(outputs), 'rows': outputs,
            'note': 'No source verification, overall score, buy signal or full-universe coverage implied.'}


def forecast(data):
    revenue0 = number(data, 'revenue', positive=True)
    income0 = number(data, 'net_income')
    shares0 = number(data, 'shares', positive=True)
    price0 = number(data, 'price', positive=True)
    equity0 = number(data, 'book_equity', optional=True)
    year = number(data, 'base_year', positive=True)
    if not year.is_integer():
        raise ValueError('base_year must be an integer fiscal year')
    scenarios = data.get('scenarios')
    if not isinstance(scenarios, dict) or not scenarios:
        raise ValueError('scenarios: expected named scenarios')
    result = {}
    for label, case in scenarios.items():
        growth = vector(case, 'revenue_growth', floor=-1)
        n = len(growth)
        margins = vector(case, 'net_margin', n)
        sharegrowth = vector(case, 'share_growth', n, floor=-1)
        pe = number(case, 'exit_pe', optional=True, positive=True)
        equity_keys = ('dividends', 'buybacks', 'net_equity_issuance', 'oci')
        has_bridge = equity0 is not None and all(case.get(k) is not None for k in equity_keys)
        bridge = {k: vector(case, k, n) for k in equity_keys} if has_bridge else None
        if bridge and any(v < 0 for k in ('dividends', 'buybacks') for v in bridge[k]):
            raise ValueError('dividends and buybacks must be nonnegative')
        rev, shares, equity = revenue0, shares0, equity0 if has_bridge else None
        rows = []
        for i in range(n):
            rev *= 1 + growth[i]
            shares *= 1 + sharegrowth[i]
            income = rev * margins[i]
            if equity is not None:
                equity += (income - bridge['dividends'][i] - bridge['buybacks'][i]
                           + bridge['net_equity_issuance'][i] + bridge['oci'][i])
            rows.append({'fiscal_year': int(year) + i + 1, 'revenue': rev,
                         'net_income': income, 'diluted_shares_proxy': shares,
                         'eps': income / shares, 'book_equity': equity,
                         'book_value_per_share': equity / shares if equity is not None else None})
        terminal = rows[-1]
        target = terminal['eps'] * pe if pe is not None and terminal['eps'] > 0 else None
        warnings = ['Model scenario, not analyst consensus or a prediction.',
                    'Diluted-share proxy used for EPS and valuation; a full model separates share timing.',
                    'Return is price-only; dividends are excluded.']
        if equity0 is not None and not has_bridge:
            warnings.append('Book-equity forecast omitted: complete equity bridge not supplied.')
        if terminal['eps'] <= 0:
            warnings.append('Terminal loss: P/E valuation not meaningful.')
        result[label] = {'years': rows, 'revenue_cagr': cagr(revenue0, rev, n),
                         'net_income_cagr': cagr(income0, terminal['net_income'], n),
                         'eps_cagr': cagr(income0 / shares0, terminal['eps'], n),
                         'exit_pe': pe, 'terminal_price': target,
                         'terminal_market_equity_value': target * shares if target is not None else None,
                         'price_return': target / price0 - 1 if target is not None else None,
                         'annualized_price_return': cagr(price0, target, n), 'warnings': warnings}
    return {'sources': data.get('sources', []), 'scenarios': result}


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


COMMANDS = {'screen': screen, 'forecast': forecast, 'dilution': dilution,
            'holdings': holdings, 'insiders': insiders}


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


if __name__ == '__main__':
    sys.exit(main())
