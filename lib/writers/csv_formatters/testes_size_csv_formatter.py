"""Format the trait for CSV output."""

from operator import itemgetter
from lib.util import ordinal


def csv_formatter(_, row, traits):
    """Format the trait for CSV output."""
    if not traits:
        return
    records = _build_records(traits)
    records = _merge_records(records)
    _format_records(records, row)


def _build_records(traits):
    records = []
    for trait in traits:
        if isinstance(trait.value, list):
            length, width = trait.value
            if width > length:
                length, width = width, length
        elif trait.dimension == 'width':
            length, width = -1, trait.value
        else:
            length, width = trait.value, -1
        records.append({'side': trait.side,
                        'length': length,
                        'width': width,
                        'ambiguous_key': trait.ambiguous_key,
                        'units_inferred': trait.units_inferred})
    return sorted(records, key=itemgetter('side', 'length', 'width'))


def _merge_records(records):
    merged = [records[0]]
    for curr in records:
        prev = merged[-1]
        if prev['side'] == curr['side']:
            if prev['length'] == curr['length'] \
                    and prev['width'] == curr['width']:
                _merge_flags(prev, curr)
                continue
            elif prev['length'] == -1 and curr['length'] != -1:
                prev['length'] = curr['length']
                _merge_flags(prev, curr)
                continue
            elif prev['width'] == -1 and curr['width'] != -1:
                _merge_flags(prev, curr)
                prev['width'] = curr['width']
                continue
        merged.append(curr)
    return merged


def _merge_flags(prev, curr):
    """If one of the flags is unambiguous then they all are."""
    prev['ambiguous_key'] |= curr['ambiguous_key']
    prev['units_inferred'] |= curr['units_inferred']


def _format_records(records, row):
    for i, rec in enumerate(records, 1):
        key = f'testes_{i}01:{ordinal(i)}_testes_side'
        row[key] = rec['side']
        key = f'testes_{i}20:{ordinal(i)}_testes_length'
        row[key] = rec['length'] if rec['length'] > 0 else ''
        key = f'testes_{i}21:{ordinal(i)} testes width'
        row[key] = rec['width'] if rec['width'] > 0 else ''
        if rec['ambiguous_key']:
            key = f'testes_{i}30:{ordinal(i)}_testes_ambiguous_key'
            row[key] = rec['ambiguous_key']
        if rec['units_inferred']:
            key = f'testes_{i}31:{ordinal(i)}_testes_units_inferred'
            row[key] = rec['units_inferred']
