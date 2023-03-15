from spacy import registry

from ..pattern_compilers.matcher import Compiler
from ..term_list import TermList
from traiter.pylib.actions import REJECT_MATCH

HABITAT_TERMS = TermList().shared("habitat")

_NOPE_SUFFIX = """ road """.split()
_NOPE_PREFIX = """national """.split()

_DECODER = {
    "habitat": {"ENT_TYPE": "habitat"},
    "prefix": {"ENT_TYPE": "habitat_prefix"},
    "suffix": {"ENT_TYPE": "habitat_suffix"},
    "nope_after": {"LOWER": {"IN": _NOPE_SUFFIX}},
    "nope_before": {"LOWER": {"IN": _NOPE_PREFIX}},
}

HABITAT = Compiler(
    "habitat",
    on_match="plant_habitat_v1",
    decoder=_DECODER,
    patterns=[
        "         habitat+",
        "prefix+  habitat+",
        "prefix+  habitat+ suffix",
        "         habitat+ suffix",
        "prefix+           suffix",
    ],
)


@registry.misc(HABITAT.on_match)
def on_habitat_match(ent):
    parts = [HABITAT_TERMS.replace.get(t.lower_, t.lower_) for t in ent]
    ent._.data["habitat"] = " ".join(parts)


# ####################################################################################
NOT_HABITAT = Compiler(
    "not_habitat",
    on_match=REJECT_MATCH,
    decoder=_DECODER,
    patterns=[
        "nope_before habitat",
        "nope_before habitat nope_after",
        "            habitat nope_after",
    ],
)
