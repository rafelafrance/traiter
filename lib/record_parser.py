"""Parse all traits for the input record."""

# pylint: disable=no-self-use

from lib.parsers.as_is import AsIs


class RecordParser:
    """Handles all of the parsed traits for a record."""

    as_is = AsIs()

    def __init__(self, parsers, search_fields=None, as_is_fields=None):
        """Create the record container."""
        self.parsers = parsers
        self.search_fields = search_fields if search_fields else []
        self.as_is_fields = as_is_fields if as_is_fields else {}

    # #########################################################################
    # HACK: : I hope that this is a temporary set of actions

    def parse_record(self, record):
        """Parse the traits for record."""
        data = {trait: {'flags': {}, 'parsed': []}
                for trait, parser in self.parsers}

        for trait, parser in self.parsers:

            self.before_action(data, trait)
            if data.get(trait) and data[trait]['flags'].get('break'):
                continue

            for field in self.as_is_fields.get(trait, []):
                parsed = self.as_is.parse(record[field], field, as_dict=True)
                data[trait]['parsed'] += parsed
                self.as_is_break_action(data, trait, field)
                if data[trait]['flags'].get('break'):
                    break

            # self.between_action(data, trait)
            # if data[trait]['flags'].get('break'):
            #     continue

            for field in self.search_fields:
                parsed = parser.parse(record[field], field, as_dict=True)
                data[trait]['parsed'] += parsed
                self.search_fields_break_action(data, trait, field)
                if data[trait]['flags'].get('break'):
                    break

            # self.after_action(data, trait)

        return data

    def before_action(self, data, trait):
        """Handle pre-processing for the trait."""
        if trait not in ('testes_size', 'testes_state') or not data.get('sex'):
            return

        if (not data['sex']['parsed']
                or data['sex']['parsed'][0]['value'] != 'female'):
            return

        data[trait]['flags']['break'] = (
            "Skipped because sex is 'female'")

    def as_is_break_action(self, data, trait, field):
        """Handle action inside of the as_is trait parsing loop."""
        if data[trait]['flags'].get('break'):
            return
        if data[trait]['parsed']:
            data[trait]['flags']['break'] = (
                "Using preferred field '{}'".format(field))

    def between_action(self, data, trait):
        """Handle action between as_is parsing & normal trait parsing."""

    def search_fields_break_action(self, data, trait, field):
        """Handle action inside of the search_fields trait parsing loop."""
        if data[trait]['flags'].get('break'):
            return
        if data[trait]['parsed']:
            data[trait]['flags']['break'] = (
                "Found '{}' in '{}'".format(trait, field))

    def after_action(self, data, trait):
        """Handle post-processing for the trait."""

    # HACK: End
    # #########################################################################
