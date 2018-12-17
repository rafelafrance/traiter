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
            # 'size': Action(replace='desc'),

            'key_with_units number':
                Action(reduce=reduce.len_in_key, args={'key': 0, 'value': 1}),

            'total_len_key number units':
                Action(reduce=reduce.key_len_units,
                       args={'key': 0, 'value': 1, 'units': 2}),
        }
