"""Write the traiter output to a file."""

from abc import abstractmethod


class BaseWriter:
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""
        self.args = args

    @abstractmethod
    def start(self):
        """Start the report."""

    @abstractmethod
    def row(self):
        """Build a report row."""

    @abstractmethod
    def cell(self):
        """Build a report cell."""

    @abstractmethod
    def end(self):
        """End the report."""
