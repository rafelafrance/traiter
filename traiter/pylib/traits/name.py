from pathlib import Path

import regex as re
from spacy.language import Language
from spacy.util import registry

from traiter.pylib import const
from traiter.pylib.pattern_compiler import Compiler
from traiter.pylib.pipes import add, reject_match
from traiter.pylib.traits import terms as t_terms

NAME_CSV = Path(t_terms.__file__).parent / "name_terms.csv"

PUNCT = "[.:;,_-]"

NAME_RE = "".join(const.OPEN + const.CLOSE + const.QUOTE + list(".,'&"))
NAME_RE = re.compile(rf"^[\sa-z{re.escape(NAME_RE)}-]+$")

CONFLICT = ["us_county", "color"]


def build(nlp: Language, overwrite: list[str] = None, min_len: int = 4):
    overwrite = overwrite if overwrite else []

    add.term_pipe(nlp, name="name_terms", path=NAME_CSV)

    # Block things that are definitely not names before we look for names
    add.trait_pipe(nlp, name="not_name_patterns", compiler=not_name_patterns())

    add.trait_pipe(
        nlp,
        name="name_patterns",
        compiler=name_patterns(min_len, overwrite),
        overwrite=overwrite + "name_prefix name_suffix".split(),
    )
    # add.debug_tokens(nlp)  # ##########################################


def not_name_patterns():
    decoder = {
        "name": {"SHAPE": {"IN": const.NAME_SHAPES}},
        "not_name": {"ENT_TYPE": "not_name"},
    }

    return [
        Compiler(
            label="not_name",
            on_match=reject_match.REJECT_MATCH,
            decoder=decoder,
            patterns=[
                "          name+ not_name+",
                "not_name+ name+",
                "not_name+ name+ not_name+",
            ],
        ),
    ]


def name_patterns(min_len: int = 4, overwrite: list[str] = None):
    overwrite = overwrite if overwrite else []
    min_shapes = [s for s in const.NAME_SHAPES if len(s) >= min_len and s[-1].isalpha()]

    decoder = {
        "(": {"TEXT": {"IN": const.OPEN + const.QUOTE}},
        ")": {"TEXT": {"IN": const.CLOSE + const.QUOTE}},
        ",": {"TEXT": {"IN": const.COMMA}},
        "..": {"TEXT": {"REGEX": r"^[.]+$"}},
        ":": {"LOWER": {"REGEX": rf"^(by|{PUNCT}+)$"}},
        "A": {"TEXT": {"REGEX": r"^[A-Z][._,]?$"}},
        "_": {"TEXT": {"REGEX": r"^[._,]+$"}},
        "conflict": {"ENT_TYPE": {"IN": overwrite}},
        "dr": {"ENT_TYPE": "name_prefix"},
        "jr": {"ENT_TYPE": "name_suffix"},
        "name": {"SHAPE": {"IN": const.NAME_SHAPES}},
        "min_len": {"SHAPE": {"IN": min_shapes}},
        "no_label": {"ENT_TYPE": "no_label"},
        "no_space": {"SPACY": False},
    }

    return [
        Compiler(
            label="name",
            on_match="name_match",
            decoder=decoder,
            patterns=[
                "       name name?     no_space* min_len",
                "       name name?     no_space* min_len _? jr+",
                "       name name?     conflict",
                "       name name?     conflict          _? jr+",
                "       conflict name? no_space* min_len ",
                "       conflict name? no_space* min_len _? jr+",
                "       A A? A?        no_space* min_len",
                "       A A? A?        no_space* min_len _? jr+",
                "       name A A? A?   no_space* min_len",
                "       name A A? A?   no_space* min_len _? jr+",
                "       name ..        no_space* min_len",
                "       name ..        no_space* min_len _? jr+",
                "       name ( name )  no_space* min_len",
                "       name ( name )  no_space* min_len _? jr+",
                "       name ( name )  no_space* min_len",
                "dr+ _? name   name?   no_space* min_len",
                "dr+ _? name   name?   no_space* min_len _? jr+",
                "dr+ _? name   name?   conflict",
                "dr+ _? name   name?   conflict          _? jr+",
                "dr+ _? conflict name? no_space* min_len",
                "dr+ _? conflict name? no_space* min_len _? jr+",
                "dr+ _? A A? A?        no_space* min_len",
                "dr+ _? A A? A?        no_space* min_len _? jr+",
                "dr+ _? name A A? A?   no_space* min_len",
                "dr+ _? name A A? A?   no_space* min_len _? jr+",
                "dr+ _? name ..        no_space* min_len",
                "dr+ _? name ..        no_space* min_len _? jr+",
                "dr+ _? name ( name )  no_space* min_len",
                "dr+ _? name ( name )  no_space* min_len _? jr+",
                "dr+ _? name ( name )  no_space* min_len",
            ],
        ),
    ]


@registry.misc("name_match")
def name_match(ent):
    name = ent.text
    name = re.sub(rf" ({PUNCT})", r"\1", name)
    name = re.sub(r"\.\.|_", "", name)

    if not NAME_RE.match(name.lower()):
        raise reject_match.RejectMatch

    for token in ent:
        token._.flag = "name"

        # Only accept some parts of speech
        if len(token.text) > 1 and token.pos_ not in ("PROPN", "NOUN", "PUNCT", "AUX"):
            raise reject_match.RejectMatch

        # If there's a digit in the name reject it
        if re.search(r"\d", token.text):
            raise reject_match.RejectMatch

        # If it is all lower case reject it
        if token.text.islower():
            raise reject_match.RejectMatch

    ent._.data = {"name": name}

    # Save for name usage in other traits
    ent[0]._.data = ent._.data
    ent[0]._.flag = "name_data"
