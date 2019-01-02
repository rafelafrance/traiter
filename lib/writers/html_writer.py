"""Write the traiter output to an HTML file."""

from lib.writers.base_writer import BaseWriter


class HtmlWriter(BaseWriter):
    """Write the traiter output to a file."""

    def __init__(self, args):
        """Build the writer."""

    def header(self):
        """Output the report header."""

    def row(self):
        """Output a report row."""

    def cell(self):
        """Output a report cell."""

    def footer(self):
        """Output the report footer."""
