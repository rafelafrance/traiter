"""Class to hold token regular expression data."""

import re
from lib.token import Token


# pylint: disable=global-statement
GROUP_COUNT = 0


class Regexp:
    """Regular expression data."""

    flags = re.VERBOSE | re.IGNORECASE

    # Get words that are not group names
    token_rx = re.compile(
        r""" (?<! [?\\a-z] ) (?<! < \s )(?<! < )
             ( \b [a-z]\w* \b )
             (?! \s* > | [a-z] )
        """, flags)

    # get all group names from a regex
    groups_rx = re.compile(r""" \( \? P< ( \w+ ) > """, flags)
    back_ref_rx = re.compile(r""" \( \? P= ( \w+ ) \) """, flags)

    # pylint: disable=too-many-arguments
    def __init__(
            self, phase=None, name=None, func=None, regexp=None, token=None):
        """Build a regexp."""
        self.name = name
        self.func = func
        self.phase = phase
        self.token = token
        self.groups = []  # A list of tuples (new_group_name, old_group_name)

        self.token = Token.build_token()

        self.regexp = regexp
        back_refs = self.rename_group_names()
        self.rename_back_references(back_refs)
        self.regexp = ' '.join(self.regexp.split())

    def __repr__(self):
        """Represent the result."""
        return '{}({})'.format(self.__class__.__name__, self.__dict__)

    def __eq__(self, other):
        """Compare traits."""
        return self.__dict__ == other.__dict__

    def rename_group_names(self):
        """Make regular expression group names unique."""
        global GROUP_COUNT
        self.groups.append((self.name, self.name))
        back_refs = {}
        matches = list(self.groups_rx.finditer(self.regexp))[1:]
        for match in reversed(matches):
            group = match.group(1)
            GROUP_COUNT += 1
            name = f'{group}_{GROUP_COUNT}'
            self.groups.append((name, group))
            start = self.regexp[:match.start(1)]
            end = self.regexp[match.end(1):]
            self.regexp = start + name + end
            back_refs[group] = name
        return back_refs

    def rename_back_references(self, back_refs):
        """Link back references to the renamed regular expression group."""
        matches = list(self.back_ref_rx.finditer(self.regexp))
        for match in reversed(matches):
            name = back_refs[match.group(1)]
            start = self.regexp[:match.start(1)]
            end = self.regexp[match.end(1):]
            self.regexp = start + name + end

    def tokenize_regex(self, other_regex):
        """Replace names in regex with their tokens."""
        if self.phase != 'token':
            matches = list(self.token_rx.finditer(self.regexp))
            for match in reversed(matches):
                token = other_regex[match.group(1)].token
                start = self.regexp[:match.start(1)]
                end = self.regexp[match.end(1):]
                self.regexp = start + token + end
        self.regexp = ' '.join(self.regexp.split())
