"""Parse the notations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_testes_state import LexTestesState
from lib.parsers.parse_base import ParseBase, Action
import lib.parsers.reducers as reduce


class ParseTestesState(ParseBase):
    """Parser logic."""

    def __init__(self):
        """Initialize the parser."""
        super().__init__(LexTestesState)

    def rule_dict(self):
        """Return the parser rules."""
        return {
            'label testes': Action(replace='record'),
            'label abbrev': Action(replace='record'),

            'descended': Action(replace='desc'),
            'not descended': Action(replace='desc'),
            'abdominal descended': Action(replace='desc'),
            'abdominal not descended': Action(replace='desc'),
            'fully descended': Action(replace='desc'),
            'not fully descended': Action(replace='desc'),
            'partially descended': Action(replace='desc'),

            'size': Action(replace='desc'),
            'size descended': Action(replace='desc'),
            'size not descended': Action(replace='desc'),

            'label not testes':
                Action(reduce=reduce.value_span, args={'span': (1, 2)}),
            'label scrotal':
                Action(reduce=reduce.value_span, args={'span': (1, )}),

            'record desc':
                Action(reduce=reduce.value_span, args={'span': (1, )}),
            'record state_abbrev':
                Action(reduce=reduce.value_span, args={'span': (1, )}),
            'record abdominal':
                Action(reduce=reduce.value_span, args={'span': (1, )}),
            'record scrotal':
                Action(reduce=reduce.value_span, args={'span': (1, )}),
            'record not scrotal':
                Action(reduce=reduce.value_span, args={'span': (1, 2)}),
            'record other_words':
                Action(reduce=reduce.value_span, args={'span': (1, 2)}),
            'record not testes':
                Action(reduce=reduce.value_span, args={'span': (1, 2)}),

            'abbrev desc':
                Action(reduce=reduce.value_span, args={'span': (1, )}),
            'abbrev abdominal':
                Action(reduce=reduce.value_span, args={'span': (1, )}),
            'abbrev not scrotal':
                Action(reduce=reduce.value_span, args={'span': (1, 2)}),
            'abbrev scrotal':
                Action(reduce=reduce.value_span, args={'span': (1, )}),
            'abbrev other_words':
                Action(reduce=reduce.value_span, args={'span': (1, )}),

            'testes desc':
                Action(reduce=reduce.value_span, args={'span': (1, )}),
            'testes state_abbrev':
                Action(reduce=reduce.value_span, args={'span': (1, )}),
            'testes abdominal':
                Action(reduce=reduce.value_span, args={'span': (1, )}),
            'testes scrotal':
                Action(reduce=reduce.value_span, args={'span': (1, )}),
            'testes not scrotal':
                Action(reduce=reduce.value_span, args={'span': (1, 2)}),
            'testes other_words':
                Action(reduce=reduce.value_span, args={'span': (1, )}),

            'not testes':
                Action(reduce=reduce.value_span, args={'span': (0, 1)}),
            'not scrotal':
                Action(reduce=reduce.value_span, args={'span': (0, 1)}),
            'not gonads':
                Action(reduce=reduce.value_span, args={'span': (0, 1)})}
