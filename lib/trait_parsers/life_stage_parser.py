from trait_parsers.parser_battery import ParserBattery
from trait_parsers.trait_parser import TraitParser


class LifeStageParser(TraitParser):

    def __init__(self):
        self.normalize = False
        self._battery(self._common_patterns())

    def success(self, value):
        return {'hasLifeStage': 1, 'derivedLifeStage': value}

    def fail(self):
        return {'hasLifeStage': 0, 'derivedLifeStage': ''}

    def _battery(self, common_patterns):
        self.battery = ParserBattery(exclude_pattern=r''' ^ determin ''')

        # Look for a key and value that is terminated with a delimiter
        self.battery.append(
            'life_stage_key_value_delimited',
            common_patterns + r'''
                \b (?P<key> (?: life \s* stage (?: \s* remarks )? | age (?: \s* class )? ) )
                \W+
                (?P<value> (?&word_chars) (?: \s+(?&word_chars) ){0,4} ) \s*
                (?: [:;,"] | $ )
            '''
        )

        # Look for a key and value without a clear delimiter
        self.battery.append(
            'life_stage_key_value_undelimited',
            common_patterns + r'''
                \b (?P<key> life \s* stage (?: \s* remarks )?
                        | age \s* class
                        | age \s* in \s* (?: hour | day ) s?
                        | age
                    )
                    \W+
                    (?P<value> [\w?.\/\-]+ (?: \s+ (?: year | recorded ) )? )
            '''
        )

        # Look for common life stage phrases
        self.battery.append(
            'life_stage_no_keyword',
            common_patterns + r'''
                (?P<value> (?: after \s+ )?
                        (?: first | second | third | fourth | hatching ) \s+
                        year )
            '''
        )

    def _common_patterns(self):
        return r'''
            (?(DEFINE)
                (?P<word_chars> [\w?.\/\-]+ )
            )
        '''
