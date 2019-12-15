"""Parse pregnancy state notations."""

from pylib.stacked_regex.rule_catalog import RuleCatalog
from pylib.vertnet.parsers.base import Base, convert
import pylib.vertnet.shared_reproductive_patterns as patterns


CATALOG = RuleCatalog(patterns.CATALOG)


PREGNANCY_STATE = Base(
    name=__name__.split('.')[-1],
    rules=[
        CATALOG.term('pregnant', r"""
            prega?n?ant pregnan preg pregnancy pregnancies
            gravid multiparous nulliparous parous """.split()),

        CATALOG.term('joiner', r""" of were """.split()),

        CATALOG.term('recent', r"""
            recently recent was previously prev """.split()),

        CATALOG.term('probably', r"""
            probably prob possibly possible
            appears? very
            visible visibly
            evidence evident
            """.split()),

        CATALOG.term('stage', r' early late mid '.split()),

        CATALOG.part('separator', r' [;,"] '),

        # E.g.: pregnancy visible
        CATALOG.producer(convert, [
            """(?P<value> pregnant joiner? none? probably quest? )"""]),

        # E.g.: Probably early pregnancy
        CATALOG.producer(convert, [
            """(?P<value> none? (recent | probably)?
            stage? (none | joiner)? pregnant quest? )"""]),
        ],
)
