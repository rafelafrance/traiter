from ...matcher_compiler import Compiler

_DECODER = {
    "habitat": {"ENT_TYPE": "habitat_term"},
    "prefix": {"ENT_TYPE": "habitat_prefix"},
    "suffix": {"ENT_TYPE": "habitat_suffix"},
    "bad_prefix": {"ENT_TYPE": "bad_prefix"},
    "bad_suffix": {"ENT_TYPE": "bad_suffix"},
}

HABITATS = Compiler(
    label="habitat",
    decoder=_DECODER,
    patterns=[
        "         habitat+",
        "prefix+  habitat+",
        "prefix+  habitat+ suffix",
        "         habitat+ suffix",
        "prefix+           suffix",
    ],
)

NOT_HABITATS = Compiler(
    label="not_habitat",
    decoder=_DECODER,
    patterns=[
        "bad_prefix habitat",
        "bad_prefix habitat bad_suffix",
        "           habitat bad_suffix",
    ],
)
