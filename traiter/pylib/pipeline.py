from .pipeline_builder import PipelineBuilder


def pipeline():
    pipes = PipelineBuilder(exclude="ner")

    pipes.add_terms(all_terms=True)

    pipes.colors()
    pipes.dates()
    pipes.elevations()
    pipes.habitats()
    pipes.lat_longs()

    pipes.delete_traits("delete_partial", keep_all=True)

    pipes.sentences()

    # pipes.debug_tokens()  # #########################################
    # pipes.debug_ents()  # ###########################################

    return pipes.build()
