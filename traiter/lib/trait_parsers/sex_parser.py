"""Find sex annotations."""

from lib.parser_battery import ParserBattery
from lib.trait_parser import TraitParser


class SexParser(TraitParser):
    """Find total sex annotations."""

    def __init__(self):
        """Add defaults for the measurements."""
        self.normalize = False
        self.battery = self._battery()

    def success(self, result):
        """Return this when the measurement is found."""
        value = result['value']
        if isinstance(value, list):
            value = ','.join(value)
        return {'hassex': 1, 'derivedsex': value}

    def fail(self):
        """Return this when the measurement is not found."""
        return {'hassex': 0, 'derivedsex': ''}

    def _battery(self):
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
