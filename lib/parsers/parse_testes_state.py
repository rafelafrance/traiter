"""Parse the notations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_testes_state import LexTestesState
from lib.parsers.parse_base import ParseBase
import lib.parsers.reducers as reduce


class ParseTestesState(ParseBase):
    """Parser logic."""

    def __init__(self):
        """Initialize the parser."""
        super().__init__(LexTestesState)

    def rule_dict(self):
        """Return the parser rules."""
        return {
            'label testes': {'action': 'record'},
            'label abbrev': {'action': 'record'},

            'descended': {'action': 'desc'},
            'not descended': {'action': 'desc'},
            'abdominal descended': {'action': 'desc'},
            'abdominal not descended': {'action': 'desc'},
            'fully descended': {'action': 'desc'},
            'not fully descended': {'action': 'desc'},
            'partially descended': {'action': 'desc'},

            'size': {'action': 'desc'},
            'size descended': {'action': 'desc'},
            'size not descended': {'action': 'desc'},

            'label not testes':
                {'action': reduce.value_span, 'args': {'span': (1, 2)}},
            'label scrotal':
                {'action': reduce.value_span, 'args': {'span': (1, )}},

            'record desc':
                {'action': reduce.value_span, 'args': {'span': (1, )}},
            'record state_abbrev':
                {'action': reduce.value_span, 'args': {'span': (1, )}},
            'record abdominal':
                {'action': reduce.value_span, 'args': {'span': (1, )}},
            'record scrotal':
                {'action': reduce.value_span, 'args': {'span': (1, )}},
            'record not scrotal':
                {'action': reduce.value_span, 'args': {'span': (1, 2)}},
            'record other_words':
                {'action': reduce.value_span, 'args': {'span': (1, 2)}},
            'record not testes':
                {'action': reduce.value_span, 'args': {'span': (1, 2)}},

            'abbrev desc':
                {'action': reduce.value_span, 'args': {'span': (1, )}},
            'abbrev abdominal':
                {'action': reduce.value_span, 'args': {'span': (1, )}},
            'abbrev not scrotal':
                {'action': reduce.value_span, 'args': {'span': (1, 2)}},
            'abbrev scrotal':
                {'action': reduce.value_span, 'args': {'span': (1, )}},
            'abbrev other_words':
                {'action': reduce.value_span, 'args': {'span': (1, )}},

            'testes desc':
                {'action': reduce.value_span, 'args': {'span': (1, )}},
            'testes state_abbrev':
                {'action': reduce.value_span, 'args': {'span': (1, )}},
            'testes abdominal':
                {'action': reduce.value_span, 'args': {'span': (1, )}},
            'testes scrotal':
                {'action': reduce.value_span, 'args': {'span': (1, )}},
            'testes not scrotal':
                {'action': reduce.value_span, 'args': {'span': (1, 2)}},
            'testes other_words':
                {'action': reduce.value_span, 'args': {'span': (1, )}},

            'not testes':
                {'action': reduce.value_span, 'args': {'span': (0, 1)}},
            'not scrotal':
                {'action': reduce.value_span, 'args': {'span': (0, 1)}},
            'not gonads':
                {'action': reduce.value_span, 'args': {'span': (0, 1)}}}
