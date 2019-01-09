"""Parse the notations."""

from abc import abstractmethod
from lib.result import Result


class Base:
    """Shared parser logic."""

    def __init__(self, args=None):
        """Initialize the parser."""
        self.args = args
        self.parser = self.build_parser()

    @abstractmethod
    def build_parser(self):
        """Return the trait parser."""
        raise NotImplementedError('You need a build_parser function.')

    def result(self, match):
        """Convert parsed tokens into a result."""
        raise NotImplementedError('You need a build_parser function.')

    def parse(self, text: str, trait=None, field=None):
        """Parse the text."""
        results = []
        for match in self.parser.parseWithTabs().scanString(text):
            result = self.result(match)
            if result:
                result.trait = trait
                result.field = field
                results.append(result)
        return results

    def shorthand(self, match, parts, key):
        """Handle shorthand notation like 11-22-33-44:55g."""
        result = Result()
        result.float_value(parts.get(key))
        if not result.value:
            return None
        result.units = 'mm_shorthand'
        if parts[key][-1] == ']':
            result.flags['estimated_value'] = True
        result.ends(match[1], match[2])
        return result
