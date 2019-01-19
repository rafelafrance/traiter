"""Tokenize the notations."""

import re
from typing import Dict, Pattern, Callable
from dataclasses import dataclass, field as datafield


@dataclass
class Token:
    """Token data."""

    token: str = None
    name: str = None
    groups: Dict = datafield(default_factory={})
    start: int = 0
    end: int = 0


@dataclass
class Regexp:
    """Regular expression data."""

    type: str = None
    name: str = None
    token: str = None
    regexp: Pattern = None
    func: Callable = None


class Base:  # pylint: disable=too-many-instance-attributes
    """Shared lexer logic."""

    flags = re.VERBOSE | re.IGNORECASE

    # get all group names from a regex
    groups_rx = re.compile(r""" \( \? P< ( \w+ ) > """, flags)
    back_ref_rx = re.compile(r""" \( \? P= ( \w+ ) \) """, flags)
    # Get words that are not group names
    token_rx = re.compile(
        r""" (?<! [?\\a-z] ) (?<! < \s )(?<! < )
             ( \b [a-z]\w* \b )
             (?! \s* > | [a-z] )
        """, flags)

    width = 4   # Token width from 001_ to 999_

    def __init__(self, args=None):
        """Build the trait parser."""
        self.args = args
        self.regexps = []       # Token types
        self.regexp = {}        # Get at the regexp via its name
        self.groups = {}        # Use this so we can quickly find regex groups
        self.tokenizer = None   # Regular expression for creating tokens
        self.replacer = None    # Regular expression for replacing tokens
        self.producer = None    # Regular expression for producing traits
        self.used_groups = set()  # Used to rename groups

    def finish_init(self):
        """Finish initialization."""
        for regexp in self.regexps:
            if regexp.type != 'token':
                regexp.regexp = self.tokenize_regex(regexp)

        self.tokenizer = re.compile(
            ' | '.join([x.regexp for x in self.regexps
                        if x.type == 'token']),
            self.flags)
        self.replacer = re.compile(
            ' | '.join([x.regexp for x in self.regexps
                        if x.type == 'replace']),
            self.flags)
        self.producer = re.compile(
            ' | '.join([x.regexp for x in self.regexps
                        if x.type == 'product']),
            self.flags)

    def parse(self, text, field=None, as_dict=False):
        """Find the traits in the text."""
        token_list = self.tokenize(text)
        want_replace = bool(self.replacer.pattern)
        while want_replace:
            (token_list, want_replace) = self.replace_tokens(token_list, text)
        traits = self.tokens_to_traits(token_list, text, field, as_dict)
        return traits

    def tokenize(self, text):
        """Split the text into a token list."""
        token_list = []
        for match in self.tokenizer.finditer(text):
            name = match.lastgroup
            groups = {self.group_name(x): text[match.start(x):match.end(x)]
                      for x in self.groups[name] if match.group(x)}
            token_list.append(Token(
                token=self.regexp[name].token,
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
            start = match.start() // self.width
            end = match.end() // self.width
            token = Token(
                token=self.regexp[name].token,
                name=name,
                groups=self.merge_token_groups(text, token_list, match),
                start=token_list[start].start,
                end=token_list[end-1].end)
            token_list[start:end] = [token]
        return (token_list, want_replace)

    def tokens_to_traits(self, token_list, text, field=None, as_dict=False):
        """Produce the final results from the remaining tokens."""
        traits = []
        token_text = ''.join([t.token for t in token_list])
        for match in self.producer.finditer(token_text):
            name = match.lastgroup
            start = match.start() // self.width
            end = match.end() // self.width
            token = Token(
                token=name,
                name=name,
                groups=self.merge_token_groups(text, token_list, match),
                start=token_list[start].start,
                end=token_list[end-1].end)
            trait = self.regexp[name].func(token)
            if trait:   # The function can still return a null & fail
                trait = self.fix_up_trait(trait, text)
                if trait:
                    trait.field = field
                    if as_dict:
                        trait = trait.as_dict()
                    traits.append(trait)
        return traits

    # pylint: disable=unused-argument,no-self-use
    def fix_up_trait(self, trait, text):
        """Fix problematic parses."""
        return trait

    def merge_token_groups(self, text, token_list, match):
        """Combine the token groups from a sequence of tokens."""
        groups = {}
        if not match.lastgroup:
            return groups
        for group in self.groups[match.lastgroup]:
            if match.group(group):
                start = match.start(group) // self.width
                end = match.end(group) // self.width
                name = self.group_name(group)
                groups[name] = text[
                    token_list[start].start:token_list[end-1].end]
        start = match.start() // self.width
        end = match.end() // self.width
        for token in token_list[start:end]:
            groups = {**groups, **token.groups}
        return groups

    def tokenize_regex(self, regexp):
        """Replace names in regex with their tokens."""
        matches = list(self.token_rx.finditer(regexp.regexp))
        for match in reversed(matches):
            token = self.regexp[match.group(1)].token
            start = regexp.regexp[:match.start(1)]
            end = regexp.regexp[match.end(1):]
            regexp.regexp = start + token + end
        return ' '.join(regexp.regexp.split())

    @staticmethod
    def group_name(group):
        """Strip the unique suffix off of the group name."""
        return re.sub(r'_\d+$', '', group)

    def adjust_group_names(self, regexp):
        """Make sure all group names are unique & handle back references."""
        # Rename group names
        back_refs = {}
        matches = list(self.groups_rx.finditer(regexp.regexp))[1:]
        for match in reversed(matches):
            group = match.group(1)
            i = 0
            while True:
                i += 1
                name = f'{group}_{i}'
                if name not in self.used_groups:
                    break
            self.used_groups.add(name)
            start = regexp.regexp[:match.start(1)]
            end = regexp.regexp[match.end(1):]
            regexp.regexp = start + name + end
            back_refs[group] = name

        # Now rename back references
        matches = list(self.back_ref_rx.finditer(regexp.regexp))
        for match in reversed(matches):
            name = back_refs[match.group(1)]
            start = regexp.regexp[:match.start(1)]
            end = regexp.regexp[match.end(1):]
            regexp.regexp = start + name + end

        return regexp.regexp

    def add_regex(self, regexp):
        """Update regex to make it unique & put add it."""
        regexp.token = f'{len(self.regexps) + 1}'.zfill(self.width - 1) + '_'
        regexp.regexp = ' '.join(self.adjust_group_names(regexp).split())
        self.groups[regexp.name] = self.groups_rx.findall(regexp.regexp)
        self.regexp[regexp.name] = regexp
        self.regexps.append(regexp)

    def shared_token(self, shared):
        """Build a regular expression with a named group."""
        self.add_regex(Regexp(
            type='token', name=shared[0],
            regexp=f'(?P<{shared[0]}> {shared[1]} )'))

    def lit(self, name, regexp):
        """Build a regular expression with a named group."""
        self.add_regex(Regexp(
            type='token', name=name,
            regexp=f'(?P<{name}> {regexp} )'))

    def kwd(self, name, regexp):
        r"""Wrap a regular expression in \b character class."""
        self.add_regex(Regexp(
            type='token', name=name,
            regexp=fr'\b (?P<{name}> {regexp} ) \b'))

    def replace(self, name, regexp):
        """Build a replacer regular expression."""
        self.add_regex(Regexp(
            type='replace', name=name,
            regexp=f'(?P<{name}> {regexp} )'))

    def product(self, func, regexp):
        """Build a replacer regular expression."""
        name = f'product_{len(self.regexps) + 1}'
        self.add_regex(Regexp(
            type='product', name=name, func=func,
            regexp=f'(?P<{name}> {regexp} )'))
