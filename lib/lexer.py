"""Tokenize the notations."""

from sly import Lexer


class TraitLexer(Lexer):
    """Tokenize the notations."""

    tokens = {
        LPAR, RPAR, LSQB, RSQB, COLON, COMMA, SEMI, PLUS, DASH,  # noqa: F821
        STAR, SLASH, VBAR, AMPER, LESS, GREATER, EQUAL, DOT,     # noqa: F821
        PERCENT, LBRACE, RBRACE, AT, SQUOTE, DQUOTE, QUEST,      # noqa: F821
        BSLASH, WORD, NUMBER}                                    # noqa: F821

    NUMBER = r'(?:\d{1,3}(?:,\d{3}){1,3}|\d+)(?:\.\d+)?'
    WORD = r'\w+'

    LPAR = r'\('
    RPAR = r'\)'
    LSQB = r'\['
    RSQB = r'\]'
    COLON = r':'
    COMMA = r','
    SEMI = r';'
    PLUS = r'\+'
    DASH = r'-'
    STAR = r'\*'
    SLASH = r'/'
    VBAR = r'\|'
    AMPER = r'&'
    LESS = r'<'
    GREATER = r'>'
    EQUAL = r'='
    DOT = r'\.'
    PERCENT = r'%'
    LBRACE = r'\{'
    RBRACE = r'\}'
    AT = r'@'
    SQUOTE = r"'"
    DQUOTE = r'"'
    QUEST = r'\?'
    BSLASH = r'\\'

    ignore = r'\s+'

    def error(self, t):
        """Skip illegal characters."""
        self.index += 1


if __name__ == '__main__':
    data = ('{"totalLengthInmm":"2,100.5",    " tailLengthInmm":"65", #'
            '"hindfootLengthInmm":"25", "earLengthInmm":"10", "weightIn":"X"}')
    lexer = TraitLexer()
    for tk in lexer.tokenize(data):
        print(tk)
