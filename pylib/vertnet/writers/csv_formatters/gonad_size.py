"""Format the trait for CSV output."""

from operator import itemgetter
from pylib.vertnet.util import ordinal


def build_records(traits):
    """Build records for output."""
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


def merge_records(records):
    """Merge records for output."""
    merged = [records[0]]
    for curr in records:
        prev = merged[-1]
        if prev['side'] == curr['side']:
            if prev['length'] == curr['length'] \
                    and prev['width'] == curr['width']:
                _merge_flags(prev, curr)
                continue
            if prev['length'] == -1 and curr['length'] != -1:
                prev['length'] = curr['length']
                _merge_flags(prev, curr)
                continue
            if prev['width'] == -1 and curr['width'] != -1:
                _merge_flags(prev, curr)
                prev['width'] = curr['width']
                continue
        merged.append(curr)
    return merged


def _merge_flags(prev, curr):
    """If one of the flags is unambiguous then they all are."""
    prev['ambiguous_key'] = bool(prev.get('ambiguous_key'))
    prev['ambiguous_key'] |= bool(curr['ambiguous_key'])

    prev['units_inferred'] = bool(prev.get('units_inferred'))
    prev['units_inferred'] |= bool(curr['units_inferred'])


def format_records(records, row, gonads):
    """Format the records."""
    for i, rec in enumerate(records, 1):
        key = f'{gonads}_{i}01:{ordinal(i)}_{gonads}_side'
        row[key] = rec['side']
        key = f'{gonads}_{i}20:{ordinal(i)}_{gonads}_length'
        row[key] = rec['length'] if rec['length'] > 0 else ''
        key = f'{gonads}_{i}21:{ordinal(i)}_{gonads}_width'
        row[key] = rec['width'] if rec['width'] > 0 else ''
        if rec['ambiguous_key']:
            key = f'{gonads}_{i}30:{ordinal(i)}_{gonads}_ambiguous_key'
            row[key] = rec['ambiguous_key']
        if rec['units_inferred']:
            key = f'{gonads}_{i}31:{ordinal(i)}_{gonads}_units_inferred'
            row[key] = rec['units_inferred']
