"""Class to hold token data."""


# pylint: disable=global-statement
TOKEN_WIDTH = 4  # Token width from 001_ to 999_
TOKEN_COUNT = 0


class Token:
    """Token data."""

    hide = tuple()

    # pylint: disable=too-many-arguments
    def __init__(self, token=None, name=None, groups=None, start=0, end=0):
        """Build a token."""
        self.token = token
        self.name = name
        self.start = start
        self.end = end
        self.groups = groups if groups else {}

    def as_dict(self):
        """Remove hidden attributes from __dict__."""
        return {k: v for k, v in self.__dict__.items() if k not in self.hide}

    def __repr__(self):
        """Represent the result."""
        return '{}({})'.format(self.__class__.__name__, self.as_dict())

    def __eq__(self, other):
        """Compare traits."""
        return self.as_dict() == other.as_dict()

    @staticmethod
    def build_token():
        """Build a token for a expression."""
        global TOKEN_COUNT
        TOKEN_COUNT += 1
        return f'{TOKEN_COUNT}'.zfill(TOKEN_WIDTH - 1) + '_'

    @staticmethod
    def merge_token_groups(text, token_list, match, regexp):
        """Combine the token groups from a sequence of tokens."""
        groups = {}
        if not match.lastgroup:
            return groups
        for new_name, old_name in regexp.groups:
            if match.group(new_name):
                start = match.start(new_name) // TOKEN_WIDTH
                end = match.end(new_name) // TOKEN_WIDTH
                name = old_name
                groups[name] = text[
                    token_list[start].start:token_list[end-1].end]
        start = match.start() // TOKEN_WIDTH
        end = match.end() // TOKEN_WIDTH
        for token in token_list[start:end]:
            groups = {**groups, **token.groups}
        return groups
