"""Parse lactation state notations."""

from lib.numeric_trait import NumericTrait
from lib.trait_builders.numeric_trait_builder import NumericTraitBuilder
from lib.shared_tokens import SharedTokens
from lib.shared_repoduction_tokens import ReproductiveTokens


class NippleCountTraitBuilder(NumericTraitBuilder):
    """Parser logic."""

    def build_token_rules(self):
        """Define the tokens."""
        tkn = SharedTokens()
        r_tkn = ReproductiveTokens()

        self.copy(tkn['uuid'])  # UUIDs cause problems with numbers

        self.keyword('id', r' \d+-\d+ ')

        self.copy(r_tkn['nipple'])
        self.copy(tkn['integer'])
        self.copy(r_tkn['visible'])
        self.copy(r_tkn['none'])
        self.copy(r_tkn['op'])
        self.copy(r_tkn['eq'])

        self.keyword('adj', r"""
            inguinal ing pectoral pec pr """.split())

        self.fragment('number', r' number | no | [#] ')
        self.fragment('eq', r' is | eq | equals? | [=] ')

        # Skip arbitrary words
        self.fragment('word', r' \w+ ')

        self.copy(r_tkn['sep'])

    def build_replace_rules(self):
        """Define rules for token simplification."""
        self.replace('count', ' integer | none ')

        self.replace('modifier', 'adj visible'.split())

        self.replace('skip', ' number (eq)? integer ')

    def build_product_rules(self):
        """Define rules for output."""
        self.product(self.typed, [
            """ (?P<notation>
                    (?P<value1> count) modifier
                    (?P<value2> count) modifier
                ) nipple """,
        ])

        self.product(self.convert, [

            # Eg: 1:2 = 6 mammae
            """ nipple (op)?
                (?P<notation> count (modifier)?
                    (op)? count (modifier)?
                    ((eq) (?P<value> count))? ) """,

            # Eg: 1:2 = 6 mammae
            """ (?P<notation> count (modifier)? (op)? count (modifier)?
                ((eq) (?P<value> count))? ) nipple """,

            # Eg: 6 mammae
            """ (?P<value> count ) (modifier)? nipple """,

            # Eg: nipples 5
            """ nipple (?P<value> count ) """,
        ])

    @staticmethod
    def convert(token):
        """Convert single value tokens into a result."""
        value = token.groups.get('value')

        if not value:
            return None

        trait = NumericTrait(start=token.start, end=token.end)
        trait.value = trait.to_int(value)

        if trait.value > 100:
            return None

        if token.groups.get('notation'):
            trait.notation = token.groups['notation']

        return trait

    @staticmethod
    def typed(token):
        """Convert single value tokens into a result."""
        trait = NumericTrait(start=token.start, end=token.end)
        trait.notation = token.groups['notation']
        trait.value = trait.to_int(token.groups['value1'])
        trait.value += trait.to_int(token.groups.get('value2'))
        return trait

    @staticmethod
    def should_skip(data, trait):
        """Check if this record should be skipped because of other fields."""
        if not data['sex'] or data['sex'][0].value != 'male':
            return False
        if data[trait]:
            data[trait].skipped = "Skipped because sex is 'male'"
        return True
