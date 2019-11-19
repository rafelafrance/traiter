"""Parse pregnancy state notations."""

from pylib.stacked_regex.rule import fragment, keyword, producer
from pylib.vertnet.parsers.base import Base, convert
from pylib.vertnet.shared_reproductive_patterns import RULE


PREGNANCY_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        RULE['none'],

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

        # E.g.: pregnancy visible
        producer(convert, [
            """(?P<value> pregnant joiner? none? probably quest? )"""]),

        # E.g.: Probably early pregnancy
        producer(convert, [
            """(?P<value> none? (recent | probably)?
            stage? (none | joiner)? pregnant quest? )"""]),
    ],
)
