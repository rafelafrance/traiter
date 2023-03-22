"""Update the tokenizer.

The default Spacy tokenizer works great for model-based parsing but sometimes causes
complications for rule-based parsers.
"""
from typing import Optional

from spacy.language import Language
from spacy.symbols import ORTH
from spacy.util import compile_infix_regex
from spacy.util import compile_prefix_regex
from spacy.util import compile_suffix_regex


def append_prefix_regex(nlp: Language, prefixes: Optional[list[str]] = None):
    prefixes = prefixes if prefixes else []
    prefixes += nlp.Defaults.prefixes
    prefix_re = compile_prefix_regex(prefixes)
    nlp.tokenizer.prefix_search = prefix_re.search


def append_suffix_regex(nlp: Language, suffixes: Optional[list[str]] = None):
    suffixes = suffixes if suffixes else []
    suffixes += nlp.Defaults.suffixes
    suffix_re = compile_suffix_regex(suffixes)
    nlp.tokenizer.suffix_search = suffix_re.search


def append_infix_regex(nlp: Language, infixes: Optional[list[str]] = None):
    infixes = infixes if infixes else []
    infixes += nlp.Defaults.infixes
    infix_re = compile_infix_regex(infixes)
    nlp.tokenizer.infix_finditer = infix_re.finditer


def append_abbrevs(nlp: Language, abbrevs: list[str]):
    for abbrev in abbrevs:
        nlp.tokenizer.add_special_case(abbrev, [{ORTH: abbrev}])


def remove_special_case(nlp: Language, remove: list[str]):
    """Remove special rules from the tokenizer.
    This is a workaround for when these special cases interfere with matcher rules.
    """
    specials = [r for r in nlp.tokenizer.rules if r not in remove]
    nlp.tokenizer.rules = None
    for text in specials:
        nlp.tokenizer.add_special_case(text, [{ORTH: text}])
