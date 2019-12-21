"""Parse life stage notations."""

from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.parsers.base import Base, convert
import pylib.vertnet.shared_patterns as patterns


CATALOG = RuleCatalog(patterns.CATALOG)


TIME_OPTIONS = CATALOG['time_units'].pattern

LIFE_STAGE = Base(
    name=__name__.split('.')[-1],
    rules=[
        # JSON keys for life stage
        CATALOG.term('json_key', [
            r' life \s* stage \s* (remarks?)? ',
            r' age \s* class ',
            r' age \s* in \s* (?P<time_units> {}) '.format(TIME_OPTIONS),
            r' age ']),

        # These words are life stages without a keyword indicator
        CATALOG.term('intrinsic', [
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
        CATALOG.term('skip', r' determin \w* '),

        # Compound words separated by dashes or slashes
        # E.g. adult/juvenile or over-winter
        CATALOG.part('joiner', r' \s* [/-] \s* '),

        # Use this to find the end of a life stage pattern
        CATALOG.part('separator', r' [;,"?] | $ '),

        # For life stages with numbers as words in them
        CATALOG['ordinals'],

        CATALOG['time_units'],

        CATALOG.part('after', 'after'),
        CATALOG.part('hatching', 'hatching'),

        # Match any word
        CATALOG.part('word', r' \b \w [\w?.-]* (?! [./-] ) '),

        CATALOG.grouper('as_time', ' after? (ordinals | hatching) time_units'),

        # E.g.: life stage juvenile/yearling
        CATALOG.producer(
            convert,
            'json_key (?P<value> ( intrinsic | word ) joiner intrinsic )'),

        # E.g.: life stage young adult
        CATALOG.producer(
            convert, 'json_key (?P<value> ( intrinsic | word ) intrinsic )'),

        # E.g.: life stage yearling
        CATALOG.producer(convert, 'json_key (?P<value> intrinsic )'),

        # A sequence of words bracketed by a keyword and a separator
        # E.g.: LifeStage Remarks: 5-6 wks;
        CATALOG.producer(
            convert,
            """ json_key (?P<value> ( intrinsic | word | joiner ){1,5} )
            separator """),

        # E.g.: LifeStage = 1st month
        CATALOG.producer(convert, 'json_key (?P<value> as_time )'),

        # E.g.: Juvenile
        CATALOG.producer(convert, '(?P<value> intrinsic )'),

        # E.g.: 1st year
        CATALOG.producer(convert, '(?P<value> as_time )'),
    ],
)
