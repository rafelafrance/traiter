"""Find testes size annotations."""

from lib.regexp_list import RegexpList
from lib.trait_parser import TraitParser
import lib.units as units
import lib.trait_parsers.common_regexp as common_regexp


class ParseTestesSize(TraitParser):
    """Find testes size annotations."""

    unit_conversions = units.LENGTH_CONVERSIONS

    def __init__(self, args, preferred_value=None):
        """Add defaults for the measurements."""
        super().__init__()
        self.args = args
        self.regexp_list = self._battery(self.common_patterns)
        self.default_units = '_mm_'
        self.preferred_value = preferred_value
        self.parser = self.search_and_normalize

    def success(self, result):
        """Return this when the measurement is found."""
        if result['value'] == 0:
            # Don't allow a 0 size
            return self.fail()

        length = result['value']
        width = None
        if isinstance(result['value'], list):
            length, width = result['value']
            if width > length:
                length, width = width, length

        return {
            'found': True,
            'regex': result['regex'],
            'field': result['field'],
            'start': result['start'],
            'end': result['end'],
            'key': result['key'],
            'length_in_mm': length,
            'width_in_mm': width,
            'units_inferred': result['is_inferred']}

    @staticmethod
    def fail():
        """Return this when the measurement is not found."""
        return {
            'found': False,
            'regex': None,
            'field': None,
            'start': None,
            'end': None,
            'key': None,
            'length_in_mm': None,
            'width_in_mm': None,
            'units_inferred': False}

    def _battery(self, common_patterns):
        regexp_list = RegexpList(
            self.args,
            parse_units=True,
            units_from_key=r""" (?P<units> grams ) $ """)

        # Look for a pattern like: testes = 8x5 mm
        regexp_list.append(
            'key_measurements',
            common_patterns + r"""
                (?P<key> (?&testes) ) \s* (?&key_end)? \s*
                (?P<value> (?&cross) ) \s*
                (?P<units> (?&len_units) )?
                """,
            default_units='_mm_')

        return regexp_list

    common_patterns = common_regexp.SHORT_PATTERNS \
        + common_regexp.LENGTH_PATTERNS \
        + common_regexp.NUMERIC_PATTERNS \
        + common_regexp.REPRODUCTIVE_PATTERNS \
        + r"""
        """
