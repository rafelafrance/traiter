from traiter.pylib.traits.pattern_compiler import Compiler

DECODER = {
    "habitat": {"ENT_TYPE": "habitat_term"},
    "prefix": {"ENT_TYPE": "habitat_prefix"},
    "suffix": {"ENT_TYPE": "habitat_suffix"},
    "bad_prefix": {"ENT_TYPE": "bad_prefix"},
    "bad_suffix": {"ENT_TYPE": "bad_suffix"},
}


HABITAT_COMPILERS = [
    Compiler(
        label="habitat",
        decoder=DECODER,
        patterns=[
            "         habitat+",
            "prefix+  habitat+",
            "prefix+  habitat+ suffix",
            "         habitat+ suffix",
            "prefix+           suffix",
        ],
    ),
    Compiler(
        label="not_habitat",
        decoder=DECODER,
        patterns=[
            "bad_prefix habitat",
            "bad_prefix habitat bad_suffix",
            "           habitat bad_suffix",
        ],
    ),
]
