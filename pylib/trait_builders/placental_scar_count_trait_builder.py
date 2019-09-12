"""Parse placental scar counts."""

from pylib.numeric_trait import NumericTrait
from pylib.trait_builders.numeric_trait_builder import NumericTraitBuilder
from pylib.trait_builders.reproductive_trait_builder import FemaleTraitBuilder
from pylib.shared_patterns import SharedPatterns
from pylib.shared_reproductive_patterns import ReproductivePatterns


class PlacentalScarCountTraitBuilder(NumericTraitBuilder, FemaleTraitBuilder):
    """Parser logic."""

    def build_token_rules(self):
        """Define the tokens."""
        tkn = SharedPatterns()
        r_tkn = ReproductivePatterns()

        self.copy(tkn['uuid'])  # UUIDs cause problems with numbers
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
