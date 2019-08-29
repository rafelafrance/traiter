"""Parse placental scar counts."""

from lib.numeric_trait import NumericTrait
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
from lib.shared_tokens import SharedTokens
from lib.shared_repoduction_tokens import ReproductiveTokens


class PlacentalScarCountTraitBuilder(NumericTraitBuilder):
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
        tkn = SharedTokens()
        r_tkn = ReproductiveTokens()

        self.copy(r_tkn['plac_scar'])
        self.copy(tkn['integer'])
        self.copy(r_tkn['side'])
        self.copy(r_tkn['none'])
        self.copy(r_tkn['op'])
        self.copy(r_tkn['eq'])
        self.copy(r_tkn['embryo'])

        # Adjectives to placental scars
        self.keyword('adj', r"""
            faint prominent recent old possible """.split())

        # Conjunction
        self.keyword('conj', ' or '.split())

        # Preposition
        self.keyword('prep', ' on of '.split())

        # Visible
        self.keyword('visible', ' visible definite '.split())

        # Skip arbitrary words
        self.fragment('word', r' \w+ ')

        # Trait separator
        self.fragment('sep', r' [;/] ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('count', """
            none embryo conj
            | none visible | integer | none """)

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.convert_count, [
            """(?P<count1> count ) op (?P<count2> count )
                ( eq (?P<value> count ) )? plac_scar """,

            """plac_scar
                  (?P<count1> count ) (prep)? (?P<side1> side )
                ( (?P<count2> count ) (prep)? (?P<side2> side ) )? """,

            """ (?P<count1> count ) (prep)? (?P<side1> side ) plac_scar
                ( (?P<count2> count ) (prep)? (?P<side2> side )
                    (plac_scar)? )? """,

            """ (?P<side1> side ) (?P<count1> count )
                    (visible | op)? plac_scar
                ( (?P<side2> side ) (?P<count2> count )
                    (visible)? (visible | op)? (plac_scar)? )? """,

            """   (?P<count1> count ) (prep)? (?P<side1> side )
                ( (?P<count2> count ) (prep)? (?P<side2> side ) )?
                plac_scar """,

            """ (?P<count1> count ) plac_scar (?P<side1> side )
                ( (?P<count2> count ) plac_scar (?P<side2> side ) )? """,

            """ plac_scar (?P<side1> side ) (?P<count1> count )
                ( plac_scar (?P<side2> side ) (?P<count2> count ) )? """,

            """plac_scar
                (?P<count1> count )
                  op (?P<count2> count )
                ( eq (?P<value> count ) )? """,

            """ (?P<value> count ) (adj)? plac_scar (op)?
                (
                    (?P<count1> count ) (?P<side1> side )
                    (op)?
                    (?P<count2> count ) (?P<side2> side )
                )?
                """,

            """ (?P<value> count ) (embryo)? plac_scar """,

            """ plac_scar (eq)? (?P<count1> count ) (?P<side1> side ) """,

            """ plac_scar (eq)? (?P<value> count ) """,
        ])

        self.product(self.convert_state, [
            """ plac_scar """
        ])

    @staticmethod
    def convert_count(token):
        """Convert parsed tokens into a result."""
        trait = NumericTrait(start=token.start, end=token.end)

        if token.groups.get('value'):
            trait.value = trait.to_int(token.groups['value'])
        elif token.groups.get('count1'):
            trait.value = trait.to_int(token.groups['count1'])
            trait.value += trait.to_int(token.groups.get('count2', ''))

        # Add scar side count
        side = token.groups.get('side1', '').lower()
        count = token.groups.get('count1', '').lower()
        if side:
            side = 'left' if side.startswith('l') else 'right'
            setattr(trait, side, trait.to_int(count))
        elif count:
            setattr(trait, 'side1', trait.to_int(count))

        # Add scar side count
        side = token.groups.get('side2', '').lower()
        count = token.groups.get('count2', '').lower()
        if side:
            side = 'left' if side.startswith('l') else 'right'
            setattr(trait, side, trait.to_int(count))
        elif count:
            setattr(trait, 'side2', trait.to_int(count))

        return trait

    @staticmethod
    def convert_state(token):
        """Convert parsed tokens into a result."""
        trait = NumericTrait(value='present', start=token.start, end=token.end)
        return trait

    @staticmethod
    def should_skip(data, trait):
        """Check if this record should be skipped because of other fields."""
        if not data['sex'] or data['sex'][0].value != 'male':
            return False
        if data[trait]:
            data[trait].skipped = "Skipped because sex is 'male'"
        return True
