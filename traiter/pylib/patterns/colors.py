import re

from spacy import registry

from . import common
from .. import actions
from .. import const
from ..pattern_compilers.matcher import Compiler
from ..vocabulary.terms import TERMS

_MULTIPLE_DASHES = ["\\" + c for c in const.DASH_CHAR]
_MULTIPLE_DASHES = rf'\s*[{"".join(_MULTIPLE_DASHES)}]{{2,}}\s*'
_SKIP = const.DASH + common.MISSING

_REMOVE = TERMS.pattern_dict("remove")

COLORS = Compiler(
    label="color",
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
    output=["color"],
)


@registry.misc(COLORS.on_match)
def on_color_match(ent):
    color_parts = []
    for token in ent:
        replace = TERMS.replace.get(token.lower_, token.lower_)
        if replace in _SKIP:  # Skip any in the list from above
            continue
        if _REMOVE.get(token.lower_):  # Skip terms marked for removal
            continue
        if token.pos_ == "AUX":  # Skip auxiliary verbs/words like: "is", "must"
            continue
        if token.shape_ in const.TITLE_SHAPES:  # Skip names like "Brown"
            continue
        part = re.sub(r"-$", "", replace)  # Remove trailing dash
        if part not in color_parts:
            color_parts.append(part)

    if not color_parts:
        raise actions.RejectMatch()

    value = "-".join(color_parts)
    value = re.sub(_MULTIPLE_DASHES, r"-", value)
    ent._.data["color"] = TERMS.replace.get(value, value)
    if any(t for t in ent if t.lower_ in common.MISSING):
        ent._.data["missing"] = True
