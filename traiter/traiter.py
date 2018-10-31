#!/bin/env python

"""Given a CSV file of natural history notes, parse traits."""

import sys
import csv
from lib.trait_parsers.body_mass_parser import BodyMassParser
from lib.trait_parsers.life_stage_parser import LifeStageParser
from lib.trait_parsers.sex_parser import SexParser
from lib.trait_parsers.total_length_parser import TotalLengthParser


class Traiter:
    """Given a CSV file of natural history notes, parse traits."""

    def __init__(self):
        """Build all of the parsers."""
        self.body_mass_parser = BodyMassParser()
        self.life_stage_parser = LifeStageParser()
        self.sex_parser = SexParser()
        self.total_length_parser = TotalLengthParser()

    def parse_row(self, row):
        """
        Parse the following fields in one row of the CSV file.

        Return a dictionary of traits.

        The fields are parsed in this order. Parsers return the first match
        found.
            1) dynamicproperties
            2) occurrenceremarks
            3) fieldnotes
        """
        strings = [
            row['dynamicproperties'],
            row['occurrenceremarks'],
            row['fieldnotes']]
        traits = self.sex_parser.preferred_or_search(row['sex'], strings)
        traits.update(self.life_stage_parser.preferred_or_search(
            row['lifestage'], strings))
        traits.update(self.total_length_parser.search_and_normalize(strings))
        traits.update(self.body_mass_parser.search_and_normalize(strings))
        return traits

    def parse_csv_file(self, file_name):
        """
        Parse a CSV file looking for traits.

        We look for traits in certain fields in the CSV file.
        """
        with open(file_name, 'r') as in_file:
            reader = csv.DictReader(in_file)
            for row in reader:
                _ = self.parse_row(row)  # noqa
                print(reader.line_num)


if __name__ == "__main__":
    traiter = Traiter()
    traiter.parse_csv_file(sys.argv[1])
