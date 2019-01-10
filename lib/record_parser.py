"""Parse all traits for the input record."""

from lib.traits.as_is import AsIs


class RecordParser:
    """Handles all of the parsed traits for a record."""

    as_is = AsIs()

    def __init__(self, parsers, search_fields=None, as_is_fields=None):
        """Create the record container."""
        self.parsers = parsers
        self.search_fields = search_fields if search_fields else []
        self.as_is_fields = as_is_fields if as_is_fields else {}

    def parse_record(self, record):
        """Parse the traits for record."""
        results = {trait: [] for trait, parser in self.parsers}

        for trait, parser in self.parsers:

            for field in self.as_is_fields.get(trait, []):
                parsed = self.as_is.parse(record[field], field, as_dict=True)
                results[trait] += parsed

            for field in self.search_fields:
                parsed = parser.parse(record[field], field, as_dict=True)
                results[trait] += parsed

        return results

    def to_json(self, results):
        """Convert the results to json."""
