"""Read the traiter input from a file."""

from abc import abstractmethod


class ReadBase:
    """Read the traiter input from a file."""

    def __init__(self, args):
        """Build the reader."""
        self.args = args

    @abstractmethod
    def __iter__(self):
        """We need to iterate thru the input file."""

    @abstractmethod
    def next(self):
        """Get the next row in the file."""
