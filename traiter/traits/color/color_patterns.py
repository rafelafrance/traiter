from . import color_action as act
from traiter.pylib import const
from traiter.traits.pattern_compiler import Compiler


def color_patterns():
    return [
        Compiler(
            label="color",
            on_match=act.COLOR_MATCH,
            decoder={
                "-": {"TEXT": {"IN": const.DASH}},
                "color": {"ENT_TYPE": "color"},
                "color_words": {"ENT_TYPE": {"IN": ["color", "color_mod"]}},
                "missing": {"ENT_TYPE": "color_missing"},
                "to": {"POS": {"IN": ["AUX"]}},
            },
            patterns=[
                "missing? color_words* -* color+ -* color_words*",
                "missing? color_words+ to color_words+ color+ -* color_words*",
            ],
        ),
    ]
