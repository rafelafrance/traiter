"""Parse the notations."""

from abc import abstractmethod


class BaseTrait:
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
            if result and result.flags.get('check_false_positive'):
                result = self.check_false_positive(text, result)
            if result:
                result.trait = trait
                result.field = field
                results.append(result)
        return results
