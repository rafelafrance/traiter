"""Parse embryo counts."""

from lib.numeric_trait import NumericTrait
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
from lib.trait_builders.reproductive_trait_builder import FemaleTraitBuilder
from lib.shared_patterns import SharedPatterns
from lib.shared_reproductive_patterns import ReproductivePatterns


class EmbryoCountTraitBuilder(NumericTraitBuilder, FemaleTraitBuilder):
    """Parser logic."""

    def build_token_rules(self):
        """Define the tokens."""
        r_tkn = ReproductivePatterns()
        tkn = SharedPatterns()

        self.copy(tkn['uuid'])  # UUIDs cause problems with shorthand
        self.copy(r_tkn['embryo'])
        self.copy(r_tkn['and'])
        self.copy(r_tkn['size'])
        self.copy(r_tkn['fat'])
        self.copy(tkn['len_units'])
        self.copy(tkn['integer'])
        self.copy(r_tkn['side'])
        self.copy(r_tkn['none'])

        self.keyword('conj', ' or '.split())
        self.keyword('prep', ' on '.split())

        # The sexes like: 3M or 4Females
        self.fragment('sex', r""" males? | females? | [mf] (?! [a-z] ) """)

        self.copy(r_tkn['sep'])

        # Skip arbitrary words
        self.fragment('word', r' \w+ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('count', ' none word conj | integer | none ')

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [
            # Eg: 4 fetuses on left, 1 on right
            """ (?P<count1> count ) embryo prep (?P<side1> side )
                (?P<count2> count ) (embryo)? (prep)? (?P<side2> side )""",

            # Eg: 5 emb 2L 3R
            """ ( (?P<total> count) (size)? )? embryo
                (word | len_units | count ){0,3}
                (?P<count1> count ) (?P<side1> side )
                ((and)? (?P<count2> count ) (?P<side2> side ))?""",

            # Eg: 5 emb 2 males 3 females
            """ ( (?P<total> count) (size)? )? embryo
                (word | len_units | count ){0,3}
                (?P<count1> count ) (?P<sex1> sex )
                ((and)? (?P<count2> count ) (?P<sex2> sex ))?""",

            # Eg: 5 embryos
            """ (?P<total> count) (size)? embryo """,
        ])

    @staticmethod
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
