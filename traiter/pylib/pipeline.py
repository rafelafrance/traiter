from .matcher_patterns import MatcherPatterns
from .patterns import colors
from .patterns import dates
from .patterns import elevations
from .patterns import habitats
from .patterns import lat_longs
from .pipe_builder import PipeBuilder


def pipeline():
    patterns = (
        colors.COLORS,
        dates.DATES,
        dates.MISSING_DAYS,
        elevations.ELEVATIONS,
        elevations.ELEVATION_RANGES,
        habitats.HABITATS,
        habitats.NOT_HABITATS,
        lat_longs.LAT_LONGS,
        lat_longs.LAT_LONG_UNCERTAIN,
    )

    pipes = PipeBuilder(exclude="ner")

    pipes.add_terms(MatcherPatterns.all_terms(patterns))

    pipes.colors()
    pipes.dates()
    pipes.elevations()
    pipes.habitats()
    pipes.lat_longs()

    pipes.delete_traits("delete_partial", keep=MatcherPatterns.all_keeps(patterns))

    pipes.sentences()

    # pipes.debug_tokens()  # #########################################
    # pipes.debug_ents()  # ###########################################

    return pipes
