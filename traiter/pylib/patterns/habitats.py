from spacy import registry

from ..actions import REJECT_MATCH
from ..matcher_patterns import MatcherPatterns
from ..vocabulary.terms import TERMS

_NOPE_SUFFIX = """ road villa street sec sec.""".split()
_NOPE_PREFIX = """national botanical """.split()


_DECODER = {
    "habitat": {"ENT_TYPE": "habitat_term"},
    "prefix": {"ENT_TYPE": "habitat_prefix"},
    "suffix": {"ENT_TYPE": "habitat_suffix"},
    "nope_after": {"LOWER": {"IN": _NOPE_SUFFIX}},
    "nope_before": {"LOWER": {"IN": _NOPE_PREFIX}},
}

# ####################################################################################
HABITATS = MatcherPatterns(
    name="habitat",
    on_match="plant_habitat_v1",
    decoder=_DECODER,
    patterns=[
        "         habitat+",
        "prefix+  habitat+",
        "prefix+  habitat+ suffix",
        "         habitat+ suffix",
        "prefix+           suffix",
    ],
    output=["habitat"],
)


@registry.misc(HABITATS.on_match)
def on_habitat_match(ent):
    parts = [TERMS.replace.get(t.lower_, t.lower_) for t in ent]
    ent._.data["habitat"] = " ".join(parts)
    ent._.data["trait"] = "habitat"
    ent._.new_label = "habitat"
    if ent._.data.get("habitat_term"):
        del ent._.data["habitat_term"]


# ####################################################################################
NOT_HABITATS = MatcherPatterns(
    name="not_habitat",
    on_match=REJECT_MATCH,
    decoder=_DECODER,
    patterns=[
        "nope_before habitat",
        "nope_before habitat nope_after",
        "            habitat nope_after",
    ],
    output=None,
)
