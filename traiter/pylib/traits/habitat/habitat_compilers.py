from traiter.pylib.matcher_compiler import Compiler

_NOPE_PREFIX = """national botanical """.split()
_NOPE_SUFFIX = """ road villa street sec sec. botanical""".split()


_DECODER = {
    "habitat": {"ENT_TYPE": "habitat_term"},
    "prefix": {"ENT_TYPE": "habitat_prefix"},
    "suffix": {"ENT_TYPE": "habitat_suffix"},
    "nope_after": {"LOWER": {"IN": _NOPE_SUFFIX}},
    "nope_before": {"LOWER": {"IN": _NOPE_PREFIX}},
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
        "nope_before habitat",
        "nope_before habitat nope_after",
        "            habitat nope_after",
    ],
)
