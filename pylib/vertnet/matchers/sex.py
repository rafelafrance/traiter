"""Rule-based parsing of sex notations."""

from pathlib import Path
from itertools import zip_longest
import pandas as pd
import regex
import json
import spacy


def setup():
    """Build a the rules and attach them to the nlp engine."""
