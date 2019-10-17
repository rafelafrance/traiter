"""Parse life stage notations."""

from stacked_regex.rule import fragment, keyword, producer, replacer
from pylib.parsers.base import Base, convert
from pylib.shared_patterns import SHARED


TIME_OPTIONS = SHARED['time_units'].pattern

LIFE_STAGE = Base(
    scanners=[
        # JSON keys for life stage
        keyword('json_key', [
            r' life \s* stage \s* (remarks?)? ',
            r' age \s* class ',
            r' age \s* in \s* (?P<time_units> {}) '.format(TIME_OPTIONS),
            r' age ']),

        # These words are life stages without a keyword indicator
        keyword('intrinsic', [
            r' yolk \s? sac ',
            r' young [\s-]? of [\s-]? the [\s-]? year ',
            r' adult \s* young ',
            r' young \s* adult ']
                     + """
                ads? adulte?s?
                chicks?
                fledgelings? fleglings?
                fry
                hatched hatchlings?
                imagos?
                imms? immatures?
                jeunes? juvs? juveniles? juvéniles?
                larvae? larvals? larves?
                leptocephales? leptocephalus
                matures? metamorphs?
                neonates?
                nestlings?
                nulliparous
                premetamorphs?
                sub-adults? subads? subadulte?s?
                tadpoles?
                têtard
                yearlings?
                yg ygs young
            """.split()),

        # This indicates that the following words are NOT a life stage
        keyword('skip', r' determin \w* '),

        # Compound words separated by dashes or slashes
        # E.g. adult/juvenile or over-winter
        fragment('joiner', r' \s* [/-] \s* '),

        # Use this to find the end of a life stage pattern
        fragment('separator', r' [;,"?] | $ '),

        # For life stages with numbers as words in them
        SHARED['ordinals'],

        SHARED['time_units'],

        fragment('after', 'after'),
        fragment('hatching', 'hatching'),

        # Match any word
        fragment('word', r' \b \w [\w?./-]* (?! [./-] ) '),
    ],

    replacers=[
        replacer('as_time', '( after )? (ordinals | hatching) time_units'),
    ],

    producers=[
        # E.g.: life stage juvenile/yearling
        producer(
            convert,
            'json_key (?P<value> ( intrinsic | word ) joiner intrinsic )'),

        # E.g.: life stage young adult
        producer(
            convert, 'json_key (?P<value> ( intrinsic | word ) intrinsic )'),

        # E.g.: life stage yearling
        producer(convert, 'json_key (?P<value> intrinsic )'),

        # A sequence of words bracketed by a keyword and a separator
        # E.g.: LifeStage Remarks: 5-6 wks;
        producer(
            convert,
            """ json_key (?P<value> ( intrinsic | word | joiner ){1,5} ) 
            separator"""),

        # E.g.: LifeStage = 1st month
        producer(convert, 'json_key (?P<value> as_time )'),

        # E.g.: Juvenile
        producer(convert, '(?P<value> intrinsic )'),

        # E.g.: 1st year
        producer(convert, '(?P<value> as_time )'),
    ],
)
