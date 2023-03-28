from spacy.tokens import Span

from .new_patterns.color import color_pipe
from .new_patterns.date import date_pipe
from .new_patterns.elevation import elevation_pipe
from .new_patterns.habitat import habitat_pipe
from .new_patterns.lat_long import lat_long_pipe
from .pipeline_builders.builder import PipelineBuilder


def pipeline():
    Span.set_extension("data", default={})

    pipes = PipelineBuilder(exclude="ner")

    pipes.tokenizer()

    color_pipe.pipe(pipes.nlp)
    date_pipe.pipe(pipes.nlp)
    elevation_pipe.pipe(pipes.nlp)
    habitat_pipe.pipe(pipes.nlp)
    lat_long_pipe.pipe(pipes.nlp)

    pipes.sentences()

    # pipes.debug_tokens()  # #########################################

    for name in pipes.nlp.pipe_names:
        print(name)

    return pipes.build()
