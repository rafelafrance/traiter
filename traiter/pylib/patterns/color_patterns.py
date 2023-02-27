import re

from spacy import registry

from . import common_patterns
from .. import actions
from .. import const
from ..pattern_compilers.matcher_compiler import MatcherCompiler
from .term_patterns import COLOR_REMOVE
from .term_patterns import COLOR_REPLACE

MULTIPLE_DASHES = ["\\" + c for c in const.DASH_CHAR]
MULTIPLE_DASHES = rf'\s*[{"".join(MULTIPLE_DASHES)}]{{2,}}\s*'

SKIP = const.DASH + common_patterns.MISSING

COLOR = MatcherCompiler(
    "color",
    on_match="plant_color_v1",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "color_words": {"ENT_TYPE": {"IN": ["color", "color_mod"]}},
        "color": {"ENT_TYPE": "color"},
        "to": {"POS": {"IN": ["AUX"]}},
    },
    patterns=[
        "missing? color_words* -* color+ -* color_words*",
        "missing? color_words+ to color_words+ color+ -* color_words*",
    ],
)


@registry.misc(COLOR.on_match)
def on_color_match(ent):
    parts = []
    for token in ent:
        replace = COLOR_REPLACE.get(token.lower_, token.lower_)
        if replace in SKIP:
            continue
        if COLOR_REMOVE.get(token.lower_):
            continue
        if token.pos_ in ["AUX"]:
            continue
        if token.shape_ in const.TITLE_SHAPES:
            continue
        parts.append(replace)

    if not parts:
        ent._.delete = True
        raise actions.RejectMatch()

    value = "-".join(parts)
    value = re.sub(MULTIPLE_DASHES, r"-", value)
    ent._.data["color"] = COLOR_REPLACE.get(value, value)
    if any(t for t in ent if t.lower_ in common_patterns.MISSING):
        ent._.data["missing"] = True
