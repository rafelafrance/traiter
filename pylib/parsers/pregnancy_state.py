"""Parse pregnancy state notations."""

from stacked_regex.rule import fragment, keyword, producer
from pylib.parsers.base import Base, convert
from pylib.shared_reproductive_patterns import REPRODUCTIVE


PREGNANCY_STATE = Base(
    name=__name__.split('.')[-1],
    scanners=[
        REPRODUCTIVE['none'],

        keyword('pregnant', r"""
            prega?n?ant pregnan preg pregnancy pregnancies
            gravid multiparous nulliparous parous """.split()),

        keyword('joiner', r""" of were """.split()),

        keyword('recent', r"""
            recently recent was previously prev """.split()),

        keyword('probably', r"""
            probably prob possibly possible
            appears? very
            visible visibly
            evidence evident
            """.split()),

        keyword('stage', r' early late mid '.split()),

        fragment('quest', '[?]'),

        fragment('separator', r' [;,"] '),

        # Skip arbitrary words
        fragment('word', r' [a-z]\w+ '),
    ],

    replacers=[],

    producers=[
        # E.g.: pregnancy visible
        producer(convert, [
            """(?P<value> pregnant joiner? none? probably quest? )"""]),

        # E.g.: Probably early pregnancy
        producer(convert, [
            """(?P<value> none? (recent | probably)?
            stage? (none | joiner)? pregnant quest? )"""]),
    ],
)
