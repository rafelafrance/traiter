from traiter.pylib import sentence_pipeline
from traiter.pylib.patterns.color import COLOR_TERMS
from traiter.pylib.patterns.date_ import DATE_TERMS
from traiter.pylib.patterns.habitat import HABITAT_TERMS
from traiter.pylib.patterns.lat_long import LAT_LONG_TERMS
from traiter.pylib.pipeline_builder import PipelineBuilder
from traiter.pylib.util import shorten

PIPELINE = PipelineBuilder(exclude="ner")
PIPELINE.tokenizer()
PIPELINE.terms(COLOR_TERMS + DATE_TERMS + LAT_LONG_TERMS + HABITAT_TERMS)
PIPELINE.color()
# PIPELINE.add_debug_tokens_pipe()  # #########################################
PIPELINE.date_()
PIPELINE.habitat()
PIPELINE.lat_long()
PIPELINE.delete_traits(["habitat_prefix", "habitat_suffix", "month"])

SENT_NLP = sentence_pipeline.pipeline()


def test(text: str) -> list[dict]:
    """Find entities in the doc."""
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
