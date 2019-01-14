"""Parse sex notations."""

import re
from pyparsing import Word, alphanums, FollowedBy
from pyparsing import CaselessKeyword as kwd
from lib.base_trait import BaseTrait
from lib.parsed_trait import ParsedTrait
import lib.shared_trait_patterns as stp


class Sex(BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        keyword = kwd('sex')

        sex = (kwd('females') | kwd('female')
               | kwd('males') | kwd('male'))
        sex_q = sex + Word('?')

        # These are words that indicate that "sex" is not a key
        skip = kwd('and') | kwd('is') | kwd('was')

        parser = (
            (keyword + sex_q('value'))
            | (keyword + sex('value'))
            | (keyword + ~FollowedBy(skip) + Word(alphanums)('value'))
            | sex_q('value')
            | sex('value')
        )

        parser.ignore(Word(stp.punct, excludeChars='.;?'))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        result = ParsedTrait()
        result.vocabulary_value(match[0].value)
        result.value = re.sub(r'\s*\?$', '?', result.value)
        result.value = re.sub(r'^(f\w*)', r'female', result.value)
        result.value = re.sub(r'^(m\w*)', r'male', result.value)
        result.ends(match[1], match[2])
        return result
