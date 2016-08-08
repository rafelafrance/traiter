#!/usr/bin/env python
# -*- coding: utf-8 -*-
# The line above is to signify that the script contains utf-8 encoded characters.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Adapted from https://github.com/rafelafrance/traiter
# Adapted from https://github.com/VertNet/dwc-indexer

__author__ = "John Wieczorek"
__contributors__ = "Raphael LaFrance, Aaron Steele, John Wieczorek"
__copyright__ = "Copyright 2016 vertnet.org"
__version__ = "trait_fields_processor.py 2016-08-07T16:35+02:00"

import csv
import argparse
# from field_utils import index_fields
# from field_utils import HARVEST_FIELDS
from vn_utils import tsv_dialect
# from vn_utils import record_level_resolution
# from vn_utils import license_resolution
from vn_utils import dynamicproperties_resolution
from vn_utils import occurrence_resolution
# from vn_utils import sex_resolution
# from vn_utils import event_resolution
# from vn_utils import location_resolution
# from vn_utils import georef_resolution
# from vn_utils import identification_resolution
# from vn_utils import is_fossil
# from vn_utils import is_mappable
# from vn_utils import was_captive
# from vn_utils import was_invasive
# from vn_utils import has_media
# from vn_utils import has_tissue
# from vn_utils import has_typestatus
# from vn_utils import vn_type
# from vn_utils import rec_rank
# from datetime import datetime
# from trait_parsers.body_mass_parser import BodyMassParser
# from trait_parsers.life_stage_parser import LifeStageParser
# from trait_parsers.sex_parser import SexParser
from trait_parsers.total_length_parser import TotalLengthParser

# need to install regex for the trait parsers to be used
# pip install regex

#INDEX_FIELDS = index_fields()
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
        dialect = tsv_dialect()
        parts = outfilename.split('.')
        posfilename = parts[0]+'_pos.'+parts[1]
        negfilename = parts[0]+'_neg.'+parts[1]
        print 'INDEX_FIELDS: %s' % INDEX_FIELDS
        with open(posfilename, 'w') as posfile:
            poswriter = csv.DictWriter(posfile, dialect=dialect, fieldnames=INDEX_FIELDS)
            with open(negfilename, 'w') as negfile:
                negwriter = csv.DictWriter(negfile, dialect=dialect, fieldnames=INDEX_FIELDS)
                # A header is not used in VertNet indexing chunks. The field order must be 
                # defined in the indexer. A header can be added to the output file by setting 
                # the optional header parameter.
                if header.lower()=='header':
                    poswriter.writeheader()
                    negwriter.writeheader()

                with open(infilename, 'r') as infile:
                    reader = csv.DictReader(infile, dialect=dialect, fieldnames=HARVEST_FIELDS)
                    for row in reader:
#                        print 'row: %s' % row
                        newrow = self.process_harvest_row(row)
                        if newrow is not None:
                            wrong_fields = [k for k in newrow if k not in INDEX_FIELDS]
#                           print 'wrong fields: %s' % wrong_fields
                            for f in wrong_fields:
                                newrow.pop(f)
#                            print 'newrow: %s' % newrow
                            if newrow['haslength'] == 1:
                                poswriter.writerow(newrow)
                            else:
                                negwriter.writerow(newrow)

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
