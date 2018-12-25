"""Parse the notations."""

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
            'shorthand': Action(
                reduce=reduce.shorthand,
                args={'value': 0,
                      'part': 'shorthand_wt',
                      'units': 'shorthand_wt_units'}),
            'shorthand_key shorthand': Action(
                reduce=reduce.shorthand,
                args={'value': 1,
                      'part': 'shorthand_wt',
                      'units': 'shorthand_wt_units'}),
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

            'shorthand_key range metric_mass': Action(
                reduce=reduce.numeric_units, args={'value': 1, 'units': 2}),
            'shorthand_key range pounds': Action(
                reduce=reduce.numeric_units, args={'value': 1, 'units': 2}),
            'shorthand_key range ounces': Action(
                reduce=reduce.numeric_units, args={'value': 1, 'units': 2}),

            'wt_key range': Action(
                reduce=reduce.numeric_units, args={'value': 1}),

            'wt_key range pounds range ounces': Action(
                reduce=reduce.english_units, args={'start': 1}),
            'range pounds range ounces': Action(
                reduce=reduce.english_units,
                args={'start': 0, 'ambiguous': True}),

            'key_with_units range': Action(
                reduce=reduce.units_in_key, args={'key': 0, 'value': 1}),
        }
