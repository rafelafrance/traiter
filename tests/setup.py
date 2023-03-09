from traiter.pylib import sentence_pipeline
from traiter.pylib.patterns import term_patterns as terms
from traiter.pylib.pipeline_builder import PipelineBuilder
from traiter.pylib.util import shorten

# Singleton for testing
PIPELINE = PipelineBuilder(exclude="ner")
PIPELINE.add_tokenizer_pipe()
PIPELINE.add_term_patterns(terms.COLOR_TERMS + terms.HABITAT_TERMS)
PIPELINE.add_color_patterns()
# PIPELINE.add_debug_tokens_pipe()  # #########################################
PIPELINE.add_habitat_patterns()
PIPELINE.add_delete_traits_patterns(terms.PARTIAL_TRAITS)


SENT_NLP = sentence_pipeline.pipeline()  # Singleton for testing


def test(text: str) -> list[dict]:
    """Find entities in the doc."""
    text = shorten(text)
    doc = PIPELINE(text)
    traits = [e._.data for e in doc.ents]

    # from pprint import pp
    # pp(traits, compact=True)

    # from spacy import displacy
    # displacy.serve(doc, options={'collapse_punct': False, 'compact': True})

    return traits
