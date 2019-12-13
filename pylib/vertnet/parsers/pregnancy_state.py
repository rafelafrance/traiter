"""Parse pregnancy state notations."""

from pylib.stacked_regex.rule import part, term, producer
from pylib.vertnet.parsers.base import Base, convert
from pylib.vertnet.shared_reproductive_patterns import RULE


PREGNANCY_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        RULE['none'],

        term('pregnant', r"""
            prega?n?ant pregnan preg pregnancy pregnancies
            gravid multiparous nulliparous parous """.split()),

        term('joiner', r""" of were """.split()),

        term('recent', r"""
            recently recent was previously prev """.split()),

        term('probably', r"""
            probably prob possibly possible
            appears? very
            visible visibly
            evidence evident
            """.split()),

        term('stage', r' early late mid '.split()),

        part('quest', '[?]'),

        part('separator', r' [;,"] '),

        # Skip arbitrary words
        part('word', r' [a-z]\w+ '),

        # E.g.: pregnancy visible
        producer(convert, [
            """(?P<value> pregnant joiner? none? probably quest? )"""]),

        # E.g.: Probably early pregnancy
        producer(convert, [
            """(?P<value> none? (recent | probably)?
            stage? (none | joiner)? pregnant quest? )"""]),
    ],
)
