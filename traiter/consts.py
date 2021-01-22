"""Shared constants."""

CLOSE = '  ) ] '.split()
COLON = ' :'.split()
COMMA = ' , '.split()
CROSS = ' x × '.split()
DASH = ' – - –– -- '.split()
DASH_RE = '|'.join(DASH)
DOT = ' . '.split()
EQ = ' = '.split()
OPEN = ' ( [ '.split()
PLUS = ' + '.split()
SEMICOLON = ' ; '.split()
SLASH = ' / '.split()
QUOTE = ' “ ” " \' '.split()
LETTERS = list('abcdefghijklmnopqrstuvwxyz')

FLOAT_RE = r'^\d+(\.\d*)?$'
INT_RE = r'^\d+$'
