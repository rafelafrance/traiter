"""Parse the notations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_total_length import LexTotalLength
from lib.parsers.parse_base import ParseBase, Action
import lib.parsers.reducers as reduce


class ParseTotalLength(ParseBase):
    """Parser logic."""

    def __init__(self):
        """Initialize the parser."""
        super().__init__(LexTotalLength)

    def rule_dict(self):
        """Return the parser rules."""
        return {
            'shorthand': Action(
                reduce=reduce.shorthand, args={'value': 0, 'part': 0}),

            'shorthand_key shorthand': Action(
                reduce=reduce.shorthand, args={'value': 1, 'part': 0}),

            'key_with_units range': Action(
                reduce=reduce.len_units_in_key, args={'key': 0, 'value': 1}),

            'total_len_key range metric_len': Action(
                reduce=reduce.key_len_units, args={'value': 1, 'units': 2}),
            'total_len_key range feet': Action(
                reduce=reduce.key_len_units, args={'value': 1, 'units': 2}),
            'total_len_key range inches': Action(
                reduce=reduce.key_len_units, args={'value': 1, 'units': 2}),
            'total_len_key range feet range inches': Action(
                reduce=reduce.english_len, args={'feet': 1, 'inches': 3}),
            'range feet range inches': Action(
                reduce=reduce.english_len, args={'feet': 0, 'inches': 2}),

            'total_len_key range': Action(
                reduce=reduce.key_len_no_units, args={'value': 1}),

        }
