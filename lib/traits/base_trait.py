"""Common logic for parsing trait notations."""

# pylint: disable=unused-argument,no-self-use

import re
import inflect
from lib.rule_builder_mixin import RuleBuilerMixin
from lib.token import Token, TOKEN_WIDTH


class BaseTrait(RuleBuilerMixin):
    """Shared lexer logic."""

    flags = re.VERBOSE | re.IGNORECASE

    inflector = inflect.engine()

    def __init__(self, args=None):
        """Build the trait parser."""
        self.args = args
        self.regexps = {}        # Get at the regexp via its name
        self.tokenizer = None    # Regular expression for creating tokens
        self.replacer = None     # Regular expression for replacing tokens
        self.producer = None     # Regular expression for producing traits

    def finish_init(self):
        """Finish initialization."""
        for regexp in self.regexps.values():
            regexp.tokenize_regex(self.regexps)

        self.tokenizer = re.compile(
            ' | '.join([x.regexp for x in self.regexps.values()
                        if x.phase == 'token']),
            self.flags)
        self.replacer = re.compile(
            ' | '.join([x.regexp for x in self.regexps.values()
                        if x.phase == 'replace']),
            self.flags)
        self.producer = re.compile(
            ' | '.join([x.regexp for x in self.regexps.values()
                        if x.phase == 'product']),
            self.flags)

    def parse(self, text, field=None):
        """Find the traits in the text."""
        token_list = self.tokenize(text)
        want_replace = bool(self.replacer.pattern)
        while want_replace:
            (token_list, want_replace) = self.replace_tokens(token_list, text)
        traits = self.tokens_to_traits(token_list, text)
        return traits

    def tokenize(self, text):
        """Split the text into a token list."""
        token_list = []
        for match in self.tokenizer.finditer(text):
            name = match.lastgroup
            groups = {old: text[match.start(new):match.end(new)]
                      for new, old
                      in self.regexps[name].groups if match.group(new)}
            token_list.append(Token(
                token=self.regexps[name].token,
                name=name,
                groups=groups,
                start=match.start(),
                end=match.end()))
        return token_list

    def replace_tokens(self, token_list, text):
        """Replace tokens with token combinations."""
        token_text = ''.join([t.token for t in token_list])
        matches = list(self.replacer.finditer(token_text))
        want_replace = False
        for match in reversed(matches):
            name = match.lastgroup
            want_replace = True
            start = match.start() // TOKEN_WIDTH
            end = match.end() // TOKEN_WIDTH
            token = Token(
                token=self.regexps[name].token,
                name=name,
                groups=Token.merge_token_groups(
                    text, token_list, match, self.regexps[match.lastgroup]),
                start=token_list[start].start,
                end=token_list[end-1].end)
            token_list[start:end] = [token]
        return (token_list, want_replace)

    def tokens_to_traits(self, token_list, text, field=''):
        """Produce the final results from the remaining tokens."""
        # for tkn in token_list:
        #     print(tkn)
        traits = []
        token_text = ''.join([t.token for t in token_list])
        for match in self.producer.finditer(token_text):
            name = match.lastgroup
            start = match.start() // TOKEN_WIDTH
            end = match.end() // TOKEN_WIDTH
            token = Token(
                token=name,
                name=name,
                groups=Token.merge_token_groups(
                    text, token_list, match, self.regexps[match.lastgroup]),
                start=token_list[start].start,
                end=token_list[end-1].end)
            trait = self.regexps[name].func(token)
            if trait:   # The function can return a null & fail
                trait = self.fix_up_trait(trait, text)
                if trait:
                    trait.field = field
                    traits.append(trait)
        return traits

    def fix_up_trait(self, trait, text):
        """Fix problematic parses."""
        return trait

    @staticmethod
    def csv_formater(trait, row, parses):
        """Format the trait for CSV output."""
        values = []
        for parse in parses:
            value = parse.value.lower()
            if value not in values:
                values.append(value)

        for i, value in enumerate(values, 1):
            row[f'{ordinal(i)} {trait} notation'] = value


def ordinal(i):
    """Convert the digit to an ordinal value: 1->1st, 2->2nd, etc."""
    return BaseTrait.inflector.ordinal(i)
