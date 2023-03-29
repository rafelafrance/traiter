import string
from pathlib import Path

from spacy.lang.char_classes import HYPHENS
from spacy.lang.char_classes import LIST_HYPHENS
from spacy.lang.char_classes import LIST_QUOTES

# ###################################################################################
# This points to the client's data directory not to the data directory here
DATA_DIR = Path.cwd() / "data"

# ###################################################################################
LOWER_SHAPES = set(""" xxxxx xxxx xxx xx x. xx. x """.split())
TITLE_SHAPES = set(""" Xxxxx Xxxx Xxx Xx X. Xx. X """.split())
UPPER_SHAPES = set(""" XXXXX XXXX XXX XX X. XX. X """.split())
NAME_SHAPES = list(TITLE_SHAPES) + list(UPPER_SHAPES)

# ###################################################################################
# Punctuation penalties when linking traits

TOKEN_WEIGHTS = {",": 3, ";": 7, ".": 7, "with": 10, "of": 7}
NEVER = 9999
REVERSE_WEIGHTS = {k: v * 2 for k, v in TOKEN_WEIGHTS.items()}
REVERSE_WEIGHTS[";"] = NEVER
REVERSE_WEIGHTS["."] = NEVER

TOKEN_WEIGHTS = {
    ",": 2,
    ";": 5,
    ".": NEVER,
}

# ###################################################################################
# For importing taxa from an ITIS DB

ITIS_SPECIES_ID = 220

# ###################################################################################
# Useful character classes

CLOSE = "  ) ] ".split()
COLON = " : ".split()
COMMA = " , ".split()
CROSS = " X x × ".split()
# DASH = ' – - –– -- '.split()
DASH = LIST_HYPHENS
DOT = " . ".split()
EQ = " = ".split()
OPEN = " ( [ ".split()
PLUS = " + ".split()
SEMICOLON = " ; ".split()
SLASH = " / ".split()
Q_MARK = " ? ".split()
QUOTE = LIST_QUOTES
LETTERS = list(string.ascii_lowercase)

TEMP = ["\\" + x for x in CLOSE]
CLOSE_RE = rf'[{"".join(TEMP)}]'

TEMP = ["\\" + x for x in OPEN]
OPEN_RE = rf'[{"".join(TEMP)}]'

DASH_RE = f"(?:{HYPHENS})"
DASH_CHAR = [d for d in DASH if len(d) == 1]

FLOAT_RE = r"(\d+\.?\d*)"
INT_RE = r"(\d+)"

FLOAT_TOKEN_RE = f"^{FLOAT_RE}$"
INT_TOKEN_RE = f"^{INT_RE}$"
