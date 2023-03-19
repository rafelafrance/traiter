from traiter.pylib.patterns.color import COLOR_TERMS
from traiter.pylib.patterns.date_ import DATE_TERMS
from traiter.pylib.patterns.habitat import HABITAT_TERMS
from traiter.pylib.patterns.lat_long import LAT_LONG_TERMS
from traiter.pylib.pipeline_builder import PipelineBuilder
from traiter.pylib.util import shorten

_TERMS = COLOR_TERMS + DATE_TERMS + LAT_LONG_TERMS + HABITAT_TERMS
_PARTIAL_TRAITS = ["habitat_prefix", "habitat_suffix", "month"]

PIPELINE = PipelineBuilder(exclude="ner")
PIPELINE.add_terms(_TERMS)
PIPELINE.colors()
# _PIPELINE.add_debug_tokens_pipe()  # #########################################
PIPELINE.dates()
PIPELINE.habitats()
PIPELINE.lat_longs()
PIPELINE.delete_traits("delete_partial", delete=_PARTIAL_TRAITS)
PIPELINE.sentences()


def test(text: str) -> list[dict]:
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
