"""Parse the notations."""

# pylint: disable=too-few-public-methods


from lib.lexers.sex_lexer import SexLexer
from lib.parsers.base_parser import BaseParser
import lib.parsers.reducers as reduce


class SexParser(BaseParser):
    """Parser logic."""

    def __init__(self):
        """Initialize the parser."""
        super().__init__(SexLexer)

    def rule_dict(self):
        """Return the parser rules."""
        return {

            'sex': {'action': reduce.value_span, 'args': {'span': (0, )}},

            'sex quest':
                {'action': reduce.value_span, 'args': {'span': (0, 1)}},

            'key sex': {'action': reduce.value_span, 'args': {'span': (1, )}},

            'key sex quest':
                {'action': reduce.value_span, 'args': {'span': (1, 2)}},

            'key word': {'action': reduce.value_span, 'args': {'span': (1, )}},

            'key word quest':
                {'action': reduce.value_span, 'args': {'span': (1, 2)}},
        }

    def post_process(self, results, args=None):
        """Post-process the results."""
        return results if len(results) < 3 else []
