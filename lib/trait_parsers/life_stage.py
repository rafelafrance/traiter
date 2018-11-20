"""Find life life stage annotations."""

from lib.regexp_list import RegexpList
from lib.trait_parser import TraitParser


class ParseLifeStage(TraitParser):
    """Find life life stage annotations."""

    def __init__(self, args, preferred_value='lifestage'):
        """Add defaults for the measurements."""
        super().__init__()
        self.args = args
        self.regexp_list = self._battery(self.common_patterns)
        self.preferred_value = preferred_value
        self.parser = self.keyword_search

    @staticmethod
    def success(result):
        """Return this when the measurement is found."""
        return {
            'found': True,
            'regex': result['regex'],
            'field': result['field'],
            'start': result['start'],
            'end': result['end'],
            'key': result['key'],
            'value': result['value']}

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
            'value': ''}

    def _battery(self, common_patterns):
        regexp_list = RegexpList(
            self.args, exclude_pattern=r""" ^ determin """)

        # Look for a key and value that is terminated with a delimiter
        regexp_list.append(
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
        regexp_list.append(
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
        regexp_list.append(
            'life_stage_no_keyword',
            common_patterns + r"""
                (?P<value> (?: after \s+ )?
                        (?: first | second | third | fourth | hatching ) \s+
                        year )
                """)

        # Look for before birth life stages
        regexp_list.append(
            'life_stage_yolk_sac',
            common_patterns + r"""
                (?P<value> (?: yolk ) \s+ sac )
                """)

        # Look for the words lifestage words without keys
        # Combinations with embryo and fetus were removed, as more often than
        # not these are reproductiveCondition indicators of the adult female.
        regexp_list.append(
            'life_stage_unkeyed',
            r"""
                \b (?P<value>
                (?: larves? |larvae? | larvals? | imagos? | neonates?
                | hatchlings? | hatched | fry | metamorphs? | premetamorphs?
                | tadpoles? | têtard
                # | embryos? | embryonic | fetus (:? es )?
                | young-of-the-year | leptocephales? | leptocephalus
                | immatures? | imms? | jeunes? | young (?: \s* adult)? | ygs?
                | fleglings? | fledgelings? | chicks? | nestlings?
                | juveniles? | juvéniles? | juvs?
                | subadults? | subadultes? | subads? | sub-adults? | yearlings?
                | matures? | adults? | adulte? | ads? )
                (?: \s* \? )? ) \b
                """)

        return regexp_list

    common_patterns = r"""
            (?(DEFINE)
                (?P<word_chars> [\w?.\/\-]+ )
            )
            """
