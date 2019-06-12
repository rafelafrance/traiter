"""Parse testes state notations."""

from traiter.trait import Trait
from traiter.trait_builders.base_trait_builder import BaseTraitBuilder


class OvariesStateTraitBuilder(BaseTraitBuilder):
    """Parser logic."""

    def __init__(self, args=None):
        """Build the trait parser."""
        super().__init__(args)

        self.build_token_rules()
        self.build_replace_rules()
        self.build_product_rules()

        self.compile_regex()

    def build_token_rules(self):
        # self.keyword('label', r' reproductive .? (data |state | condition) ')
        self.fragment('ovary', r' (ovaries | ovary s? ) \b ')

        self.keyword('size', r"""
            (enlarged | enlarge | large
                | small
                | moderate | mod
            ) ( \s+ size d? )?
            """)
        self.keyword('uterus', r' uterus | uterine ')
        self.keyword('fallopian', r' fallopian \s* ( tubes? )? ')
        self.keyword('immature', r' immature | mature ')
        self.keyword('horns', r' horns? ')
        self.keyword('covered', r' covered ')
        self.keyword('fat', r' fat ')
        self.keyword('corpus', r' corpus | corpora | corp | cor | c ')
        self.keyword('alb', r' albicans | alb ')
        self.keyword('lut', r' luteum | lute | lut ')
        self.keyword('side', r' (?P<side> both | left | right | [lr]) ')
        self.keyword('color', r' ( dark | light | pale )? \s* (red | pink) ')

        self.fragment('sign', r' \+ | \- ')
        self.fragment('and', r' and | & ')
        self.fragment('word', r' [a-z]+ ')

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('ovaries', r"""
            ovary ( ( ( and )? uterus ( horns )? )
                    | ( and )? fallopian )?""")
        self.replace('coverage', r' covered (word){0,2} fat ')
        self.replace('luteum', r' ( sign )? ( corpus )? (alb | lut) ')

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.double, r"""
            ovaries (?P<side1> side) (?P<value1> ( word )? luteum)
                (?P<side2> side) (?P<value2> ( word )? luteum)
            """)

        self.product(
            self.convert, r"""
            side ovaries (word){0,3} (?P<value> color)
            | ovaries (?P<value> ( size ) ( immature )? )
            | ovaries (?P<value> ( size )? ( immature ) )
            | ovaries (?P<value> coverage)
            | ovaries (?P<value> color)
            | (?P<value> luteum) ( side )? ovaries
            | ovaries ( side )? luteum
            """)

    @staticmethod
    def convert(token):
        """Convert parsed token into a trait product."""
        trait = Trait(
            value=token.groups['value'].lower(),
            start=token.start,
            end=token.end)
        trait.is_flag_in_token('ambiguous_key', token)
        trait.is_value_in_token('side', token)
        return trait

    @staticmethod
    def double(token):
        """Convert a single token into multiple (two) trait_builders."""
        trait1 = Trait(
            value=token.groups['value1'].lower(),
            side=token.groups['side1'].lower(),
            start=token.start,
            end=token.end)
        trait2 = Trait(
            value=token.groups['value2'].lower(),
            side=token.groups['side2'].lower(),
            start=token.start,
            end=token.end)
        return [trait1, trait2]
