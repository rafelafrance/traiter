from spacy import registry

from ..pattern_compilers.matcher_compiler import MatcherCompiler
from .term_patterns import HABITAT_REPLACE

HABITAT = MatcherCompiler(
    "habitat",
    on_match="plant_habitat_v1",
    decoder={
        "habitat": {"ENT_TYPE": "habitat"},
        "prefix": {"ENT_TYPE": "habitat_prefix"},
        "suffix": {"ENT_TYPE": "habitat_suffix"},
    },
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
