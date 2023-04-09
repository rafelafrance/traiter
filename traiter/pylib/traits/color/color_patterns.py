from . import color_action as act
from ... import const
from ..pattern_compiler import Compiler


def color_patterns():
    return [
        Compiler(
            label="color",
            on_match=act.COLOR_MATCH,
            decoder={
                "-": {"TEXT": {"IN": const.DASH}},
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
