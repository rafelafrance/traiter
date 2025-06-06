import string
from pathlib import Path

from spacy.lang.char_classes import HYPHENS, LIST_HYPHENS

# ---------------------
# This points to the client's data directory not to the data directory here
DATA_DIR = Path.cwd() / "data"

# ---------------------
# Shapes for matching names

UPPER_SHAPES = """ XXXX       XXX XX X. XX. X """.split()
LOWER_SHAPES = """  xxxx  xxx  xx    x. xx. x """.split()

TITLE_SHAPES = """ Xxxxx Xxxx Xxx Xx X. Xx. X """.split()
O_SHAPES = """   X'Xxxxx   X'Xxxx   X'Xxx   X'Xx """.split()
O2_SHAPES = """  Xx'Xxxxx  Xx'Xxxx  Xx'Xxx  Xx'Xx """.split()
DEL_SHAPES = """ Xxx'Xxxxx Xxx'Xxxx Xxx'Xxx Xxx'Xx """.split()
MC_SHAPES = """  XxXxxxx   XxXxxx   XxXxx   XxXx """.split()
MAC_SHAPES = """ XxxXxxxx  XxxXxxx  XxxXxx  XxxXx """.split()
MAC4_SHAPES = """ XxxxXxxxx  XxxxXxxx  XxxxXxx  XxxxXx """.split()
MAC5_SHAPES = """ XxxxxXxxxx  XxxxxXxxx  XxxxxXxx  XxxxxXx """.split()

NAME_SHAPES = TITLE_SHAPES + MC_SHAPES + MAC_SHAPES + O_SHAPES + O2_SHAPES + DEL_SHAPES
NAME_SHAPES += MAC4_SHAPES + MAC5_SHAPES
NAME_AND_UPPER = NAME_SHAPES + UPPER_SHAPES

# ---------------------
# For importing taxa from an ITIS DB

ITIS_SPECIES_ID = 220

# ---------------------
# Useful character classes

CLOSE = " ) ] ".split()
COLON = " : ".split()
COMMA = " , ".split()
CROSS = " X x × ".split()
# DASH = ' - - -- -- '.split()
DASH = LIST_HYPHENS
DOT = " . ".split()
EQ = " = ".split()
OPEN = " ( [ ".split()
PLUS = " + ".split()
SEMICOLON = " ; ".split()
SLASH = " / ".split()
Q_MARK = " ? ".split()

D_QUOTE = ' " ” “ '.split()
S_QUOTE = " ' ` ‘ ´ ’ ".split()
QUOTE = D_QUOTE + S_QUOTE

LETTERS = list(string.ascii_lowercase)

TEMP = ["\\" + x for x in CLOSE]
CLOSE_RE = rf"[{''.join(TEMP)}]"

TEMP = ["\\" + x for x in OPEN]
OPEN_RE = rf"[{''.join(TEMP)}]"

DASH_RE = f"(?:{HYPHENS})"
DASH_CHAR = [d for d in DASH if len(d) == 1]

FLOAT_RE = r"(\d{1,3}(\.\d{,3})?)"
INT_RE = r"(\d{1,3})"

FLOAT_TOKEN_RE = f"^{FLOAT_RE}$"
INT_TOKEN_RE = f"^{INT_RE}$"
