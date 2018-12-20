"""Parse the notations."""

# pylint: disable=too-few-public-methods

from lib.lexers.lex_body_mass import LexBodyMass
from lib.parsers.parse_base import ParseBase, Action
import lib.parsers.shared_reducers as reduce


class ParseBodyMass(ParseBase):
    """Parser logic."""

    def __init__(self):
        """Initialize the parser."""
        super().__init__(LexBodyMass)

    def rule_dict(self):
        """Return the parser rules."""
        return {
            'shorthand_mass': Action(
                reduce=reduce.shorthand_mass, args={'value': 0}),
            'shorthand_key shorthand_mass': Action(
                reduce=reduce.shorthand_mass, args={'value': 1}),

        }
