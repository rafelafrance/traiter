from traiter.pylib.patterns import terms_old
from traiter.pylib.pipe_builder import PipeBuilder


def pipeline():
    pipes = PipeBuilder(exclude="ner")
    pipes.add_terms(terms_old.ALL_TERMS)
    pipes.colors()
    pipes.dates()
    pipes.elevations()
    pipes.habitats()
    pipes.lat_longs()
    pipes.delete_traits("delete_partial", keep=terms_old.KEEP)
    pipes.sentences()

    pipes.debug_tokens()  # #########################################
    return pipes
