"""Find sex annotations."""

from lib.parser_battery import ParserBattery
from lib.trait_parser import TraitParser


class ParseSex(TraitParser):
    """Find total sex annotations."""

    def __init__(self, args, preferred_value='sex'):
        """Add defaults for the measurements."""
        super().__init__()
        self.args = args
        self.battery = self._battery()
        self.preferred_value = preferred_value
        self.parser = self.keyword_search

    @staticmethod
    def success(result):
        """Return this when the measurement is found."""
        value = result['value']
        if isinstance(value, list):
            value = ','.join(value)
        return {
            'key': result['key'],
            'has_sex': True,
            'derived_sex': value,
            'regex': result['regex']}

    @staticmethod
    def fail():
        """Return this when the measurement is not found."""
        return {
            'key': None,
            'has_sex': False,
            'derived_sex': '',
            'regex': None}

    @staticmethod
    def _battery():
        battery = ParserBattery(
            exclude_pattern=r""" ^ (?: and | was | is ) $ """)

        # Look for a key and value that is terminated with a delimiter
        battery.append(
            'sex_key_value_delimited',
            r"""
                \b (?P<key> sex)
                \W+
                (?P<value> [\w?.]+ (?: \s+ [\w?.]+ ){0,2} )
                \s* (?: [:;,"] | $ )
                """)

        # Look for a key and value without a clear delimiter
        battery.append(
            'sex_key_value_undelimited',
            r"""
                \b (?P<key> sex) \W+ (?P<value> \w+ )
                """)

        # Look for the words 'male' or 'female'
        battery.append(
            'sex_unkeyed',
            r"""
                \b (?P<value> (?: males? | females? ) (?: \s* \? )? ) \b
                """,
            want_list=2)

        return battery
