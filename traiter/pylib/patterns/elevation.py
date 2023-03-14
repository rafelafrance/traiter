# from spacy.util import registry
# from traiter.pylib.pattern_compilers.matcher_compiler import MatcherCompiler
#
# from . import common_patterns
# from .term_patterns import REPLACE_BASIC_TERMS
#
#
# ELEVATION = MatcherCompiler(
#     "elevation",
#     on_match="digi_leap_elevation_v1",
#     decoder=common_patterns.PATTERNS | {
#     },
#     patterns=[
#     ],
# )
#
#
# @registry.misc(ELEVATION.on_match)
# def on_elevation_match(ent):
#     for token in ent:
#         pass
