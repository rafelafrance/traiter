from trait_parsers.parser_battery import ParserBattery
from trait_parsers.trait_parser import TraitParser


class SexParser(TraitParser):

    def __init__(self):
        self.normalize = False
        self._battery()

    def success(self, value):
        if isinstance(value, list):
            value = ','.join(value)
        return {'hasSex': 1, 'derivedSex': value}

    def fail(self):
        return {'hasSex': 0, 'derivedSex': ''}

    def _battery(self):
        self.battery = ParserBattery(exclude_pattern=r''' ^ (?: and | was | is ) $ ''')

        # Look for a key and value that is terminated with a delimiter
        self.battery.append(
            'sex_key_value_delimited',
            r'''
                \b (?P<key> sex)
                \W+
                (?P<value> [\w?.]+ (?: \s+ [\w?.]+ ){0,2} )
                \s* (?: [:;,"] | $ )
            '''
        )

        # Look for a key and value without a clear delimiter
        self.battery.append(
            'sex_key_value_undelimited',
            r'''
                \b (?P<key> sex) \W+ (?P<value> \w+ )
            '''
        )

        # Look for the words male & female
        self.battery.append(
            'sex_unkeyed',
            r'''
                \b (?P<value> (?: males? | females? ) (?: \s* \? )? ) \b
            ''',
            want_array=2
        )
