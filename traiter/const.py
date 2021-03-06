"""Shared constants."""
from pathlib import Path

import regex as re
from spacy.lang.char_classes import HYPHENS, LIST_HYPHENS, LIST_QUOTES

__VERSION__ = '0.9.1'

# This points to the client's data directory to the data directory here
DATA_DIR = Path.cwd() / 'data'

FLAGS = re.VERBOSE | re.IGNORECASE

BATCH_SIZE = 1_000_000  # How many records to work with at a time

# Useful character classes
CLOSE = '  ) ] '.split()
COLON = ' : '.split()
COMMA = ' , '.split()
CROSS = ' x × '.split()
# DASH = ' – - –– -- '.split()
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

DASH_RE = f'(?:{HYPHENS})'
DASH_CHAR = [d for d in DASH if len(d) == 1]

FLOAT_RE = r'(\d+\.?\d*)'
INT_RE = r'(\d+)'

FLOAT_TOKEN_RE = f'^{FLOAT_RE}$'
INT_TOKEN_RE = f'^{INT_RE}$'
