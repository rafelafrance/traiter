import re

from spacy import registry

from . import common
from .. import actions
from .. import const
from ..pattern_compilers.matcher import Compiler
from ..term_list import TermList

_MULTIPLE_DASHES = ["\\" + c for c in const.DASH_CHAR]
_MULTIPLE_DASHES = rf'\s*[{"".join(_MULTIPLE_DASHES)}]{{2,}}\s*'

_SKIP = const.DASH + common.MISSING

TERMS = TermList.shared("colors")
_REMOVE = TERMS.pattern_dict("remove")

MATCHER = Compiler(
    "color",
    on_match="plant_color_v1",
    decoder=common.PATTERNS
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


@registry.misc(MATCHER.on_match)
def on_color_match(ent):
    parts = []
    for token in ent:
        replace = TERMS.replace.get(token.lower_, token.lower_)
        if replace in _SKIP:
            continue
        if _REMOVE.get(token.lower_):
            continue
        if token.pos_ in ["AUX"]:
            continue
        if token.shape_ in const.TITLE_SHAPES:
            continue
        parts.append(replace)

    if not parts:
        raise actions.RejectMatch()

    value = "-".join(parts)
    value = re.sub(_MULTIPLE_DASHES, r"-", value)
    ent._.data["color"] = TERMS.replace.get(value, value)
    if any(t for t in ent if t.lower_ in common.MISSING):
        ent._.data["missing"] = True
