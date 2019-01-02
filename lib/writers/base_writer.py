"""Write the traiter output to a file."""

from abc import abstractmethod


class BaseWriter:
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""
        self.args = args

    @abstractmethod
    def header(self):
        """Output the report header."""

    @abstractmethod
    def row(self):
        """Output a report row."""

    @abstractmethod
    def cell(self):
        """Output a report cell."""

    @abstractmethod
    def footer(self):
        """Output the report footer."""
