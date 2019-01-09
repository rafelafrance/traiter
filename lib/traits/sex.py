"""Parse sex notations."""

import re
from pyparsing import Word, alphanums, FollowedBy
from lib.base_trait import BaseTrait
from lib.parse_result import ParseResult
import lib.shared_parser_patterns as sp


class Sex(BaseTrait):
    """Parser logic."""

    def build_parser(self):
        """Return the trait parser."""
        keyword = sp.kwd('sex')

        sex = (sp.kwd('females') | sp.kwd('female')
               | sp.kwd('males') | sp.kwd('male'))
        sex_q = sex + Word('?')

        # These are words that indicate that "sex" is not a key
        skip = sp.kwd('and') | sp.kwd('is') | sp.kwd('was')

        parser = (
            (keyword + sex_q('value'))
            | (keyword + sex('value'))
            | (keyword + ~FollowedBy(skip) + Word(alphanums)('value'))
            | sex_q('value')
            | sex('value')
        )

        parser.ignore(Word(sp.punct, excludeChars='.;?'))
        return parser

    def result(self, match):
        """Convert parsed tokens into a result."""
        result = ParseResult()
        result.vocabulary_value(match[0].value)
        result.value = re.sub(r'\s*\?$', '?', result.value)
        result.value = re.sub(r'^(f\w*)', r'female', result.value)
        result.value = re.sub(r'^(m\w*)', r'male', result.value)
        result.ends(match[1], match[2])
        return result
