from ... import const
from ...matcher_compiler import Compiler

COMPILERS = [
    Compiler(
        label="color",
        decoder={
            "-": {"TEXT": {"IN": const.DASH}, "OP": "+"},
            "color_term": {"ENT_TYPE": "color_term"},
            "color_words": {"ENT_TYPE": {"IN": ["color_term", "color_mod"]}},
            "missing": {"ENT_TYPE": "color_missing"},
            "to": {"POS": {"IN": ["AUX"]}},
        },
        patterns=[
            "missing? color_words* -* color_term+ -* color_words*",
            "missing? color_words+ to color_words+ color_term+ -* color_words*",
        ],
    ),
]
