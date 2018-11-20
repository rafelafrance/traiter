"""Find testes state annotations."""

from lib.regexp_list import RegexpList
from lib.trait_parser import TraitParser


class ParseTestesState(TraitParser):
    """Find testes state annotations."""

    def __init__(self, args, preferred_value=None):
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
            'value': None}

    def _battery(self, common_patterns):
        regexp_list = RegexpList(self.args)

        # Look for testes state
        regexp_list.append(
            'testes_state',
            common_patterns + r"""
                \b (?P<key>  (?&testes) ) \s*
                   (?P<value> (?&state) | (?&state_abbrev) )
                """)

        # Look for abbreviated testes key and a full state
        regexp_list.append(
            'testes_abbrev_state',
            common_patterns + r"""
                \b (?P<key>  (?&testes_abbrev) ) \s*
                   (?P<value> (?&state) )
                """)

        regexp_list.append(
            'reproductive_data',
            common_patterns + r"""
                \b (?P<key>  reproductive [\s_-]? data ) \W+
                   (?P<value> (?: (?&testes) | (?&testes_abbrev) )? \s*
                              (?: (?&state) | (?&state_abbrev) ) )
                """)

        return regexp_list

    common_patterns = TraitParser.short_patterns + r"""
        (?(DEFINE)
            # Negative state indicators
            (?P<not> not | non | no )

            # Completely
            (?P<complete>
                (?&not) (?&dash) (:? in )?
                (?: completely | complete )
            )

            # Testes
            (?P<testes> testes |  testis |  gonads? )

            # Abbreviations for testes. Other indicators required
            (?P<testes_abbrev> tes | ts | t )

            # Forms of the word descend
            (?P<descended> descend (?: ed)? (?&dot) | desc (?&dot) )

            # State words
            (?P<state>
                (?&not)? (?&dash) (?: scrot (?&dot) | scrotum | scrotal ) \b
              | (?&not)? (?&dash) (?: fully? )? (?&dash) (?&descended) \b
              | (?: un)? (?&descended)
              | abdominal | abdomin (?&dot) | abdom (?&dot)
              | cryptorchism | cryptorchid | monorchism | monorchid
              | (?: partially | partially) \s* (?&descended)
              | nscr
            )

            # State Abbreviations. Other indicators required
            (?P<state_abbrev> scr | ns | s )
        )
        """
