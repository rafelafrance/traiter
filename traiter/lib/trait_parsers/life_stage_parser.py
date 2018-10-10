"""Find life life stage annotations."""

from lib.parser_battery import ParserBattery
from lib.trait_parser import TraitParser


class LifeStageParser(TraitParser):
    """Find life life stage annotations."""

    def __init__(self):
        """Add defaults for the measurements."""
        self.normalize = False
        self.battery = self._battery(self._common_patterns())

    def success(self, result):
        """Return this when the measurement is found."""
        return {'haslifestage': 1, 'derivedlifestage': result['value']}

    def fail(self):
        """Return this when the measurement is not found."""
        return {'haslifestage': 0, 'derivedlifestage': ''}

    def _battery(self, common_patterns):
        battery = ParserBattery(exclude_pattern=r""" ^ determin """)

        # Look for a key and value that is terminated with a delimiter
        battery.append(
            'life_stage_key_value_delimited',
            common_patterns + r"""
                \b (?P<key>
                    (?: life \s* stage (?: \s* remarks )?
                    | age (?: \s* class )? ) )
                \W+
                (?P<value> (?&word_chars) (?: \s+(?&word_chars) ){0,4} ) \s*
                (?: [:;,"] | $ )
                """)

        # Look for a key and value without a clear delimiter
        battery.append(
            'life_stage_key_value_undelimited',
            common_patterns + r"""
                \b (?P<key> life \s* stage
                    (?: \s* remarks )?
                    | age \s* class
                    | age \s* in \s* (?: hour | day ) s?
                    | age)
                    \W+
                    (?P<value> [\w?.\/\-]+ (?: \s+ (?: year | recorded ) )? )
                """)

        # Look for common life stage phrases
        battery.append(
            'life_stage_no_keyword',
            common_patterns + r"""
                (?P<value> (?: after \s+ )?
                        (?: first | second | third | fourth | hatching ) \s+
                        year )
                """)

        battery.append(
            'life_stage_yolk_sac',
            common_patterns + r"""
                (?P<value> (?: yolk ) \s+
                        sac )
                """)

        # Look for the words lifestage words without keys
        # Combinations with embryo and fetus were removed,
        # as more often than not these are reproductiveCondition
        # indicators of and adult female.
        battery.append(
            'life_stage_unkeyed',
            r"""
                \b (?P<value>
                (?: larves? |larvae? | larvals? | imagos? | neonates?
                | hatchlings? | hatched? | fry? | metamorphs? | premetamorphs
                | tadpoles? | têtard?
                | young-of-the-year? | leptocephales? | leptocephalus?
                | immatures? | imms? | jeunes? | young? | ygs?
                | fleglings? | fledgelings? | chicks? | nestlings?
                | juveniles? | juvéniles? | juvs?
                | subadults? | subadultes? | subads? | sub-adults? | yearlings?
                | matures? | adults? | adulte? | ads? ) (?: \s* \? )? ) \b
                """)

        return battery

    def _common_patterns(self):
        return r"""
            (?(DEFINE)
                (?P<word_chars> [\w?.\/\-]+ )
            )
            """
