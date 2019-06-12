"""Read the traiter input from a file."""

from abc import abstractmethod


class BaseReader:
    """Read the traiter input from a file."""

    def __init__(self, args):
        """Build the reader."""
        self.args = args

    @abstractmethod
    def __enter__(self):
        """Setup the iterator."""

    @abstractmethod
    def __iter__(self):
        """Iterate thru the input file."""

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback):
        """Teardown the iterator."""
