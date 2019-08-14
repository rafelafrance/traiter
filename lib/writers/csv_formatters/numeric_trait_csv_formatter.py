"""Format the trait for CSV output."""

from lib.util import ordinal


def csv_formatter(trait_name, row, parses):
    """Format the trait for CSV output."""
    if not parses:
        return

    records = {}
    has_range = False
    for parse in parses:
        key = parse.as_key()
        has_range |= bool(key.high)
        if key in records:
            records[key].merge_flags(parse)
        else:
            records[key] = parse

    low_key = '_low' if has_range else ''
    for i, (key, parse) in enumerate(records.items(), 1):
        col = f'{trait_name}_{i}01:{ordinal(i)}_{trait_name}{low_key}'
        row[col] = key.low
        if key.high:
            col = f'{trait_name}_{i}02:{ordinal(i)}_{trait_name}_high'
            row[col] = key.high
        if parse.dimension:
            col = f'{trait_name}_{i}03:{ordinal(i)}_{trait_name}_dimension'
            row[col] = parse.dimension
        if parse.includes:
            col = f'{trait_name}_{i}04:{ordinal(i)}_{trait_name}_includes'
            row[col] = parse.includes
        if parse.measured_from:
            col = (f'{trait_name}_{i}05:{ordinal(i)}_{trait_name}'
                   '_measured_from')
            row[col] = parse.measured_from
        if parse.ambiguous_key:
            col = f'{trait_name}_{i}06:{ordinal(i)}_{trait_name}_ambiguous'
            row[col] = parse.ambiguous_key
        if parse.units_inferred:
            col = (f'{trait_name}_{i}07:{ordinal(i)}_{trait_name}'
                   '_units_inferred')
            row[col] = parse.units_inferred
        if parse.estimated_value:
            col = f'{trait_name}_{i}08:{ordinal(i)}_{trait_name}_estimated'
            row[col] = parse.estimated_value
