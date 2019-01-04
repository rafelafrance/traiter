"""Write the traiter output to a file."""

from abc import abstractmethod


class BaseWriter:
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""
        self.args = args
        self.outfile = args.outfile

    def __enter__(self):
        """Use the writer in with statements."""
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Use the writer in with statements."""
        self.end()

    @abstractmethod
    def start(self):
        """Start the report."""

    @abstractmethod
    def start_row(self, row):
        """Start a report row."""

    @abstractmethod
    def cell(self, results, trait):
        """Build a report cell."""

    @abstractmethod
    def end_row(self):
        """End a report row."""

    @abstractmethod
    def end(self):
        """End the report."""
