"""Parse the notations."""

# pylint: disable=too-few-public-methods

from itertools import product
from lib.lexers.life_stage_lexer import LifeStageLexer
from lib.parsers.base_parser import BaseParser
import lib.parsers.reducers as reduce


class LifeStageParser(BaseParser):
    """Parser logic."""

    def __init__(self):
        """Initialize the parser."""
        super().__init__(LifeStageLexer)

    def rule_dict(self):
        """Return the parser rules."""
        rule_dict = {
            'keyless':
                {'action': reduce.value_span, 'args': {'span': (0, )}},

            'key keyless':
                {'action': reduce.value_span, 'args': {'span': (1, )}},
            'key keyless joiner keyless':
                {'action': reduce.value_span, 'args': {'span': (1, 3)}}}

        for j in range(1, 6):
            for prod in product(['keyless', 'word_plus'], repeat=j):
                tokens = ' '.join(prod)
                rule = f'key {tokens} stop'
                span = (1, )
                if j > 1:
                    span = (1, j)
                rule_dict[rule] = {
                    'action': reduce.value_span, 'args': {'span': span}}

        return rule_dict
