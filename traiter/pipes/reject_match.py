from spacy.tokens import Span
from spacy.util import registry

SKIP_TRAIT_CREATION = "skip_trait_creation"
REJECT_MATCH = "reject_match"


class SkipTraitCreation(Exception):
    """
    Raise this when you want to skip trait creation from a match.

    Sometimes you want to change trait fields based on the surrounding context, but
    you don't want to create a new trait. For instance, I use this to link subparts to
    their parent part. I change the subpart (put a reference to the part in the subpart)
    and skip the trait creation step.
    """


@registry.misc(SKIP_TRAIT_CREATION)
def skip_trait_creation(_: Span) -> None:
    """
    Use this to reject a pattern from doc.ents.

    Sometimes it is easier to search for a pattern that you know you don't want
    rather than writing a bunch of rules to work around a set of bad patterns within
    the normal set of rules.
    """
    raise SkipTraitCreation


class RejectMatch(Exception):
    """
    Raise this when you want to remove a match from doc.ents.

    If you're processing a match, and you discover that it really isn't a trait/entity
    then you'd raise this exception so the match would not be included in the
    document's entities.
    """


@registry.misc(REJECT_MATCH)
def reject_match(_: Span) -> None:
    """
    Use this to reject a pattern from doc.ents.

    Sometimes it is easier to search for a pattern that you know you don't want
    rather than writing a bunch of rules to work around a set of bad patterns within
    the normal set of rules.
    """
    raise RejectMatch
