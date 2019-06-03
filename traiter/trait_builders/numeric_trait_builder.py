"""Mix-in for parsing length notations."""

import re
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder, ordinal
from traiter.numeric_trait import NumericTrait

LOOK_BACK_FAR = 40

QUOTES_VS_INCHES = re.compile(r' \d " (?! \s* \} )', re.VERBOSE)
IS_COLLECTOR = re.compile(r' collector ', re.VERBOSE)


class NumericTraitBuilder(BaseTraitBuilder):
    """Shared parser logic."""

    @staticmethod
    def add_flags(token, trait):
        """Add common flags to the numeric trait."""
        trait.is_flag_in_token('ambiguous_key', token)
        trait.is_flag_in_token('estimated_value', token)
        trait.is_value_in_token('measured_from', token)
        trait.is_value_in_token('includes', token)

    def simple(self, token):
        """Handle a normal length notation."""
        trait = NumericTrait(start=token.start, end=token.end)
        self.add_flags(token, trait)
        trait.float_value(token.groups['value1'], token.groups.get('value2'))
        trait.convert_value(token.groups.get('units'))
        return trait

    def compound(self, token, units=''):
        """Handle a pattern like: 4 lbs 9 ozs."""
        trait = NumericTrait(start=token.start, end=token.end)
        self.add_flags(token, trait)
        values = [token.groups[units[0]], token.groups[units[1]]]
        trait.compound_value(values, units)
        return trait

    def fraction(self, token):
        """Handle fractional values like 10 3/8 inches."""
        trait = NumericTrait(start=token.start, end=token.end)
        self.add_flags(token, trait)
        trait.fraction_value(token)
        trait.convert_value(token.groups.get('units'))
        return trait

    @staticmethod
    def shorthand_length(token, measurement=''):
        """Handle shorthand length notation like 11-22-33-44:55g."""
        trait = NumericTrait(start=token.start, end=token.end)
        trait.float_value(token.groups.get(measurement))
        if not trait.value:
            return None
        trait.units = 'mm_shorthand'
        trait.is_shorthand = True
        flag = measurement.split('_')[1]
        flag = f'estimated_{flag}'
        trait.is_flag_in_token(flag, token, rename='estimated_value')
        return trait

    def numeric_fix_ups(self, trait, text):
        """All of the numeric fix-ups."""
        return self.fix_up_shorthand(trait, text) \
            and self.fix_up_inches(trait, text)

    @staticmethod
    def fix_up_shorthand(trait, text):
        """All of the fix-ups for numbers."""
        if not trait.is_shorthand:
            return trait
        start = max(0, trait.start - LOOK_BACK_FAR)
        if IS_COLLECTOR.search(text, start, trait.start):
            return None
        return trait

    @staticmethod
    def fix_up_inches(trait, text):
        """Disambiguate between double quotes "3" and inch units 3"."""
        if (not trait.units
                and QUOTES_VS_INCHES.match(text[trait.end-1:])
                and text[trait.start:trait.end].count('"') == 0):
            trait.end += 1
            trait.units = '"'
            trait.convert_value(trait.units)
        return trait

    @staticmethod
    def csv_formatter(trait, row, parses):
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
            col = f'{trait}_{i}01:{ordinal(i)}_{trait}{low_key}'
            row[col] = key.low
            if key.high:
                col = f'{trait}_{i}02:{ordinal(i)}_{trait}_high'
                row[col] = key.high
            if parse.dimension:
                col = f'{trait}_{i}03:{ordinal(i)}_{trait}_dimension'
                row[col] = parse.dimension
            if parse.includes:
                col = f'{trait}_{i}04:{ordinal(i)}_{trait}_includes'
                row[col] = parse.includes
            if parse.measured_from:
                col = f'{trait}_{i}05:{ordinal(i)}_{trait}_measured_from'
                row[col] = parse.measured_from
            if parse.ambiguous_key:
                col = f'{trait}_{i}06:{ordinal(i)}_{trait}_ambiguous'
                row[col] = parse.ambiguous_key
            if parse.units_inferred:
                col = f'{trait}_{i}07:{ordinal(i)}_{trait}_units_inferred'
                row[col] = parse.units_inferred
            if parse.estimated_value:
                col = f'{trait}_{i}08:{ordinal(i)}_{trait}_estimated'
                row[col] = parse.estimated_value
