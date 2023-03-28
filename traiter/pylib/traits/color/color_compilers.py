from ... import const
from traiter.pylib.matcher_compiler import Compiler

_MISSING = """
    no without missing lack lacking except excepting not rarely obsolete
    """.split()

COLOR = Compiler(
    label="color",
    decoder={
        "-": {"TEXT": {"IN": const.DASH}, "OP": "+"},
        "color_term": {"ENT_TYPE": "color_term"},
        "color_words": {"ENT_TYPE": {"IN": ["color_term", "color_mod"]}},
        "missing": {"LOWER": {"IN": _MISSING}},
        "to": {"POS": {"IN": ["AUX"]}},
    },
    patterns=[
        "missing? color_words* -* color_term+ -* color_words*",
        "missing? color_words+ to color_words+ color_term+ -* color_words*",
    ],
)
