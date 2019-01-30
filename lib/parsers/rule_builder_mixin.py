"""Mix-in for building parser rules."""

import re
from lib.parsers.regexp import Regexp


class RuleBuilerMixin:
    """Mix-in for building parser rules."""

    flags = re.VERBOSE | re.IGNORECASE

    # get all group names from a regex
    groups_rx = re.compile(r""" \( \? P< ( \w+ ) > """, flags)
    back_ref_rx = re.compile(r""" \( \? P= ( \w+ ) \) """, flags)

    def __init__(self):
        """Build the trait parser."""
        self.tie_breaker = 0

    def adjust_group_names(self, regexp):
        """Make sure all group names are unique & handle back references."""
        regexp, back_refs = self.rename_group_names(regexp)
        regexp = self.rename_back_references(regexp, back_refs)
        return regexp.regexp

    def rename_group_names(self, regexp):
        """Make regular expression group names unique."""
        self.renamed_group[regexp.name] = regexp.name
        back_refs = {}
        matches = list(self.groups_rx.finditer(regexp.regexp))[1:]
        for match in reversed(matches):
            group = match.group(1)
            self.tie_breaker += 1
            name = f'{group}_{self.tie_breaker}'
            self.renamed_group[name] = group
            start = regexp.regexp[:match.start(1)]
            end = regexp.regexp[match.end(1):]
            regexp.regexp = start + name + end
            back_refs[group] = name
        return regexp, back_refs

    def rename_back_references(self, regexp, back_refs):
        """Link back references to the renamed regular expression group."""
        matches = list(self.back_ref_rx.finditer(regexp.regexp))
        for match in reversed(matches):
            name = back_refs[match.group(1)]
            start = regexp.regexp[:match.start(1)]
            end = regexp.regexp[match.end(1):]
            regexp.regexp = start + name + end
        return regexp

    def add_regex(self, regexp):
        """Update regex to make it unique & put add it."""
        regexp.token = f'{len(self.regexps) + 1}'.zfill(self.width - 1) + '_'
        regexp.regexp = ' '.join(self.adjust_group_names(regexp).split())
        self.inner_groups[regexp.name] = self.groups_rx.findall(regexp.regexp)
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
