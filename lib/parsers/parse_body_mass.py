"""Parse the notations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_body_mass import LexBodyMass
from lib.parsers.parse_base import ParseBase, Action
import lib.parsers.shared_reducers as reduce


class ParseBodyMass(ParseBase):
    """Parser logic."""

    def __init__(self):
        """Initialize the parser."""
        super().__init__(LexBodyMass)

    def rule_dict(self):
        """Return the parser rules."""
        return {
            'shorthand_mass': Action(
                reduce=reduce.shorthand_mass, args={'value': 0}),
            'shorthand_key shorthand_mass': Action(
                reduce=reduce.shorthand_mass, args={'value': 1}),
            'wt_key metric_mass range': Action(
                reduce=reduce.numeric_units, args={'value': 2, 'units': 1}),
            'wt_key pounds range': Action(
                reduce=reduce.numeric_units, args={'value': 2, 'units': 1}),
            'wt_key ounces range': Action(
                reduce=reduce.numeric_units, args={'value': 2, 'units': 1}),
            'wt_key range metric_mass': Action(
                reduce=reduce.numeric_units, args={'value': 1, 'units': 2}),
            'wt_key range pounds': Action(
                reduce=reduce.numeric_units, args={'value': 1, 'units': 2}),
            'wt_key range ounces': Action(
                reduce=reduce.numeric_units, args={'value': 1, 'units': 2}),

            'wt_key range': Action(
                reduce=reduce.numeric_units, args={'value': 1}),

            'wt_key range pounds range ounces': Action(
                reduce=reduce.english_units, args={'start': 1}),
            'range pounds range ounces': Action(
                reduce=reduce.english_units,
                args={'start': 0, 'ambiguous': True}),

        }
