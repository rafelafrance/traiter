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

    def parse(self, text: str, trait=None, field=None, as_dict=False):
        """Parse the text."""
        results = []
        for match in self.parser.parseWithTabs().scanString(text):

            result = self.result(match)

            if result:
                result = self.fix_up_result(text, result)

                if result:
                    result.trait = trait
                    result.field = field
                    if as_dict:
                        result = result.as_dict()
                    results.append(result)

        return results

    # pylint: disable=unused-argument,no-self-use
    def fix_up_result(self, text, result):
        """Fix problematic parses."""
        return result
