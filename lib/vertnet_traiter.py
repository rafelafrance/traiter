import sys
import csv
from trait_parsers.body_mass_parser import BodyMassParser
from trait_parsers.life_stage_parser import LifeStageParser
from trait_parsers.sex_parser import SexParser
from trait_parsers.total_length_parser import TotalLengthParser


class VertnetTraiter:

    def __init__(self):
        self.body_mass_parser    = BodyMassParser()
        self.life_stage_parser   = LifeStageParser()
        self.sex_parser          = SexParser()
        self.total_length_parser = TotalLengthParser()

    def parse_row(self, row):
        strings = [row['dynamicproperties'], row['occurrenceremarks'], row['fieldnotes']]
        traits  = self.sex_parser.preferred_or_search(row['sex'], strings)
        traits.update(self.life_stage_parser.preferred_or_search(row['lifestage'], strings))
        traits.update(self.total_length_parser.search_and_normalize(strings))
        traits.update(self.body_mass_parser.search_and_normalize(strings))
        return traits

    def parse_csv_file(self, file_name):
        with open(file_name, 'r') as in_file:
            reader = csv.DictReader(in_file)
            for row in reader:
                traits = self.parse_row(row)
                print(reader.line_num)


if __name__ == "__main__":
    vertnet_traiter = VertnetTraiter()
    vertnet_traiter.parse_csv_file(sys.argv[1])
