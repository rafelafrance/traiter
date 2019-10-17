"""Parse embryo counts."""

from stacked_regex.rule import fragment, keyword, producer, replacer
from pylib.parsers.base import Base
from pylib.numeric_trait import NumericTrait
from pylib.shared_patterns import SHARED
from pylib.shared_reproductive_patterns import REPRODUCTIVE


def convert(token):
    """Convert parsed tokens into a result."""
    trait = NumericTrait(start=token.start, end=token.end)

    # If a total embryo count is given
    if token.groups.get('total'):
        trait.value = trait.to_int(token.groups['total'])

    # If no total embryo count add the left & right embryo counts
    elif token.groups.get('count1'):
        trait.value = trait.to_int(token.groups['count1'])
        if token.groups.get('count2'):
            trait.value += trait.to_int(token.groups['count2'])

    # If no total embryo count add the male & female embryo counts
    elif token.groups.get('sex1'):
        trait.value = trait.to_int(token.groups['count1'])
        if token.groups.get('count2'):
            trait.value += trait.to_int(token.groups['count2'])

    if trait.value > 1000:
        return None

    # Add embryo side count
    side = token.groups.get('side1', '').lower()
    if side:
        side = 'left' if side.startswith('l') else 'right'
        setattr(trait, side, trait.to_int(token.groups['count1']))

    # Add embryo side count
    side = token.groups.get('side2', '').lower()
    if side:
        side = 'left' if side.startswith('l') else 'right'
        setattr(trait, side, trait.to_int(token.groups['count2']))

    # Add embryo sex count
    sex = token.groups.get('sex1', '').lower()
    if sex:
        sex = 'male' if sex.startswith('m') else 'female'
        setattr(trait, sex, trait.to_int(token.groups['count1']))

    # Add embryo sex count
    sex = token.groups.get('sex2', '').lower()
    if sex:
        sex = 'male' if sex.startswith('m') else 'female'
        setattr(trait, sex, trait.to_int(token.groups['count2']))

    return trait


EMBRYO_COUNT = Base(
    scanners=[
        SHARED['uuid'],  # UUIDs cause problems with shorthand
        REPRODUCTIVE['embryo'],
        REPRODUCTIVE['and'],
        REPRODUCTIVE['size'],
        REPRODUCTIVE['fat'],
        SHARED['len_units'],
        SHARED['integer'],
        REPRODUCTIVE['side'],
        REPRODUCTIVE['none'],

        keyword('conj', ' or '),
        keyword('prep', ' on '),

        # The sexes like: 3M or 4Females
        fragment('sex', r""" males? | females? | [mf] (?! [a-z] ) """),

        REPRODUCTIVE['sep'],

        # Skip arbitrary words
        fragment('word', r' \w+ '),
    ],

    replacers=[
        replacer('count', ' none word conj | integer | none '),
    ],

    producers=[
        # Eg: 4 fetuses on left, 1 on right
        producer(convert, [
            """ (?P<count1> count ) embryo prep (?P<side1> side )
                (?P<count2> count ) (embryo)? (prep)? (?P<side2> side )"""]),

        # Eg: 5 emb 2L 3R
        producer(convert, [
            """ ( (?P<total> count) (size)? )? embryo
                (word | len_units | count ){0,3}
                (?P<count1> count ) (?P<side1> side )
                ((and)? (?P<count2> count ) (?P<side2> side ))?"""]),

        # Eg: 5 emb 2 males 3 females
        producer(convert, [
            """ ( (?P<total> count) (size)? )? embryo
                (word | len_units | count ){0,3}
                (?P<count1> count ) (?P<sex1> sex )
                ((and)? (?P<count2> count ) (?P<sex2> sex ))?"""]),

        # Eg: 5 embryos
        producer(convert, """ (?P<total> count) (size)? embryo """),
    ],
)
