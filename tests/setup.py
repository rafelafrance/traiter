from traiter.pylib import sentence_pipeline
from traiter.pylib.patterns import color_patterns
from traiter.pylib.patterns import habitat_patterns
from traiter.pylib.patterns import lat_long_patterns
from traiter.pylib.pipeline_builder import PipelineBuilder
from traiter.pylib.util import shorten

PIPELINE = PipelineBuilder(exclude="ner")
PIPELINE.add_tokenizer_pipe()
PIPELINE.add_term_patterns(
    color_patterns.COLOR_TERMS
    + lat_long_patterns.LAT_LONG_TERMS
    + habitat_patterns.HABITAT_TERMS
)
PIPELINE.add_color_patterns()
# PIPELINE.add_debug_tokens_pipe()  # #########################################
PIPELINE.add_habitat_patterns()
PIPELINE.add_lat_long_patterns()
PIPELINE.add_delete_traits_patterns(["habitat_prefix", "habitat_suffix"])


SENT_NLP = sentence_pipeline.pipeline()


def test(text: str) -> list[dict]:
    """Find entities in the doc."""
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    return traits
