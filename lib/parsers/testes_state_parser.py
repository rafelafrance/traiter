"""Parse the notations."""

from lib.parsers.base_parser import BaseParser
from lib.lexers.testes_state_lexer import LexerTestesState


class ParserTestesState(BaseParser):
    """Shared parser logic."""

    def __init__(self):
        """Initialize the parser."""
        super().__init__(LexerTestesState)

    def get_rules(self):
        """Return the parser rules."""
        return {
            'label testes': {'action': 'record'},
            'label abbrev': {'action': 'record'},

            'label not testes':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'label scrotal':
                {'action': self.value_span, 'args': {'span': (1, )}},

            'record state_abbrev':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'record not testes':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'record descended':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'record not descended':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'record abdominal':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'record abdominal not descended':
                {'action': self.value_span, 'args': {'span': (1, 3)}},
            'record fully descended':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'record partially descended':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'record not fully descended':
                {'action': self.value_span, 'args': {'span': (1, 3)}},
            'record scrotal':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'record not scrotal':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'record other_words':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'record size':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'record size not descended':
                {'action': self.value_span, 'args': {'span': (1, 3)}},

            'testes descended':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'testes abdominal':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'testes scrotal':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'testes abdominal not descended':
                {'action': self.value_span, 'args': {'span': (1, 3)}},
            'testes not descended':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'testes not fully descended':
                {'action': self.value_span, 'args': {'span': (1, 3)}},
            'testes not scrotal':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'testes other_words':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'testes size not descended':
                {'action': self.value_span, 'args': {'span': (1, 3)}},
            'testes state_abbrev':
                {'action': self.value_span, 'args': {'span': (1, )}},

            'abbrev descended':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'abbrev abdominal':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'abbrev scrotal':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'abbrev abdominal not descended':
                {'action': self.value_span, 'args': {'span': (1, 3)}},
            'abbrev not descended':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'abbrev not fully descended':
                {'action': self.value_span, 'args': {'span': (1, 3)}},
            'abbrev not scrotal':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'abbrev other_words':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'abbrev size not descended':
                {'action': self.value_span, 'args': {'span': (1, 3)}},

            'not testes':
                {'action': self.value_span, 'args': {'span': (0, 1)}},
            'not scrotal':
                {'action': self.value_span, 'args': {'span': (0, 1)}},
            'not gonads':
                {'action': self.value_span, 'args': {'span': (0, 1)}}}
