import sys
import csv
from trait_parsers.body_mass_parser import BodyMassParser
from trait_parsers.life_stage_parser import LifeStageParser
from trait_parsers.sex_parser import SexParser
from trait_parsers.total_length_parser import TotalLengthParser

# need to install regex for this to be used
# pip install regex

# trait fields to add to the harvest files
traitfields = ['has_length', 'has_lifestage', 'has_mass', 'has_sex', 
  'length_in_mm', 'mass_in_g', 'length_units_inferred', 'mass_units_inferred',
  'derived_lifestage', 'derived_sex']

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

    def parse_harvest_file(self, infilename, outfilename, header=None):
        # fields from the original harvest files
        harvestfields = self.harvest_fields()
        dialect = tsv_dialect()
        print 'harvestfields: %s\n%s' % (len(harvestfields), harvestfields)
        newharvestfields = self.harvest_fields_with_traits(harvestfields)
        print 'newharvestfields: %s\n%s' % (len(newharvestfields), newharvestfields)

        # A header is not used in VertNet indexing chunks. The field order must be defined
        # in the indexer. A header can be added optionally by setting the header parameter
        if header is not None:
            with open(outfilename, 'w') as outfile:
                writer = csv.DictWriter(outfile, dialect=dialect, fieldnames=newharvestfields)
                writer.writeheader()

        with open(outfilename, 'a') as outfile:
            writer = csv.DictWriter(outfile, dialect=dialect, fieldnames=newharvestfields)
        
            with open(infilename, 'r') as infile:
                reader = csv.DictReader(infile, dialect=dialect, fieldnames=harvestfields)
                for row in reader:
#                    print '%s' % row
                    traits = self.parse_row(row)
                    newtraits = self.trait_fields(traits)
                    newrow = self.row_with_traits(row, newtraits)
                    print 'newrow:\n%s' % newrow
                    writer.writerow(newrow)
#                    self.row_with_traits(row, traits)
#                    print '%s %s' % (reader.line_num, self.trait_fields(traits))
#                    print '%s %s' % (reader.line_num, traits)
#                    print(reader.line_num)

    def harvest_fields(self):
        fields = []
        with open("./vertnet_harvest_fields.txt", 'r') as o:
            field_names = o.read().split("\n")
            for field_name in field_names:
                if len(field_name) == 0:
                    continue
                fields.append(field_name)
        return fields

    def harvest_fields_with_traits(self, harvestfields):
        newharvestfields = harvestfields
        for trait in traitfields:
            newharvestfields.append(trait)
        return newharvestfields

    def row_with_traits(self, row, traits):
        for trait in traits:
            row[trait]=traits[trait]
        return row
    
    def trait_fields(self, traits):

        # map of the trait fields to the traiter output keys
        traitfieldname_lookup = {
          'has_lifestage' : 'hasLifeStage', 
          'mass_in_g' : 'massInG', 
          'has_sex' : 'hasSex', 
          'derived_lifestage' : 'derivedLifeStage', 
          'has_mass' : 'hasMass', 
          'length_units_inferred' : 'wereLengthUnitsInferred', 
          'derived_sex' : 'derivedSex', 
          'mass_units_inferred' : 'wereMassUnitsInferred', 
          'length_in_mm' : 'lengthInMM', 
          'has_length' : 'hasLength'  
        }
        
        newfields = {}
        for trait in traitfields:
            newfields[trait] = traits[traitfieldname_lookup[trait]]
        return newfields

def tsv_dialect():
    """Get a dialect object with TSV properties.
    parameters:
        None
    returns:
        dialect - a csv.dialect object with TSV attributes"""
    dialect = csv.excel_tab
    dialect.lineterminator='\n'
    dialect.delimiter='\t'
    dialect.escapechar='/'
    dialect.doublequote=True
    dialect.quotechar='"'
    dialect.quoting=csv.QUOTE_NONE
    dialect.skipinitialspace=True
    dialect.strict=False
    return dialect

if __name__ == "__main__":
    vertnet_traiter = VertnetTraiter()
#    Example command line invocation:
#        python vertnet_traiter.py data-2015-10-28-uam_herp-753047f9-b2d1-4356-96c8-c84618183efc-aa outn.txt header
    vertnet_traiter.parse_harvest_file(sys.argv[1], sys.argv[2], sys.argv[3])
#    vertnet_traiter.parse_harvest_file(sys.argv[1])
#    vertnet_traiter.parse_csv_file(sys.argv[1])

# From indexer.py
#        input_class = (input_readers.__name__ + "." +
#                    input_readers.GoogleCloudStorageLineInputReader.__name__)
