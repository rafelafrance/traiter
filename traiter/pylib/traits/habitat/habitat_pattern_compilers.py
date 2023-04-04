from traiter.pylib.traits.pattern_compiler import Compiler


def habitat_compilers():
    decoder = {
        "habitat": {"ENT_TYPE": "habitat_term"},
        "prefix": {"ENT_TYPE": "habitat_prefix"},
        "suffix": {"ENT_TYPE": "habitat_suffix"},
        "bad_prefix": {"ENT_TYPE": "bad_prefix"},
        "bad_suffix": {"ENT_TYPE": "bad_suffix"},
    }

    return [
        Compiler(
            label="habitat",
            decoder=decoder,
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
            decoder=decoder,
            patterns=[
                "bad_prefix habitat",
                "bad_prefix habitat bad_suffix",
                "           habitat bad_suffix",
            ],
        ),
    ]
