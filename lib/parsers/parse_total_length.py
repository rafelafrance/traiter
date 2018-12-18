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

            'shorthand_key range': Action(
                reduce=reduce.length, args={'value': 1}),
            'shorthand_key range metric_len': Action(
                reduce=reduce.length, args={'value': 1, 'units': 2}),
            'shorthand_key range feet': Action(
                reduce=reduce.length, args={'value': 1, 'units': 2}),
            'shorthand_key range inches': Action(
                reduce=reduce.length, args={'value': 1, 'units': 2}),

            'key_with_units range': Action(
                reduce=reduce.len_units_in_key, args={'key': 0, 'value': 1}),

            'total_len_key range': Action(
                reduce=reduce.length, args={'value': 1}),
            'total_len_key range metric_len': Action(
                reduce=reduce.length, args={'value': 1, 'units': 2}),
            'total_len_key range feet': Action(
                reduce=reduce.length, args={'value': 1, 'units': 2}),
            'total_len_key range inches': Action(
                reduce=reduce.length, args={'value': 1, 'units': 2}),
            'total_len_key range feet range inches': Action(
                reduce=reduce.english_len, args={'feet': 1, 'inches': 3}),
            'range feet range inches': Action(
                reduce=reduce.english_len, args={'feet': 0, 'inches': 2}),

            'total_len_key word range': Action(
                reduce=reduce.length, args={'value': 2}),
            'total_len_key word word range': Action(
                reduce=reduce.length, args={'value': 3}),
            'total_len_key word word word range': Action(
                reduce=reduce.length, args={'value': 4}),
            'total_len_key word range metric_len': Action(
                reduce=reduce.length, args={'value': 2, 'units': 3}),
            'total_len_key word word range metric_len': Action(
                reduce=reduce.length, args={'value': 3, 'units': 4}),
            'total_len_key word word word range metric_len': Action(
                reduce=reduce.length, args={'value': 4, 'units': 5}),
            'total_len_key word range feet': Action(
                reduce=reduce.length, args={'value': 2, 'units': 3}),
            'total_len_key word word range feet': Action(
                reduce=reduce.length, args={'value': 3, 'units': 4}),
            'total_len_key word word word range feet': Action(
                reduce=reduce.length, args={'value': 4, 'units': 5}),
            'total_len_key word range inches': Action(
                reduce=reduce.length, args={'value': 2, 'units': 3}),
            'total_len_key word word range inches': Action(
                reduce=reduce.length, args={'value': 3, 'units': 4}),
            'total_len_key word word word range inches': Action(
                reduce=reduce.length, args={'value': 4, 'units': 5}),

            'ambiguous range': Action(
                reduce=reduce.length,
                args={'value': 1, 'ambiguous': True}),
            'ambiguous range metric_len': Action(
                reduce=reduce.length,
                args={'value': 1, 'units': 2, 'ambiguous': True}),
            'ambiguous range feet': Action(
                reduce=reduce.length,
                args={'value': 1, 'units': 2, 'ambiguous': True}),
            'ambiguous range inches': Action(
                reduce=reduce.length,
                args={'value': 1, 'units': 2, 'ambiguous': True}),

            'key_units_req range metric_len': Action(
                reduce=reduce.length, args={'value': 1, 'units': 2}),
            'key_units_req range feet': Action(
                reduce=reduce.length, args={'value': 1, 'units': 2}),
            'key_units_req range inches': Action(
                reduce=reduce.length, args={'value': 1, 'units': 2}),

            # Due to the trailing total_len_key it is not longer ambiguous
            'ambiguous range total_len_key': Action(
                reduce=reduce.length,
                args={'value': 1, 'ambiguous': False}),
            'ambiguous range metric_len total_len_key': Action(
                reduce=reduce.length,
                args={'value': 1, 'units': 2, 'ambiguous': False}),
            'ambiguous range feet total_len_key': Action(
                reduce=reduce.length,
                args={'value': 1, 'units': 2, 'ambiguous': False}),
            'ambiguous range inches total_len_key': Action(
                reduce=reduce.length,
                args={'value': 1, 'units': 2, 'ambiguous': False}),

            'range total_len_key': Action(
                reduce=reduce.length, args={'value': 0}),
            'range metric_len total_len_key': Action(
                reduce=reduce.length, args={'value': 0, 'units': 1}),
            'range feet total_len_key': Action(
                reduce=reduce.length, args={'value': 0, 'units': 1}),
            'range inches total_len_key': Action(
                reduce=reduce.length, args={'value': 0, 'units': 1}),

            'total_len_key metric_len range': Action(
                reduce=reduce.length, args={'value': 2, 'units': 1}),
            'total_len_key feet range': Action(
                reduce=reduce.length, args={'value': 2, 'units': 1}),
            'total_len_key inches range': Action(
                reduce=reduce.length, args={'value': 2, 'units': 1}),

            'total_len_key fraction inches': Action(
                reduce=reduce.fraction, args={'value': 1, 'units': 2}),
            'key_units_req fraction inches': Action(
                reduce=reduce.fraction, args={'value': 1, 'units': 2}),
            'ambiguous fraction inches': Action(
                reduce=reduce.fraction,
                args={'value': 1, 'units': 2, 'ambiguous': True}),
        }

    def post_process(self, results, args=None):
        """Post-process the results."""
        return [r for r in results if r.value]
