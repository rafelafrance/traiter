from traiter.pylib.patterns import terms
from traiter.pylib.pipeline_builder import PipelineBuilder


def pipeline():
    pipes = PipelineBuilder(exclude="ner")
    pipes.add_terms(terms.ALL_TERMS)
    # pipes.colors()
    pipes.dates()
    # pipes.debug_tokens()  # #########################################
    pipes.elevations()
    pipes.habitats()
    pipes.lat_longs()
    pipes.delete_traits("delete_partial", keep=terms.KEEP)
    pipes.sentences()

    # pipes.debug_tokens()  # #########################################
    return pipes
