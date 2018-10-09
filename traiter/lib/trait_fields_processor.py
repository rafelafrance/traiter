import csv
import argparse
from vn_utils import tsv_dialect
from vn_utils import dialect_attributes
from vn_utils import csv_file_dialect
from vn_utils import dynamicproperties_resolution
from vn_utils import occurrence_resolution
from trait_parsers.total_length_parser import TotalLengthParser

# need to install regex for the trait parsers to be used
# pip install regex

HARVEST_FIELDS = [ 'dynamicproperties', 'occurrenceremarks', 'fieldnotes' ]
INDEX_FIELDS = HARVEST_FIELDS + ['haslength', 'lengthinmm', 'lengthtype', 'lengthunitsinferred']

class VertNetTraitFieldProcessor:

    def __init__(self):
#        self.body_mass_parser    = BodyMassParser()
#        self.life_stage_parser   = LifeStageParser()
#        self.sex_parser          = SexParser()
        self.total_length_parser = TotalLengthParser()

    def parse_row_for_traits(self, row):
        '''
        Parse traits out of the given fields in the row.
        '''
        strings = [row['dynamicproperties'], row['occurrenceremarks'], row['fieldnotes']]
#        traits  = self.sex_parser.preferred_or_search(row['sex'], strings)
#        traits.update(self.life_stage_parser.preferred_or_search(row['lifestage'], strings))

        # Only parse measurements if the record is not an observation. Expects
        # row['vntype'] to have been determined.
#         if row.has_key('vntype') and 'obs' in row['vntype'].lower():
#             traits.update({'haslength': 0, 'lengthinmm': None, \
#                 'lengthunitsinferred': None, 'lengthtype': None})
#             traits.update({'hasmass': 0, 'massing': None, 'massunitsinferred': None})
#         else:
#             traits.update(self.total_length_parser.search_and_normalize(strings))
#             traits.update(self.body_mass_parser.search_and_normalize(strings))

        traits = self.total_length_parser.search_and_normalize(strings)
#        traits.update(self.body_mass_parser.search_and_normalize(strings))
#        print 'strings: %s\ntraits: %s' % (strings, traits)
        return traits

    def parse_harvest_file(self, infilename, outfilename, header=None):
        # fields from the original harvest files
        indialect = csv_file_dialect(infilename)
#        print 'indialect: %s' % dialect_attributes(indialect)
        parts = outfilename.split('.')
        posfilename = parts[0]+'_pos.'+parts[1]
        negfilename = parts[0]+'_neg.'+parts[1]
#        print 'INDEX_FIELDS: %s' % INDEX_FIELDS
        with open(posfilename, 'w') as posfile:
            poswriter = csv.DictWriter(posfile, dialect=tsv_dialect(), fieldnames=INDEX_FIELDS)
            with open(negfilename, 'w') as negfile:
                negwriter = csv.DictWriter(negfile, dialect=tsv_dialect(), fieldnames=INDEX_FIELDS)
                # A header is not used in VertNet indexing chunks. The field order must be
                # defined in the indexer. A header can be added to the output file by setting
                # the optional header parameter.
                if header.lower()=='header':
                    poswriter.writeheader()
                    negwriter.writeheader()

#                i = 0
                with open(infilename, 'r') as infile:
                    reader = csv.DictReader(infile, dialect=indialect, fieldnames=HARVEST_FIELDS)
                    # read the header
                    reader.next()
                    for row in reader:
#                        print 'row: %s' % row
#                        if i % 1 == 0:
                        newrow = self.process_harvest_row(row)
                        if newrow is not None:
                            wrong_fields = [k for k in newrow if k not in INDEX_FIELDS]
#                           print 'wrong fields: %s' % wrong_fields
                            for f in wrong_fields:
                                newrow.pop(f)
#                               print 'newrow: %s' % newrow
                            if newrow['haslength'] == 1:
                                poswriter.writerow(newrow)
                            else:
                                negwriter.writerow(newrow)
#                        i += 1

    def process_harvest_row(self, row):
        """Produces an output record ready for indexing based on a post-harvest input
           record with structure determined by HARVEST_FIELDS. Adds new fields and
           changes contents of some existing fields. All others remain as in the input.
        """

        ### DYNAMICPROPERTIES ###
        # Process the dynamicProperties prior to trait extraction
        dp = dynamicproperties_resolution(row)
        if dp is not None and len(dp) > 0:
            row['dynamicproperties'] = dp

        ### OCCURRENCE ###
        # Fields determined: occurrenceremarks, establishmentmeans (relies on was_captive)
        c = occurrence_resolution(row)
#        print 'occurrence:\n%s' % c
        # Set values of fields from dictionary
        for key, value in c.iteritems():
            row[key] = value

        ### TRAITS ###
        # Process the traits and add trait fields to the record, but only if the record
        # is not an observation. Requires vntype to have been determined.
        # Fields determined: haslength, haslifestage, hasmass, hassex,
        #   lifestageverbatim, sexverbatim, lengthinmm, massing,
        #   lengthunitsinferred, massunitsinferred
        traits = self.parse_row_for_traits(row)
#        print 'traits:\n%s' % traits
        for trait in traits:
#            print 'trait: %s %s' % (trait, traits[trait])
            row[trait]=traits[trait]
#         row['underivedsex'] = row['sex']
#         row['underivedlifestage'] = row['lifestage']
#         row['sex'] = row['derivedsex']
#         row['lifestage'] = row['derivedlifestage']
#         row.pop('derivedsex')
#         row.pop('derivedlifestage')

        ### SEX ###
        # Standardize the field 'sex' after all trait extraction is done
        # fields determined: sex
#        row['sex'] = sex_resolution(row['sex'])
#        print 'row: %s' % row
        return row

def _getoptions():
    """Parse command line options and return them."""
    parser = argparse.ArgumentParser()

    help = 'full path to the input file (required)'
    parser.add_argument("-i", "--inputfile", help=help)

    help = 'output file name, no path (required)'
    parser.add_argument("-o", "--outputfile", help=help)

    help = 'elect header inclusion (default = noheader)'
    parser.add_argument("-e", "--includeheader", help=help)

    help = 'log level (e.g., DEBUG, WARNING, INFO) (optional)'
    parser.add_argument("-l", "--loglevel", help=help)

    return parser.parse_args()

def main():
    options = _getoptions()

#    print 'options: %s' % options

    if options.inputfile is None or len(options.inputfile)==0 or \
       options.outputfile is None or len(options.outputfile)==0:
        s =  'syntax:\n'
        s += 'python trait_fields_processor.py'
        s += ' -i data/test_trait_fields.txt'
        s += ' -o outfile.txt'
        s += ' -e header'
        s += ' -l DEBUG'
        print '%s' % s
        return

    processor = VertNetTraitFieldProcessor()
    inputfile = options.inputfile
    outputfile = options.outputfile
    includeheader = options.includeheader
    loglevel = options.loglevel

    processor.parse_harvest_file(inputfile, outputfile, includeheader)

if __name__ == '__main__':
    main()
