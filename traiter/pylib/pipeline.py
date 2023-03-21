from traiter.pylib.patterns.terms import COLOR_TERMS
from traiter.pylib.patterns.terms import DATE_TERMS
from traiter.pylib.patterns.terms import ELEV_TERMS
from traiter.pylib.patterns.terms import HABITAT_TERMS
from traiter.pylib.patterns.terms import LAT_LONG_TERMS
from traiter.pylib.pipeline_builder import PipelineBuilder


def pipeline():
    terms = COLOR_TERMS + DATE_TERMS + ELEV_TERMS + LAT_LONG_TERMS + HABITAT_TERMS
    partial_traits = """
        habitat_prefix habitat_suffix month metric_length imperial_length about
        no_label elev_label uncertain_label
        """.split()

    pipes = PipelineBuilder(exclude="ner")
    pipes.add_terms(terms)
    pipes.colors()
    pipes.dates()
    # pipes.debug_tokens()  # #########################################
    pipes.elevations()
    pipes.habitats()
    pipes.lat_longs()
    pipes.delete_traits("delete_partial", delete=partial_traits)
    pipes.sentences()
    return pipes
