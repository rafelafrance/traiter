"""Find life life stage annotations."""

from lib.parser_battery import ParserBattery
from lib.trait_parser import TraitParser


class LifeStageParser(TraitParser):
    """Find life life stage annotations."""

    def __init__(self):
        """Add defaults for the measurements."""
        super().__init__()
        self.battery = self._battery(self._common_patterns())

    @staticmethod
    def success(result):
        """Return this when the measurement is found."""
        return {
            'key': result['key'],
            'has_life_stage': True,
            'derived_life_stage': result['value'],
            'regex': result['regex']}

    @staticmethod
    def fail():
        """Return this when the measurement is not found."""
        return {
            'key': None,
            'has_life_stage': False,
            'derived_life_stage': '',
            'regex': None}

    @staticmethod
    def _battery(common_patterns):
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

        # Look for before birth life stages
        battery.append(
            'life_stage_yolk_sac',
            common_patterns + r"""
                (?P<value> (?: yolk ) \s+ sac )
                """)

        # Look for the words lifestage words without keys
        # Combinations with embryo and fetus were removed, as more often than
        # not these are reproductiveCondition indicators of the adult female.
        battery.append(
            'life_stage_unkeyed',
            r"""
                \b (?P<value>
                (?: larves? |larvae? | larvals? | imagos? | neonates?
                | hatchlings? | hatched | fry | metamorphs? | premetamorphs?
                | tadpoles? | têtard
                # | embryos? | embryonic | fetus(es)?
                | young-of-the-year | leptocephales? | leptocephalus
                | immatures? | imms? | jeunes? | young | ygs?
                | fleglings? | fledgelings? | chicks? | nestlings?
                | juveniles? | juvéniles? | juvs?
                | subadults? | subadultes? | subads? | sub-adults? | yearlings?
                | matures? | adults? | adulte? | ads? ) (?: \s* \? )? ) \b
                """)

        return battery

    @staticmethod
    def _common_patterns():
        return r"""
            (?(DEFINE)
                (?P<word_chars> [\w?.\/\-]+ )
            )
            """
