"""Find testes state annotations."""

from lib.parser_battery import ParserBattery
from lib.trait_parser import TraitParser


class ParseTestesState(TraitParser):
    """Find testes state annotations."""

    def __init__(self, preferred=''):
        """Add defaults for the measurements."""
        super().__init__()
        self.battery = self._battery(self.common_patterns)
        self.preferred = preferred
        self.parser = self.preferred_or_search

    @staticmethod
    def success(result):
        """Return this when the measurement is found."""
        return {
            'key': result['key'],
            'has_testes_state': True,
            'testes_state': result['value'],
            'regex': result['regex']}

    @staticmethod
    def fail():
        """Return this when the measurement is not found."""
        return {
            'key': None,
            'has_testes_state': False,
            'testes_state': None,
            'regex': None}

    @staticmethod
    def _battery(common_patterns):
        battery = ParserBattery()

        # Look for testes state
        battery.append(
            'testes_state',
            common_patterns + r"""
                \b (?P<key>  (?&testes) ) \s*
                   (?P<value> (?&state) | (?&state_abbrev) )
                """)

        # Look for abbreviated testes key and a full state
        battery.append(
            'testes_abbrev_state',
            common_patterns + r"""
                \b (?P<key>  (?&testes_abbrev) ) \s*
                   (?P<value> (?&state) )
                """)

        return battery

    common_patterns = TraitParser.common_regex_mass_length + r"""
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

            # State words
            (?P<state>
                (?&not)? (?&dash) (?: scrot (?&dot) | scrotum | scrotal ) \b
              | (?&not)? (?&dash) (?: fully? )? (?&dash)
                descend (?&dot) (?: ed)?  \b
              | undescended | undescend (?&dot) | undesc (?&dot)
              | abdominal | abdomin (?&dot) | abdom (?&dot)
              | cryptorchism | cryptorchid | monorchism | monorchid
              | nscr
            )

            # State Abbreviations. Other indicators required
            (?P<state_abbrev> scr | ns | s )
        )
        """
