"""Parse embryo counts."""

from lib.numeric_trait import NumericTrait
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
import lib.shared_tokens as tkn
import lib.shared_repoduction_tokens as r_tkn


class EmbryoCountTraitBuilder(NumericTraitBuilder):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_replace_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        """Define the tokens."""
        self.shared_token(r_tkn.embryo)
        self.shared_token(r_tkn.and_)
        self.shared_token(r_tkn.size)
        self.shared_token(r_tkn.fat)
        self.shared_token(tkn.len_units)

        self.keyword('conj', ' or '.split())
        self.keyword('prep', ' on '.split())

        self.fragment('integer', r""" \d+ """)

        self.keyword('none', r""" no | none """)

        # The sides like: 3L or 4Right
        self.fragment('side', r""" ( left | right | [lr] ) """)

        # The sexes like: 3M or 4Females
        self.fragment('sex', r""" ( males? | females? | [mf] ) """)

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

    @staticmethod
    def should_skip(data, trait):
        """Check if this record should be skipped because of other fields."""
        if not data['sex'] or data['sex'][0].value != 'male':
            return False
        if data[trait]:
            data[trait].skipped = "Skipped because sex is 'male'"
        return True
