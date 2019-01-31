"""Parse all traits for the input record."""

from lib.parsers.as_is import AsIs


class StopLooking(Exception):
    """Stop looking for parses because we found one."""


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
        data = {trait: [] for trait, parser in self.parsers}

        for trait, parser in self.parsers:
            try:

                if self.should_skip(data, trait):
                    raise StopLooking()

                for field in self.as_is_fields.get(trait, []):
                    parsed = self.as_is.parse(
                        record[field], field, as_dict=True)
                    if parsed:
                        data[trait] += parsed
                        raise StopLooking()

                for field in self.search_fields:
                    parsed = parser.parse(record[field], field, as_dict=True)
                    if parsed:
                        data[trait] += parsed
                        raise StopLooking()

            except StopLooking:
                pass

        return data

    @staticmethod
    def should_skip(data, trait):
        """Handle pre-processing for the trait."""
        if trait not in ('testes_size', 'testes_state') or not data.get('sex'):
            return False

        if not data['sex'] or data['sex'][0]['value'] != 'female':
            return False

        data[trait].append({
            'flags': {'skipped': "Skipped because sex is 'female'"}})

        return True
