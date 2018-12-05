"""Parse the notations."""

from lib.lexers.base_lexer import BaseLexer


class BaseParser:
    """Shared parser logic."""

    forms = {

    }

    def __init__(self, lexer=BaseLexer):
        """Build the trait parsers."""
        self.lexer = lexer()
        self.lookahead = 0

    def parse(self, input):
        """Parse the tokens."""
        tokens = self.lexer.tokenize(input)

        found = False
        while not found:
            keys = [' '.join([tokens[0:i] for i in range(self.lookahead + 1)])]
            for key in keys:
                if key in self.forms:
                    found = True
                    self.forms[key]()
                else:
                    tokens.pop(0)
