"""Parse life stage notations."""

from pylib.stacked_regex.vocabulary import Vocabulary
from pylib.vertnet.parsers.base import Base, convert
import pylib.vertnet.shared_patterns as patterns

VOCAB = Vocabulary(patterns.VOCAB)

TIME_OPTIONS = VOCAB['time_units'].pattern

LIFE_STAGE = Base(
    name=__name__.split('.')[-1],
    rules=[
        # JSON keys for life stage
        VOCAB.term('json_key', [
            r' life \s* stage \s* (remarks?)? ',
            r' age \s* class ',
            r' age \s* in \s* (?P<time_units> {}) '.format(TIME_OPTIONS),
            r' age ']),

        # These words are life stages without a keyword indicator
        VOCAB.term('intrinsic', [
            r' yolk \s? sac ',
            r' young [\s-]? of [\s-]? the [\s-]? year ',
            r' adult \s* young ',
            r' young \s* adult ']
                     + """
                ads? adulte?s?
                chicks?
                fledgelings? fleglings? fry
                hatched hatchlings?
                imagos? imms? immatures?
                jeunes? juvs? juveniles? juvéniles?
                larvae? larvals? larves? leptocephales? leptocephalus
                matures? metamorphs?
                neonates? nestlings? nulliparous
                premetamorphs?
                sub-adults? subads? subadulte?s?
                tadpoles? têtard
                yearlings? yg ygs young
            """.split()),

        # This indicates that the following words are NOT a life stage
        VOCAB.term('skip', r' determin \w* '),

        # Compound words separated by dashes or slashes
        # E.g. adult/juvenile or over-winter
        VOCAB.part('joiner', r' \s* [/-] \s* '),

        # Use this to find the end of a life stage pattern
        VOCAB.part('separator', r' [;,"?] | $ '),

        # For life stages with numbers as words in them
        VOCAB['ordinals'],

        VOCAB['time_units'],

        VOCAB.part('after', 'after'),
        VOCAB.part('hatching', 'hatching'),

        # Match any word
        VOCAB.part('word', r' \b \w [\w?.-]* (?! [./-] ) '),

        VOCAB.grouper('as_time', ' after? (ordinals | hatching) time_units'),

        # E.g.: life stage juvenile/yearling
        VOCAB.producer(
            convert,
            'json_key (?P<value> ( intrinsic | word ) joiner intrinsic )'),

        # E.g.: life stage young adult
        VOCAB.producer(
            convert, 'json_key (?P<value> ( intrinsic | word ) intrinsic )'),

        # E.g.: life stage yearling
        VOCAB.producer(convert, 'json_key (?P<value> intrinsic )'),

        # A sequence of words bracketed by a keyword and a separator
        # E.g.: LifeStage Remarks: 5-6 wks;
        VOCAB.producer(
            convert,
            """ json_key (?P<value> ( intrinsic | word | joiner ){1,5} )
            separator """),

        # E.g.: LifeStage = 1st month
        VOCAB.producer(convert, 'json_key (?P<value> as_time )'),

        # E.g.: Juvenile
        VOCAB.producer(convert, '(?P<value> intrinsic )'),

        # E.g.: 1st year
        VOCAB.producer(convert, '(?P<value> as_time )'),
    ],
)
