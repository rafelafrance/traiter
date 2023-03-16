from traiter.pylib import sentence_pipeline
from traiter.pylib.patterns.color import COLOR_TERMS
from traiter.pylib.patterns.date_ import DATE_TERMS
from traiter.pylib.patterns.habitat import HABITAT_TERMS
from traiter.pylib.patterns.lat_long import LAT_LONG_TERMS
from traiter.pylib.pipeline_builder import PipelineBuilder
from traiter.pylib.util import shorten

_TERMS = COLOR_TERMS + DATE_TERMS + LAT_LONG_TERMS + HABITAT_TERMS
_PIPELINE = PipelineBuilder(exclude="ner")
_PIPELINE.terms(_TERMS)
_PIPELINE.colors()
# _PIPELINE.add_debug_tokens_pipe()  # #########################################
_PIPELINE.dates()
_PIPELINE.habitats()
_PIPELINE.lat_longs()
_PIPELINE.delete_traits(["habitat_prefix", "habitat_suffix", "month"])

SENT_NLP = sentence_pipeline.pipeline()


def test(text: str) -> list[dict]:
    text = shorten(text)
    doc = _PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
