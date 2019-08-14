"""Parse embryo counts."""

from lib.numeric_trait import NumericTrait
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
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

        self.fragment('integer', r""" \d+ """)

        self.keyword('none', r""" no | none """)

        # The side comes after the number like: 3L or 4Right
        self.fragment('side_trailing', r""" ( left | right | [lr] ) \b """)

        # Skip arbitrary words
        self.fragment('word', r' [a-z]\w+ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('count', 'integer none'.split())

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert, [
            # Eg: 5 emb 2L 3R
            """ (?P<total> count) embryo
                (?P<count1> count ) (?P<side1> side_trailing ) 
                (?P<count2> count ) (?P<side2> side_trailing )""",

            # Eg: emb 2L 3R
            """ embryo
                (?P<count1> count ) (?P<side1> side_trailing ) 
                (?P<count2> count ) (?P<side2> side_trailing )""",

            # Eg: 2 emb 2L
            """ (?P<total> count) embryo
                (?P<count1> count ) (?P<side1> side_trailing ) """,

            # Eg: 5 embryos
            """ (?P<total> count) embryo """,
        ])

    @staticmethod
    def convert(token):
        """Convert parsed tokens into a result."""
        traits = []

        # A total embryo count is given
        if token.groups.get('total'):
            total = NumericTrait(start=token.start, end=token.end)
            total.value = total.to_int(token.groups['total'])
            traits.append(total)

        # Not total embryo count add the left & right embryo counts
        elif token.groups.get('count1'):
            total = NumericTrait(start=token.start, end=token.end)
            total.value = total.to_int(token.groups['count1'])
            if token.groups.get('count2'):
                total.value += total.to_int(token.groups['count2'])
            traits.append(total)

        # Add embryo side count
        if token.groups.get('count1'):
            side1 = NumericTrait(start=token.start, end=token.end)
            side1.side = token.groups.get('side1')
            side1.value = side1.to_int(token.groups['count1'])
            traits.append(side1)

        # Add embryo side count
        if token.groups.get('count2'):
            side2 = NumericTrait(start=token.start, end=token.end)
            side2.side = token.groups.get('side2')
            side2.value = side2.to_int(token.groups['count2'])
            traits.append(side2)

        return traits[0] if len(traits) == 1 else traits

    @staticmethod
    def should_skip(data, trait):
        """Check if this record should be skipped because of other fields."""
        if not data['sex'] or data['sex'][0].value != 'male':
            return False
        if data[trait]:
            data[trait].skipped = "Skipped because sex is 'male'"
        return True
