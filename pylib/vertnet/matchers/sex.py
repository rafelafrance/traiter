"""Rule-based parsing of sex notations."""

from pathlib import Path
from itertools import zip_longest
import pandas as pd
import regex
import json
import spacy
from pylib.shared.util import DotDict


C = DotDict(
    rule_path='',

    # These should go into a shared module
    key_sep=list('=:"'),    # Separates key from value
    value_sep=list(';,"'),  # Separate value from next key
    quest=list('?'),
    quote=list('"'),
    letters_re='^[a-z]+$',
)


def setup():
    """Build a the rules and attach them to the nlp engine."""
