"""Build parsed record objects and accumulate totals."""

from lib.record_parser import RecordParser


class FileParser:
    """Build parsed record objects."""

    def __init__(self, args, parsers):
        """Create data for making parsed record objects and totals."""
        self.args = args
        self.parsers = parsers
        self.search_fields = args.search_field
        self.as_is_fields = args.as_is

    def new_record_parser(self):
        """Build a parsed record object."""
        return RecordParser(
            self.parsers, self.search_fields, self.as_is_fields)

    def accumulate(self, trait_list):
        """Add up totals."""
