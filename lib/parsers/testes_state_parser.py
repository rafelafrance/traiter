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
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'label scrotal':
                {'action': self.value_span, 'args': {'span': (1, )}},

            'record desc':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'record state_abbrev':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'record abdominal':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'record scrotal':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'record not scrotal':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'record other_words':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'record not testes':
                {'action': self.value_span, 'args': {'span': (1, 2)}},

            'abbrev desc':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'abbrev abdominal':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'abbrev not scrotal':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'abbrev scrotal':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'abbrev other_words':
                {'action': self.value_span, 'args': {'span': (1, )}},

            'testes desc':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'testes state_abbrev':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'testes abdominal':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'testes scrotal':
                {'action': self.value_span, 'args': {'span': (1, )}},
            'testes not scrotal':
                {'action': self.value_span, 'args': {'span': (1, 2)}},
            'testes other_words':
                {'action': self.value_span, 'args': {'span': (1, )}},

            'not testes':
                {'action': self.value_span, 'args': {'span': (0, 1)}},
            'not scrotal':
                {'action': self.value_span, 'args': {'span': (0, 1)}},
            'not gonads':
                {'action': self.value_span, 'args': {'span': (0, 1)}}}
