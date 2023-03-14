from traiter.pylib import sentence_pipeline
from traiter.pylib.patterns import color
from traiter.pylib.patterns import habitat
from traiter.pylib.patterns import lat_long
from traiter.pylib.pipeline_builder import PipelineBuilder
from traiter.pylib.util import shorten

PIPELINE = PipelineBuilder(exclude="ner")
PIPELINE.tokenizer()
PIPELINE.terms(color.TERMS + lat_long.TERMS + habitat.TERMS)
PIPELINE.color()
# PIPELINE.add_debug_tokens_pipe()  # #########################################
PIPELINE.habitat()
PIPELINE.lat_long()
PIPELINE.delete_traits(["habitat_prefix", "habitat_suffix"])


SENT_NLP = sentence_pipeline.pipeline()


def test(text: str) -> list[dict]:
    """Find entities in the doc."""
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
