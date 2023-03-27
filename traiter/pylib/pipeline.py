from .pipeline_builders.builder import PipelineBuilder
from .vocabulary import terms


def pipeline():
    pipes = PipelineBuilder(exclude="ner")

    pipes.tokenizer()

    pipes.add_terms(terms.TERMS)

    pipes.colors()
    pipes.dates()
    pipes.elevations()
    pipes.habitats()
    pipes.lat_longs()

    pipes.delete_traits("delete_partial", keep_outputs=True)

    pipes.sentences()

    # pipes.debug_tokens()  # #########################################

    return pipes.build()
