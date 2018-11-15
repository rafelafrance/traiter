"""Find sex annotations."""

from lib.regexp_list import RegexpList
from lib.trait_parser import TraitParser


class ParseSex(TraitParser):
    """Find total sex annotations."""

    def __init__(self, args, preferred_value='sex'):
        """Add defaults for the measurements."""
        super().__init__()
        self.args = args
        self.regexp_list = self._battery()
        self.preferred_value = preferred_value
        self.parser = self.keyword_search

    @staticmethod
    def success(result):
        """Return this when the measurement is found."""
        value = result['value']
        if isinstance(value, list):
            value = ','.join(value)
        return {
            'has_sex': True,
            'regex': result['regex'],
            'field': result['field'],
            'start': result['start'],
            'end': result['end'],
            'key': result['key'],
            'derived_sex': value}

    @staticmethod
    def fail():
        """Return this when the measurement is not found."""
        return {
            'has_sex': False,
            'regex': None,
            'field': None,
            'start': None,
            'end': None,
            'key': None,
            'derived_sex': ''}

    def _battery(self):
        regexp_list = RegexpList(
            self.args,
            exclude_pattern=r""" ^ (?: and | was | is ) $ """)

        # Look for a key and value that is terminated with a delimiter
        regexp_list.append(
            'sex_key_value_delimited',
            r"""
                \b (?P<key> sex)
                \W+
                (?P<value> [\w?.]+ (?: \s+ [\w?.]+ ){0,2} )
                \s* (?: [:;,"] | $ )
                """)

        # Look for a key and value without a clear delimiter
        regexp_list.append(
            'sex_key_value_undelimited',
            r"""
                \b (?P<key> sex) \W+ (?P<value> \w+ )
                """)

        # Look for the words 'male' or 'female'
        regexp_list.append(
            'sex_unkeyed',
            r"""
                \b (?P<value> (?: males? | females? ) (?: \s* \? )? ) \b
                """,
            want_list=2)

        return regexp_list
