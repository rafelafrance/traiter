"""Mix-in for building parser rules."""

from lib.parsers.regexp import Regexp


class RuleBuilerMixin:
    """Mix-in for building parser rules."""

    def shared_token(self, shared):
        """Build a regular expression with a named group."""
        name = shared[0]
        self.regexps[name] = Regexp(
            phase='token', name=name,
            regexp=f'(?P<{name}> {shared[1]} )')

    def lit(self, name, regexp):
        """Build a regular expression with a named group."""
        self.regexps[name] = Regexp(
            phase='token', name=name,
            regexp=f'(?P<{name}> {regexp} )')

    def kwd(self, name, regexp):
        r"""Wrap a regular expression in \b character class."""
        self.regexps[name] = Regexp(
            phase='token', name=name,
            regexp=fr'\b (?P<{name}> {regexp} ) \b')

    def replace(self, name, regexp):
        """Build a replacer regular expression."""
        self.regexps[name] = Regexp(
            phase='replace', name=name,
            regexp=f'(?P<{name}> {regexp} )')

    def product(self, func, regexp):
        """Build a replacer regular expression."""
        name = f'product_{len(self.regexps) + 1}'
        self.regexps[name] = Regexp(
            phase='product', name=name, func=func,
            regexp=f'(?P<{name}> {regexp} )')
