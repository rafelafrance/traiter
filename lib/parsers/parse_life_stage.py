"""Parse the notations."""

from itertools import product
from lib.lexers.lex_life_stage import LexLifeStage
from lib.parsers.parse_base import ParseBase, Action
import lib.parsers.shared_reducers as reduce


class ParseLifeStage(ParseBase):
    """Parser logic."""

    def __init__(self):
        """Initialize the parser."""
        super().__init__(LexLifeStage)

    def rule_dict(self):
        """Return the parser rules."""
        rule_dict = {
            'keyless':
                Action(reduce=reduce.value_span, args={'span': (0, )}),

            'key keyless':
                Action(reduce=reduce.value_span, args={'span': (1, )}),
            'key word_plus keyless':
                Action(reduce=reduce.value_span, args={'span': (1, 2)}),
            'key word_plus joiner keyless':
                Action(reduce=reduce.value_span, args={'span': (1, 3)}),
            'key keyless joiner keyless':
                Action(reduce=reduce.value_span, args={'span': (1, 3)})}

        for j in range(1, 6):
            for prod in product(['keyless', 'word_plus'], repeat=j):
                tokens = ' '.join(prod)
                rule = f'key {tokens} sep'
                span = (1, )
                if j > 1:
                    span = (1, j)
                rule_dict[rule] = Action(
                    reduce=reduce.value_span, args={'span': span})

        return rule_dict
