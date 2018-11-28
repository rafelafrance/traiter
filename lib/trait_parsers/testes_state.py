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

        regexp_list.append(
            'reproductive_data',
            common_patterns + r"""
                (?P<key> (?&reproductive_data) ) .{1,40}?
                (?P<value> (?: (?&state) | (?&state_abbrev) ) )
                """)

        regexp_list.append(
            'reproductive_data_keyed',
            common_patterns + r"""
                (?P<key> (?&reproductive_data) )     .{1,40}?
                (?: (?&testes) | (?&testes_abbrev) ) .{0,40}?
                (?P<value> (?&key_req) )
                """)

        regexp_list.append(
            'reproductive_data_immediate',
            common_patterns + r"""
                (?P<key> (?&reproductive_data) ) .{1,2}?
                (?P<value> (?&key_req) )
                """)

        # Look for testes state
        regexp_list.append(
            'testes_state',
            common_patterns + r"""
                (?P<key>   (?&testes) ) \s+
                (?P<value> (?&state) | (?&state_abbrev) | (?&key_req) )
                """)

        # Look for abbreviated testes key and a full state
        regexp_list.append(
            'testes_abbrev_state',
            common_patterns + r"""
                (?P<key>   (?&testes_abbrev) ) \s*
                (?P<value> (?&state) | (?&key_req) )
                """)

        # Look for testes state
        regexp_list.append(
            'testes_state_only',
            common_patterns + r""" (?P<value> (?&state) ) """)

        return regexp_list

    common_patterns = TraitParser.numeric_patterns + r"""
        (?(DEFINE)
            # Negative state indicators
            (?P<not> not | non | no | semi | sub )

            # Completely
            (?P<complete>
                (?&not) (?&dash) (:? in )?
                (?: completely | complete ) \b
            )

            # Testes
            (?P<testes> \b
                (?: testes |  testis | testicles |  gonads?)
                (?: \s* normal)? \b )

            # Abbreviations for testes. Other indicators required
            (?P<testes_abbrev> \b (?: tes | ts | t) \b )

            # Forms of the word descend & some common misspellings
            (?P<descended>
                descend (?: ed)? | desc (?&dot) | decend (?: ed)? )

            # State words
            (?P<state> \b (?:
                (?&not) (?&dash) (?&testes)
                | (?&not) (?&dash)
                    (?: scrot (?&dot) | scrotum | scrotal | gonads?)
                | (?: scrot (?&dot) | scrotum | scrotal )
                | small ,? \s* (?&not)? (?&dash) (?&descended)
                | partially (?&dash_req) (?&descended)
                | part (?&dot) (?&dash_req) (?&descended)
                | part (?&dot) \s* (?&descended)
                | (?&not) (?&dash_req) (?: fully? ) (?&dash_req) (?&descended)
                | (?: fully? ) (?&dash_req) (?&descended)
                | (?&not) (?&dash_req) (?&descended)
                | (?: un) (?&descended)
                | (?&descended)
                | cryptorchism | cryptorchid | monorchism | monorchid
                | nscr | inguinal
            ) \b )

            # Key is required
            (?P<key_req> \b (?:
                (?&not)? -? (?: visible | enlarged )
                | small | abdominal | abdomin (?&dot) | abdom (?&dot)
            ) \b )

            # State Abbreviations. Other indicators required
            (?P<state_abbrev> \b (?: scr | ns | sc ) \b )

            # reproductive_data key
            (?P<reproductive_data> \b reproductive [\s_-]?
                         (?: data | state | condition ) \b )
        )
        """
