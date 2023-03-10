from spacy import registry

from ..pattern_compilers.matcher_compiler import MatcherCompiler
from .term_patterns import HABITAT_REPLACE
from traiter.pylib.actions import REJECT_MATCH


NOPE_SUFFIX = """ road """.split()
NOPE_PREFIX = """""".split()

DECODER = {
    "habitat": {"ENT_TYPE": "habitat"},
    "prefix": {"ENT_TYPE": "habitat_prefix"},
    "suffix": {"ENT_TYPE": "habitat_suffix"},
    "nope_after": {"LOWER": {"IN": NOPE_SUFFIX}},
}


HABITAT = MatcherCompiler(
    "habitat",
    on_match="plant_habitat_v1",
    decoder=DECODER,
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
    parts = [HABITAT_REPLACE.get(t.lower_, t.lower_) for t in ent]
    ent._.data["habitat"] = " ".join(parts)


# ####################################################################################
NOT_name = MatcherCompiler(
    "not_habitat",
    on_match=REJECT_MATCH,
    decoder=DECODER,
    patterns=[
        "habitat nope_after",
    ],
)
