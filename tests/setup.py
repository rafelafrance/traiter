from traiter.pylib.patterns.color import COLOR_TERMS
from traiter.pylib.patterns.date_ import DATE_TERMS
from traiter.pylib.patterns.habitat import HABITAT_TERMS
from traiter.pylib.patterns.lat_long import LAT_LONG_TERMS
from traiter.pylib.pipelines import PipelineBuilder
from traiter.pylib.pipelines import SentencePipeline
from traiter.pylib.util import shorten

_TERMS = COLOR_TERMS + DATE_TERMS + LAT_LONG_TERMS + HABITAT_TERMS
_PARTIAL_TRAITS = ["habitat_prefix", "habitat_suffix", "month"]

_PIPELINE = PipelineBuilder(exclude="ner")
_PIPELINE.add_terms(_TERMS)
_PIPELINE.colors()
# _PIPELINE.add_debug_tokens_pipe()  # #########################################
_PIPELINE.dates()
_PIPELINE.habitats()
_PIPELINE.lat_longs()
_PIPELINE.delete_traits("delete_partial", delete=_PARTIAL_TRAITS)

SENT_NLP = SentencePipeline()


def test(text: str) -> list[dict]:
    text = shorten(text)
    doc = _PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
