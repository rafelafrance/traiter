"""Shared constants."""

from spacy.lang.char_classes import LIST_HYPHENS, LIST_QUOTES


CLOSE = '  ) ] '.split()
COLON = ' :'.split()
COMMA = ' , '.split()
CROSS = ' x × '.split()
DASH = LIST_HYPHENS
DOT = ' . '.split()
EQ = ' = '.split()
OPEN = ' ( [ '.split()
PLUS = ' + '.split()
SEMICOLON = ' ; '.split()
SLASH = ' / '.split()
QUOTE = LIST_QUOTES
LETTERS = list('abcdefghijklmnopqrstuvwxyz')

TEMP = ['\\' + x for x in CLOSE]
CLOSE_RE = fr'[{"".join(TEMP)}]'

TEMP = ['\\' + x for x in OPEN]
OPEN_RE = fr'[{"".join(TEMP)}]'

TEMP = ['\\' + c for c in DASH[:2]]
DASH_RE = fr'[{"".join(TEMP)}]'

FLOAT_RE = r'(\d+\.?\d*)'
INT_RE = r'(\d+)'

FLOAT_TOKEN_RE = f'^{FLOAT_RE}$'
INT_TOKEN_RE = f'^{INT_RE}$'

DASH_CHAR = [d for d in DASH if len(d) == 1]
